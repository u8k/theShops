from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shop, Product, User
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)
defImgUrl = "http://xpenology.org/wp-content/themes/qaengine/img/default-thumbnail.jpg"

#allow CORS
#CORS(app)

# force update of static files on every refresh
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "ShopShop"

# Connect to Database and create database session
engine = create_engine('sqlite:///shopData.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#enable gAuth google sign in
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
        'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['email'] = data['email']

    # see if user exists, if they don't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # respond to the client, sending them json data for the now logged in user
    user = session.query(User).filter_by(id=login_session['user_id']).one()
    return jsonify(user=user.serialize)

# User Helper Functions
def createUser(login_session):
    newUser = User(email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/theshops/gdisconnect/')
def gdisconnect():
    # check if user has an access token
    access_token = login_session.get('access_token')
    if access_token is not None:
        # send request to google to void the current token
        url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
    # Reset the user's sesson.
    login_session.pop('access_token', None)
    login_session.pop('gplus_id', None)
    login_session.pop('email', None)
    login_session.pop('user_id', None)
    return jsonify("success")

############ PORTFOLIO REDIRECT #################
@app.route("/")
def sendToPortfolio():
    return redirect("https://u8k.github.io/portfolio/")

######THE SHOPS#############
#main and ONLY page intended for general public viewing
@app.route("/theshops/")
def main():
    #pass in the userID/email if a user is logged in, else send an empty string
    try:
        userId = login_session['user_id']
    except:
        userId = ''
    try:
        email = login_session['email']
    except:
        email = ''
    # Create anti-forgery state token, pass to client
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # pass in list of all shops
    shops = session.query(Shop).order_by(asc(Shop.id))
    return render_template('template.html', shops=shops, userId=userId,
        STATE=state, email=email)


#public API GET routes:

#get a directory of all shops
@app.route("/theshops/shops/", methods = ['GET'])
def allShops():
    shops = session.query(Shop).all()
    return jsonify(shops=[i.serialize for i in shops])

#get a list of all products from all shops
@app.route("/theshops/products/", methods = ['GET'])
def allProducts():
    products = session.query(Product).all()
    return jsonify(products=[i.serialize for i in products])

#get a product list for a specific shop
@app.route("/theshops/shop/<int:shop_id>/", methods = ['GET'])
def shopInventory(shop_id):
    products = session.query(Product).filter_by(shop_id=shop_id).all()
    return jsonify(products=[i.serialize for i in products])

#get info for a single product
@app.route("/theshops/product/<int:product_id>/", methods = ['GET'])
def productInfo(product_id):
    product = session.query(Product).filter_by(id=product_id).one()
    return jsonify(product=product.serialize)


    #private API non-GET routes:

#private API POST routes
#create a shop
@app.route('/theshops/shop/create/', methods=['POST'])
def createShop():
    newShop = Shop(name=request.data, owner_id=login_session['user_id'],
        image = defImgUrl)
    session.add(newShop)
    session.commit()
    shop = session.query(Shop).filter_by(name=request.data,
        owner_id=login_session['user_id']).order_by(Shop.id.desc()).first()
    return jsonify(shop=shop.serialize)

#edit a shop
@app.route('/theshops/shop/<int:shop_id>/<trait>/', methods=['POST'])
def editShop(shop_id, trait):
    print ("hello")
    editedShop = session.query(Shop).filter_by(id=shop_id).one()
    if login_session['user_id'] != editedShop.owner_id:
        return jsonify("unauthorized")
    if trait == 'name':
        editedShop.name = request.data
    if trait == 'hours':
        editedShop.hours = request.data
    if trait == 'phone_number':
        editedShop.phone_number = request.data
    if trait == 'image':
        editedShop.image = request.data
    session.commit()
    return jsonify("success")

#delete a shop
@app.route('/theshops/shop/<int:shop_id>/delete/', methods=['POST'])
def deleteShop(shop_id):
    targetShop = session.query(Shop).filter_by(id=shop_id).one()
    if login_session['user_id'] != targetShop.owner_id:
        return jsonify("unauthorized")
    #also delete the shop's products
    for product in session.query(Product).filter_by(shop_id=shop_id).all():
        session.delete(product)
    session.delete(targetShop)
    session.commit()
    return jsonify("success")

#create a product
@app.route('/theshops/product/create/<int:shop_id>/', methods=['POST'])
def createProduct(shop_id):
    targetShop = session.query(Shop).filter_by(id=shop_id).one()
    if login_session['user_id'] != targetShop.owner_id:
        return jsonify("unauthorized")
    newProduct = Product(name=request.data, shop_id=shop_id, image=defImgUrl)
    session.add(newProduct)
    session.commit()
    product = session.query(Product).filter_by(name=request.data,
        shop_id=shop_id).order_by(Product.id.desc()).first()
    return jsonify(product=product.serialize)

#edit a product
@app.route('/theshops/product/<int:product_id>/<trait>/', methods=['POST'])
def editProduct(product_id, trait):
    editedProduct = session.query(Product).filter_by(id=product_id).one()
    targetShop = session.query(Shop).filter_by(id=editedProduct.shop_id).one()
    if login_session['user_id'] != targetShop.owner_id:
        return jsonify("unauthorized")
    if trait == 'name':
        editedProduct.name = request.data
    if trait == 'description':
        editedProduct.description = request.data
    if trait == 'price':
        editedProduct.price = request.data
    if trait == 'image':
        editedProduct.image = request.data
    session.commit()
    return jsonify("success")

#delete a product
@app.route('/theshops/product/<int:product_id>/delete/', methods=['POST'])
def deleteProduct(product_id):
    toBeDeleted = session.query(Product).filter_by(id=product_id).one()
    targetShop = session.query(Shop).filter_by(id=toBeDeleted.shop_id).one()
    if login_session['user_id'] != targetShop.owner_id:
        return jsonify("unauthorized")
    session.delete(toBeDeleted)
    session.commit()
    return jsonify("success")

###################### METRO MAP ######################
@app.route("/metro-map/")
def sendToMetroMap():
    return redirect("https://u8k.github.io/la-metro-map/")

##################### WEATHER #########################
@app.route("/weather/", methods = ['GET'])
def weather():
    return render_template('weather.html')

##################### TWITCH #########################
@app.route("/twitch/", methods = ['GET'])
def twitch():
    return render_template('twitch.html')

@app.route("/twitch/", methods = ['POST'])
def twitchAPI():
    channel = request.data
    url = "https://api.twitch.tv/kraken/streams/" + channel + "?client_id=f9548j618zhrxjedzvjdinqmx44lsl"
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    #if they aren't currently streaming, then check if the channel is dead
    if data['stream'] == None:
        url = "https://api.twitch.tv/kraken/channels/" + channel + "?client_id=f9548j618zhrxjedzvjdinqmx44lsl"
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]
        data = json.loads(result)
        if data['status'] == 404:
            return jsonify(' is a defunct channel', 'false')
        return jsonify(' is currently offline', 'false')
    return jsonify(" is playing " + data['stream']['game'], 'true')

app.secret_key = 'the_very_most_secret_of_keys'

if __name__ == '__main__':
    #app.secret_key = 'the_very_most_secret_of_keys'
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
    #app.run(host='0.0.0.0')
