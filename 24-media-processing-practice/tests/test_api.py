import json
from tests.conftest import AUTH
def p(c,path,x,h=AUTH):return c.post(path,data=json.dumps(x),content_type='application/json',headers=h)
def test_auth(client):assert client.post('/media/m1/process',data=b'{}',content_type='application/json').status_code==401
def test_owner(client):assert client.get('/media/m1',headers={'X-User':'bob'}).status_code==403
def test_retry_then_fail(client):
 assert p(client,'/media/m1/process',{'ok':False}).json()['status']=='queued';assert p(client,'/media/m1/process',{'ok':False}).json()['status']=='queued';assert p(client,'/media/m1/process',{'ok':False}).json()['status']=='failed'
def test_ready_url(client):assert p(client,'/media/m1/process',{'ok':True}).json()['url']=='https://cdn/m1'
def test_signed_url(client):assert client.get('/media/m1/signed-url').json()['expires_in']==60
def test_pagination(client):assert len(client.get('/media?limit=1').json()['items'])==1
