import json
from tests.conftest import AUTH
def post(client,path,data,headers=None): return client.post(path,data=json.dumps(data),content_type="application/json",headers=headers or AUTH)
def test_mutations_require_auth(client): assert client.post("/cart",data=b"{}",content_type="application/json").status_code==401
def test_add_and_get_cart(client):
    assert post(client,"/cart",{"product_id":"p1","quantity":1}).status_code==200
    assert client.get("/cart").json()==[{"product_id":"p1","quantity":1}]
def test_missing_product(client): assert post(client,"/cart",{"product_id":"bad","quantity":1}).status_code==404
def test_checkout_discount_and_clears_cart(client):
    post(client,"/cart",{"product_id":"p1","quantity":1}); r=post(client,"/checkout",{"coupon":"SAVE10"},{**AUTH,"Idempotency-Key":"a"})
    assert r.status_code==201 and r.json()["total"]==90 and client.get("/cart").json()==[]
def test_checkout_idempotent(client):
    post(client,"/cart",{"product_id":"p2","quantity":1}); h={**AUTH,"Idempotency-Key":"same"}; a=post(client,"/checkout",{},h); b=post(client,"/checkout",{},h); assert a.json()==b.json()
def test_stock_failure_does_not_create_order(client):
    post(client,"/cart",{"product_id":"p1","quantity":3}); assert post(client,"/checkout",{}, {**AUTH,"Idempotency-Key":"x"}).status_code==409
def test_order_missing(client): assert client.get("/orders/nope").status_code==404
