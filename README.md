# theShops
CRUD demo site with RESTful API for a fake shopping mall

**API Guide:**
All requests return data formatted in JSON.

http://www.peterb.space/theshops/shops
returns a list of all shops and their associated meta data

http://www.peterb.space/theshops/products
returns a list of all products and their associated meta data

http://www.peterb.space/theshops/shop/(shop id)- integer
ie,
http://www.peterb.space/theshops/shop/2
returns a list of products sold at a specific shop,

http://www.peterb.space/theshops/product/(product id)- integer
ie,
http://www.peterb.space/theshops/product/2
returns a single product
