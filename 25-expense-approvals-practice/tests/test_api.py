import json
from tests.conftest import AUTH
def p(c,path,x,h=AUTH):return c.post(path,data=json.dumps(x),content_type='application/json',headers=h)
def test_auth(client):assert client.post('/expenses',data=b'{}',content_type='application/json').status_code==401
def test_idempotency(client):
 h={**AUTH,'Idempotency-Key':'x'};assert p(client,'/expenses',{'amount':10},h).json()==p(client,'/expenses',{'amount':10},h).json()
def test_invalid_amount(client):assert p(client,'/expenses',{'amount':0},{**AUTH,'Idempotency-Key':'a'}).status_code==400
def test_approve_and_total(client):
 e=p(client,'/expenses',{'amount':25},{**AUTH,'Idempotency-Key':'a'}).json();assert p(client,'/expenses/'+e['id']+'/decision',{'approved':True}).status_code==200;assert client.get('/expenses/total').json()['total']==25
def test_decision_is_one_way(client):
 e=p(client,'/expenses',{'amount':25},{**AUTH,'Idempotency-Key':'a'}).json();p(client,'/expenses/'+e['id']+'/decision',{'approved':True});assert p(client,'/expenses/'+e['id']+'/decision',{'approved':False}).status_code==409
def test_missing(client):assert client.get('/expenses/no').status_code==404
