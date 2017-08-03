'use strict';

var userId;
var userEmail;
var STATE;
var shopList;//raw json recieved from backend
var shopDirectory = [];//organized array, shops placed at array position coresponding w/ their ID
var shopInventoryList = [];
var defImgUrl = "http://xpenology.org/wp-content/themes/qaengine/img/default-thumbnail.jpg"
var isDetailPanelUp = false;

function getVars(user_Id, state, user_email) {//pulls in global variables from the html
  userId = user_Id;
  userEmail = user_email;
  STATE = state;
}

(function getData() {// Load in and store data as json via API
  apiCall ('/shops', "GET", (json) => {
    shopList = json;
    var numberOfShops = shopList['shops'].length;
    for (var i = 0; i < numberOfShops; i++) {
      var shopId = (shopList['shops'][i]['id']);
      shopDirectory[shopId] = shopList['shops'][i];
      apiCall (('/shop/' + shopId), "GET", (json, url) => {
        shopInventoryList[(url.slice(6))] = json;
      });
    }
  });
})();

function checkUser() {// checks if user is signed in/out and alters page accordingly
  if ((userId != "") && (userId != undefined)) {
    document.getElementById("create-new-shop").classList.remove('removed');
    document.getElementById("logout").classList.remove('removed');
    document.getElementById("signInButton").classList.add('removed');
    document.getElementById("user-status").innerHTML = "logged in as "+userEmail;
  } else {
    document.getElementById("create-new-shop").classList.add('removed');
    document.getElementById("logout").classList.add('removed');
    document.getElementById("signInButton").classList.remove('removed');
    document.getElementById("user-status").innerHTML = "log in for creation<br>priviledges";
  }
}

function showShopDetailPanel(shopID) {
  //catch if user tries to open panel w/in first seconds of app loading,
  //before the data has loaded in
  if (((typeof shopInventoryList[shopID]) == 'undefined')) {return;}
  //check if the panel is already up, don't allow trying to open multiple
  if (isDetailPanelUp) {return;}
  else {isDetailPanelUp = true;}
  var topContainer = document.getElementById("detail-panel-top");
  //generate product listings
  for (var i = 0; i < shopInventoryList[shopID]['products'].length; i++) {
    displayProduct(shopID, i)
  }
  //deleteShop and image editing buttons, IFF user is owner
  if (userId == shopDirectory[shopID]['owner_id']){
    createButton("delete shop", '-', topContainer, ()=>{(deleteShop(shopID));});
    topContainer.appendChild(document.createElement("br"));
    createButton("edit image", '-shop-', topContainer,
      (btn)=>{(editShop(btn, shopID,'image'));});
    createInput('image', 100)
  }
  //set shop meta text and related buttons/input fields
  createText('name', shopDirectory[shopID]['shop-name']);
  if (userId == shopDirectory[shopID]['owner_id']){
    createInput('name', 100)
    createButton("edit name", '-shop-', topContainer,
    (btn)=>{(editShop(btn, shopID,'name'));});
    topContainer.appendChild(document.createElement("br"));
    topContainer.appendChild(document.createElement("br"));
  }
  createText('hours-label', 'hours:');
  createText('hours', shopDirectory[shopID]['shop-hours']);
  if (userId == shopDirectory[shopID]['owner_id']){
    createInput('hours', 60)
    createButton("edit hours", '-shop-', topContainer,
      (btn)=>{(editShop(btn, shopID,'hours'));});
    topContainer.appendChild(document.createElement("br"));
    topContainer.appendChild(document.createElement("br"));
  }
  createText('phone_number-label', 'phone_number:');
  createText('phone_number', shopDirectory[shopID]['shop-phone_number']);
  if (userId == shopDirectory[shopID]['owner_id']){
    createInput('phone_number', 20)
    createButton("edit phone_number", '-shop-', topContainer,
      (btn)=>{(editShop(btn, shopID,'phone_number'));});
    topContainer.appendChild(document.createElement("br"));
    createInput('product', 80)
    createButton("create product", '-', topContainer,
      (btn)=>{(createProduct(btn, shopID));});
  }
  function createText(kind, text) {
    var x = document.createElement("div");
    x.setAttribute('id', 'shop-'+kind);
    topContainer.appendChild(x);
    x.innerHTML = text
  }
  function createInput(trait, maxLength) {
    topContainer.appendChild(document.createElement("br"));
    var input = document.createElement("input");
    input.setAttribute('type', 'text');
    input.setAttribute('placeholder', 'shop '+trait);
    input.setAttribute('id', ('input-shop-'+trait));
    input.setAttribute('class', 'removed input');
    input.setAttribute('maxlength', maxLength);
    topContainer.appendChild(input);
    topContainer.appendChild(document.createElement("br"));
  }
  var wrapper = document.getElementById("panel-wrapper");
  var panel = document.getElementById("shop-detail-panel");
  //disable scrolling on main window
  document.body.classList.add('no-scroll');
  //set width to hide scroll bar behind wrapper
  var wrapperWidth = window.getComputedStyle(wrapper).getPropertyValue("width")
  panel.style.width = (((Number(wrapperWidth.slice(0,-2)))+20)+ "px");
  //set top and inventory-containers to width of wrapper
  document.getElementById("inventory-container").style.width = wrapperWidth;
  document.getElementById("detail-panel-top").style.width = wrapperWidth;
  //set background of panel to the shop's image
  wrapper.style.backgroundImage  = "url(" + shopDirectory[shopID]['shop-image'] + ")";
  //animate in!
  document.getElementById("closeShopDetailPanel").classList.remove('hidden');
  wrapper.classList.remove('hidden');
}

function displayProduct(shopID, i) {//fills in featured product section of the shopPanel
  var id = shopInventoryList[shopID]['products'][i]['id'];
  var product = document.createElement("div");
  product.setAttribute('class', 'product');
  product.setAttribute('id', ('product'+i));
  product.addEventListener("click", ()=>{toggleProductDetails(product, i)});
  function createText(kind, parent) {
    var x = document.createElement("div");
    x.setAttribute('id', 'product-'+kind+id);
    x.setAttribute('class', 'product-'+kind);
    parent.appendChild(x);
    x.innerHTML = shopInventoryList[shopID]['products'][i]['product-'+kind];
  }
  function createInput(trait, maxLength) {
    if (trait == "description") {
      var input = document.createElement("textarea");
      input.setAttribute('rows', '3');
    } else {
      var input = document.createElement("input");
      input.setAttribute('type', 'text');
    }
    input.setAttribute('placeholder', 'product-'+trait);
    input.setAttribute('class', ('removed input input-edit-product-'+trait));
    input.setAttribute('id', ('input-edit-product-'+trait+id));
    input.setAttribute('maxlength', maxLength);
    input.addEventListener("click", (e)=>{e.stopPropagation();});
    details.appendChild(input);
    details.appendChild(document.createElement("br"));
  }
  var image = document.createElement("IMG");
  image.setAttribute("src", shopInventoryList[shopID]['products'][i]['product-image']);
  image.setAttribute("alt", "owner provided product image");
  image.setAttribute('class', 'product-image');
  image.setAttribute('id', ('product-image'+id));
  product.appendChild(image);
  createText('name', product);
  var details = document.createElement("div");
  details.setAttribute('class', 'product-detail removed');
  details.setAttribute('id', 'product-detail'+i);
  createText('description', details)
  var priceLabel = document.createElement("div");
  priceLabel.setAttribute('class', 'product-price-label');
  details.appendChild(priceLabel);
  priceLabel.innerHTML = "price:";
  createText('price', details)
  product.appendChild(details);
  //owner only buttons
  if (userId == shopDirectory[shopID]['owner_id']){
    createInput('name', 80);
    createButton('edit name', "-product-", details,
      (btn) => {(editProduct(btn, id, shopID, 'name'))});
    createInput('image', 100);
    createButton('edit image', "-product-", details,
      (btn) => {(editProduct(btn, id, shopID, 'image'))});
    createInput('description', 250);
    createButton('edit description', "-product-",
      details, (btn) => {(editProduct(btn, id, shopID, 'description'))});
    createInput('price', 8);
    createButton('edit price', "-product-", details,
      (btn) => {(editProduct(btn, id, shopID, 'price'))});
    createButton('delete product', "-", details,
      () => {deleteProduct(id, shopID, product)});
  }
  document.getElementById("inventory-container").appendChild(product);
}

function createButton(text, classMod, parent, clickFunction) {
  //'classMod' is the value that will replace Spaces when
  //converting 'text' to the button's class name
  var btn = document.createElement("button");
  btn.setAttribute('class', 'button ' + text.replace(/ /g, classMod));
  btn.innerHTML = text;
  btn.addEventListener("click", (e)=>{
    e.stopPropagation();
    //addEnterListener(()=>{clickFunction(btn);});
    clickFunction(btn);
  });
  parent.appendChild(btn);
}

function closeShopDetailPanel() {
  // return scrolling to main
  document.body.classList.remove('no-scroll');
  //animate out!
  document.getElementById("panel-wrapper").classList.add('hidden');
  document.getElementById("closeShopDetailPanel").classList.add('hidden');
  removeAllChildren(document.getElementById("detail-panel-top"));
  removeAllChildren(document.getElementById("inventory-container"));
  function removeAllChildren(parent) {
    var childCount = parent.childNodes.length;
    for (var i = 0; i < childCount; i++) {
      parent.removeChild(parent.childNodes[0]);
    }
  }
  isDetailPanelUp = false;
}

function toggleProductDetails(self, prodNum) {
  var element = document.getElementById('product-detail'+prodNum);
  if (element.classList.contains('removed')) {
    element.classList.remove('removed');
  } else {
    element.classList.add('removed');
  }
}

function createProduct(btn, shopID) {
  var input = document.getElementById("input-shop-product");
  if (btn.innerHTML != 'submit') {
    btn.innerHTML = 'submit';
    input.classList.remove('removed');
    input.focus();
  } else {
    apiCall('/product/create/'+ shopID , 'POST', (json) => {
      //add new product to clientSide data
      var array = shopInventoryList[shopID]['products'];
      var i = array.length;
      array.push(json['product']);
      //update current display
      displayProduct(shopID, i);
      toggleProductDetails(document.getElementById("product"+i), i);
      btn.innerHTML = 'create new product';
      input.classList.add('removed');
      input.setAttribute('placeholder', "product name");
      input.value = "";
    }, input.value);
  }
}

function editProduct(btn, prodID, shopID, trait) {
  var display = document.getElementById('product-'+trait+prodID);
  var input = document.getElementById('input-edit-product-'+trait+prodID);
  if (btn.innerHTML != 'submit') {
    btn.innerHTML = 'submit';
    if (trait == "image") {input.value = display.src}
    else if (display.innerHTML != "") {
      input.value = display.innerHTML
      display.classList.add('removed');
    }
    input.classList.remove('removed');
    input.focus();
  } else {
    //call to edit product in server DB
    apiCall('/product/'+ prodID +'/'+ trait, 'POST', (json) => {
      if (json == "success") {
        //edit current product display
        if (trait == "image") {display.src = input.value}
        else {
          display.innerHTML = input.value;
          display.classList.remove('removed');
        }
        btn.innerHTML = 'edit '+trait;
        input.classList.add('removed');
        //find and edit product in clientSide data
        var length = shopInventoryList[shopID]['products'].length;
        for (var i = 0; i < length; i++) {
          if (prodID == shopInventoryList[shopID]['products'][i].id) {
            shopInventoryList[shopID]['products'][i]['product-'+trait] = input.value
            i = length;
          }
        }
      }
    }, input.value);
  }
}

function deleteProduct(prodID, shopID, product) {
  var check = confirm("You sure?\n\nThis cannot be undone.");
  if (check == true) {
    //call to remove product from severDB
    apiCall('/product/'+ prodID +'/delete', 'POST', (json) => {
      if (json == "success") {
        //remove product from the display
        product.parentNode.removeChild(product);
        //find and remove product from clientSide data
        var length = shopInventoryList[shopID]['products'].length;
        for (var i = 0; i < length; i++) {
          if (prodID == shopInventoryList[shopID]['products'][i].id) {
            shopInventoryList[shopID]['products'].splice(i, 1);
            i = length;
          }
        }
      }
    });
  }
}

function createShop() {
  var btn = document.getElementById("create-new-shop");
  var input = document.getElementById("input-create-shop");
  if (btn.innerHTML != 'submit') {
    btn.innerHTML = 'submit';
    input.classList.remove('removed');
    input.focus();
  } else {
    apiCall('/shop/create', 'POST', (json) => {
      //add new product to clientSide data
      shopList['shops'].push(json['shop'])
      var id = json['shop'].id
      shopDirectory[id] = json['shop'];
      var products = [];
      shopInventoryList[id] = {products}
      //display new shop's detail panel
      showShopDetailPanel(id);
      //display a new listing in the directory
      var shop = document.createElement("div");
      shop.setAttribute('class', 'shop');
      shop.setAttribute('id', ('shop'+id));
      var shopAttr = document.createAttribute("onclick");
      shopAttr.value = ("showShopDetailPanel("+ id +")");
      shop.setAttributeNode(shopAttr);
      var image = document.createElement("IMG");
      image.setAttribute("src", defImgUrl);
      image.setAttribute("alt", "owner provided shop image");
      image.setAttribute('class', 'front-shop-image');
      image.setAttribute('id', ('front-shop-image'+id));
      shop.appendChild(image);
      var title = document.createElement("div");
      title.setAttribute('class', 'front-shop-name');
      title.setAttribute('id', ('front-shop-name'+id));
      title.innerHTML = input.value;
      shop.appendChild(title);
      document.getElementById("shop-directory").appendChild(shop);
      //reset the create button/text field
      btn.innerHTML = 'create new shop';
      input.classList.add('removed');
      input.setAttribute('placeholder', "shop name");
      input.value = "";
    }, input.value);
  }
}

function editShop(btn, shopID, trait) {
  var input = document.getElementById('input-shop-'+trait)
  if (trait == "image") {
    display = document.getElementById("panel-wrapper");
  } else {
    var display = document.getElementById('shop-'+trait)
  }
  if (btn.innerHTML != 'submit') {
    btn.innerHTML = 'submit';
    if (trait == "image") {
      input.value = display.style.backgroundImage.slice(5,-2)
    }
    else if (display.innerHTML != "") {
      input.value = display.innerHTML
      display.classList.add('removed');
    }
    input.classList.remove('removed');
    input.focus();
  } else {
    //call to edit product in server DB
    apiCall('/shop/'+ shopID +'/'+ trait, 'POST', (json) => {
      if (json == "success") {
        //edit current product display
        if (trait == "image") {
          display.style.backgroundImage = "url(" + input.value + ")";
          document.getElementById('front-shop-image'+shopID).src = input.value;
        }
        else {
          display.innerHTML = input.value;
          display.classList.remove('removed');
        }
        if (trait == 'name') {
          document.getElementById('front-shop-name'+shopID).innerHTML = input.value;
        }
        btn.innerHTML = 'edit '+trait;
        input.classList.add('removed');
        //edit product in clientSide data
        shopDirectory[shopID]['shop-'+trait] = input.value;
      }
    }, input.value);
  }
}

function deleteShop(shopID) {
  var check = confirm("You sure?\n(deleting a shop will also delete all of it's items)\n\nThis cannot be undone.");
  if (check == true) {
    //update display
    var target = document.getElementById("shop"+shopID);
    target.parentNode.removeChild(target);
    closeShopDetailPanel();
    //server call to delete shop
    apiCall('/shop/'+ shopID +'/delete', 'POST', (json) => {
      //find and remove shop from client sideDB
        var length = shopList['shops'].length
        for (var i = 0; i < length; i++) {
          if (shopID == shopList['shops'][i].id) {
            shopList['shops'].splice(i,1);
            i = length;
          }
        }
    });
  }
}

function apiCall(url, method, callback, data) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var json = JSON.parse(xhttp.responseText);
      if (json == "unauthorized") {
        alert("unauthorized");
      } else {
        callback(json, url);
      }
    }
  }
  xhttp.open(method, "/theshops"+url+ "/", true);
  xhttp.send(data);
}

function logout() {
  var pending = setInterval(tick , 100);
  document.getElementById("user-status").innerHTML = ".";
  apiCall('/gdisconnect', "GET", ()=>{
    userId = '';
    userEmail = '';
    clearInterval(pending);
    checkUser();
  })
}

function tick() {
  document.getElementById("user-status").innerHTML += " .";
}

//callback function for google sign in
function signInCallback(authResult) {
  var pending = setInterval(tick , 100);
  document.getElementById("user-status").innerHTML = ".";
  if (authResult['code']) {
    // Send the one-time-use code to the server, if the server responds, write a 'login successful' message to the web page and then redirect back to the main page
    $.ajax({
      type: 'POST',
      url: '/gconnect?state=' + STATE,
      processData: false,
      data: authResult['code'],
      contentType: 'application/octet-stream; charset=utf-8',
      success: function(result) {
        // Handle or verify the server response if necessary.
        if (result) {
          userEmail = result.user["user-email"];
          userId = result.user["user-id"];
          clearInterval(pending);
          checkUser();
        } else if (authResult['error']) {
          console.log('There was an error: ' + authResult['error']);
        } else {
          $('#result').html('Failed to make a server-side call. Check your configuration and console.');
        }
      },
      error: function(result) {
        console.log('There was an error: ' + result);
      }
    });
  }
}
