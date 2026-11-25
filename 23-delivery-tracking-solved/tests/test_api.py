import json
from tests.conftest import AUTH
def p(c,path,x,h=AUTH):return c.post(path,data=json.dumps(x),content_type='application/json',headers=h)
def test_owner_required(client):assert client.get('/shipments/s1',headers={'X-User':'bob'}).status_code==403
def test_transition_order(client):
 for x in ('picked_up','in_transit','delivered'):assert p(client,'/shipments/s1/status',{'status':x}).status_code==200
def test_skip_transition_rejected(client):assert p(client,'/shipments/s1/status',{'status':'delivered'}).status_code==409
def test_webhook_idempotent(client):
 h={**AUTH,'Event-Id':'e1'};a=p(client,'/shipments/s1/webhook',{'status':'picked_up'},h);b=p(client,'/shipments/s1/webhook',{'status':'picked_up'},h);assert a.json()==b.json()
def test_missing(client):assert client.get('/shipments/no').status_code==404
def test_mutation_auth(client):assert client.post('/shipments/s1/status',data=b'{}',content_type='application/json').status_code==401
