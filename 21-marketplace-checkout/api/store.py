from copy import deepcopy
import threading
_products = {"p1":{"id":"p1","name":"Keyboard","price":100,"stock":2},"p2":{"id":"p2","name":"Mouse","price":25,"stock":10}}
_carts = {"alice":[]}; _orders = {}; _keys = {}; _lock = threading.Lock()
def reset():
    global _products,_carts,_orders,_keys
    _products={"p1":{"id":"p1","name":"Keyboard","price":100,"stock":2},"p2":{"id":"p2","name":"Mouse","price":25,"stock":10}}; _carts={"alice":[]}; _orders={}; _keys={}
def products(): return deepcopy(list(_products.values()))
def cart(user): return deepcopy(_carts.setdefault(user, []))
def add(user,pid,qty):
    if pid not in _products: return None
    for line in _carts.setdefault(user,[]):
        if line["product_id"]==pid: line["quantity"]+=qty; return cart(user)
    _carts[user].append({"product_id":pid,"quantity":qty}); return cart(user)
def checkout(user,coupon,key):
    if key in _keys: return deepcopy(_orders[_keys[key]])
    lines=cart(user)
    if not lines: return None
    total=0
    for line in lines:
        p=_products[line["product_id"]]
        if p["stock"]<line["quantity"]: return "stock"
        total += p["price"]*line["quantity"]
    if coupon=="SAVE10": total=round(total*.1,2)
    with _lock:
        for line in lines: _products[line["product_id"]]["stock"]-=line["quantity"]
        oid=f"o{len(_orders)+1}"; order={"id":oid,"user":user,"items":lines,"total":total,"status":"paid"}; _orders[oid]=order; _carts[user]=[]
    return deepcopy(order)
def order(oid): return deepcopy(_orders.get(oid))
