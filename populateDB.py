from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Shop, Product

engine = create_engine('sqlite:///shopData.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# Placeholder Data

user = User(email= "blair@fakemail.com")
session.add(user)
session.commit()

user = User(email= "pat@fakemail.com")
session.add(user)
session.commit()


#############Store 1
shop = Shop(name="Blair's Blankets",
            hours="9am-7pm",
            phone_number="555-7654",
            image="https://images.pexels.com/photos/90317/pexels-photo-90317.jpeg",
            owner_id=1)
session.add(shop)
session.commit()

product = Product(name="duvet",
            description="it is the one that goes on the bed",
            image="https://cdn.pixabay.com/photo/2016/04/28/13/41/sunday-1358907__340.jpg",
            price="$36",
            shop_id=1)
session.add(product)
session.commit()

product = Product(name="sheet",
            description="it is white",
            image="https://cdn.pixabay.com/photo/2016/01/19/17/41/bed-linen-1149842__340.jpg",
            price="$16",
            shop_id=1)
session.add(product)
session.commit()

product = Product(name="blanket",
            description="our signature product",
            image="https://static.pexels.com/photos/57686/pexels-photo-57686.jpeg",
            price="$22",
            shop_id=1)
session.add(product)
session.commit()



#############Store 2
shop = Shop(name="Eda's Eats",
            hours="1030am-2pm and 5-10pm",
            phone_number="555-3881",
            image="http://www.publicdomainpictures.net/pictures/10000/velka/1-1248161543llOC.jpg",
            owner_id=2)
session.add(shop)
session.commit()

product = Product(name="broccoli",
            description="high in vitamin k",
            image="https://images.pexels.com/photos/47347/broccoli-vegetable-food-healthy-47347.jpeg",
            price="$7",
            shop_id=2)
session.add(product)
session.commit()

product = Product(name="artichoke",
            description="premium butter conveyance device",
            image="http://www.publicdomainpictures.net/pictures/220000/velka/artichauts-legumes-marches.jpg",
            price="$4",
            shop_id=2)
session.add(product)
session.commit()

product = Product(name="carrot",
            description="orange sticks",
            image="https://images.pexels.com/photos/143133/pexels-photo-143133.jpeg?w=940&h=650&auto=compress&cs=tinysrgb",
            price="$1",
            shop_id=2)
session.add(product)
session.commit()

product = Product(name="strawberries",
            description="terrifying",
            image="https://static.pexels.com/photos/46174/strawberries-berries-fruit-freshness-46174.jpeg",
            price="$3000 per ton",
            shop_id=2)
session.add(product)
session.commit()

product = Product(name="banana",
            description="there's more potassium in a potato",
            image="https://static.pexels.com/photos/38283/bananas-fruit-carbohydrates-sweet-38283.jpeg",
            price="$3",
            shop_id=2)
session.add(product)
session.commit()


#############Store 3
shop = Shop(name="Pat's Pants",
            hours="M-F: 8am-5pm, Sa: 9am-9pm, Su: closed",
            phone_number="555-9842",
            image="https://static.pexels.com/photos/165226/pexels-photo-165226.jpeg",
            owner_id=2)
session.add(shop)
session.commit()

product = Product(name="jeans",
            description="imported denim",
            image="https://static.pexels.com/photos/52518/jeans-pants-blue-shop-52518.jpeg",
            price="$47",
            shop_id=3)
session.add(product)
session.commit()

product = Product(name="other jeans",
            description="mostly like the other jeans, but kinda different, in some ways",
            image="https://images.pexels.com/photos/65676/nanjing-studio-jeans-65676.jpeg",
            price="$23",
            shop_id=3)
session.add(product)
session.commit()


#############Store 4
shop = Shop(name="Cody's Coats",
            hours="oh pretty much whenever",
            phone_number="555-6572",
            image="https://cdn.pixabay.com/photo/2016/11/18/13/48/clothes-1834650__340.jpg",
            owner_id=2)
session.add(shop)
session.commit()

product = Product(name="blue",
            description="it's blue!",
            image="https://cdn.pixabay.com/photo/2016/11/29/13/26/casual-1869832__340.jpg",
            price="$7",
            shop_id=4)
session.add(product)
session.commit()

product = Product(name="red",
            description="it's red",
            image="https://cdn.pixabay.com/photo/2016/07/30/18/22/zip-1557693__340.jpg",
            price="$77",
            shop_id=4)
session.add(product)
session.commit()

product = Product(name="black",
            description="no not the pink shirt and no not the watch we're talking about the black coat",
            image="https://static.pexels.com/photos/179909/pexels-photo-179909.jpeg",
            price="$777",
            shop_id=4)
session.add(product)
session.commit()

product = Product(name="brown",
            description="i'm sure i've seen this image used somewhere before...",
            image="https://cdn.pixabay.com/photo/2015/03/26/09/54/people-690547__340.jpg",
            price="$7777",
            shop_id=4)
session.add(product)
session.commit()

product = Product(name="blue",
            description="yet another blue coat!",
            image="https://snappygoat.com/b/791254d040b77c5fa7ee3c55f7c92dfff7b93f46",
            price="$77777",
            shop_id=4)
session.add(product)
session.commit()

#############Store 5
shop = Shop(name="Shane's Shoes",
            hours="ALL DAY ALL DAY ALL DAY",
            phone_number="555-4444",
            image="https://static.pexels.com/photos/318236/pexels-photo-318236.jpeg",
            owner_id=2)
session.add(shop)
session.commit()

product = Product(name="yellow lovelies",
            description="dandy as your mother",
            image="https://static.pexels.com/photos/137603/pexels-photo-137603.jpeg",
            price="twelve",
            shop_id=5)
session.add(product)
session.commit()

product = Product(name="shoodly woodlys",
            description="for your feetsie weetsies!",
            image="https://static.pexels.com/photos/267320/pexels-photo-267320.jpeg",
            price="four",
            shop_id=5)
session.add(product)
session.commit()

product = Product(name="harold",
            description="artisanal af right?",
            image="https://static.pexels.com/photos/292999/pexels-photo-292999.jpeg",
            price="nine",
            shop_id=5)
session.add(product)
session.commit()

product = Product(name="heels",
            description="i don't know anything about horcruxes!",
            image="https://static.pexels.com/photos/336372/pexels-photo-336372.jpeg",
            price="seven",
            shop_id=5)
session.add(product)
session.commit()

product = Product(name="sonia",
            description="fresh from the cobbler this morning",
            image="https://static.pexels.com/photos/293405/pexels-photo-293405.jpeg",
            price="SEVEN",
            shop_id=5)
session.add(product)
session.commit()


#############Store 6
shop = Shop(name="Antoni's Antiques",
            hours="7am-3pm Tues-Sat",
            phone_number="555-3233",
            image="https://static.pexels.com/photos/264507/pexels-photo-264507.jpeg",
            owner_id=2)
session.add(shop)
session.commit()

product = Product(name="chair",
            description="boy i tell you is it a chair!",
            image="https://cdn.pixabay.com/photo/2016/11/19/15/50/chair-1840011__340.jpg",
            price="$99",
            shop_id=6)
session.add(product)
session.commit()

product = Product(name="table",
            description="itsah table though, innit?",
            image="https://static.pexels.com/photos/17738/pexels-photo.jpg",
            price="$99",
            shop_id=6)
session.add(product)
session.commit()

product = Product(name="spectacles",
            description="i found them on the ground",
            image="https://cdn.pixabay.com/photo/2014/08/11/03/51/glasses-415257__340.jpg",
            price="$99",
            shop_id=6)
session.add(product)
session.commit()

product = Product(name="sofa",
            description="they don't make 'em like this anymore",
            image="http://www.publicdomainpictures.net/pictures/210000/velka/leather-sofa-14883910431AU.jpg",
            price="$99",
            shop_id=6)
session.add(product)
session.commit()


#############Store 7
shop = Shop(name="Candace's Candles",
            hours="8pm-1am Fridays",
            phone_number="555-7841",
            image="https://cdn.pixabay.com/photo/2016/11/18/19/13/buildings-1836478__340.jpg",
            owner_id=2)
session.add(shop)
session.commit()

product = Product(name="product #Q77TT2",
            description="monotheism was a precursor,",
            image="https://static.pexels.com/photos/33197/tealight-candles-tea-lights-wax.jpg",
            price="04601",
            shop_id=7)
session.add(product)
session.commit()

product = Product(name="product #F5R55F",
            description="a transitional thought-technology",
            image="https://static.pexels.com/photos/233296/pexels-photo-233296.jpeg",
            price="20533",
            shop_id=7)
session.add(product)
session.commit()

product = Product(name="product #7PX5DE",
            description="between polytheism and the enlightenment",
            image="https://static.pexels.com/photos/359564/pexels-photo-359564.jpeg",
            price="38601",
            shop_id=7)
session.add(product)
session.commit()

product = Product(name="product #9TM7I4",
            description="polytheism was more antifragile.",
            image="http://www.publicdomainpictures.net/pictures/170000/velka/candle-with-flame-1.jpg",
            price="73176",
            shop_id=7)
session.add(product)
session.commit()

print "populated the database has been, sir"
