import json
from tests.conftest import AUTH
def p(c,path,x,h=AUTH):return c.post(path,data=json.dumps(x),content_type='application/json',headers=h)
def test_auth(client):assert client.post('/projects',data=b'{}',content_type='application/json').status_code==401
def test_create_project(client):assert p(client,'/projects',{'name':'X'}).status_code==201
def test_archive_hidden_by_default(client):p(client,'/projects/p1/archive',{});assert client.get('/projects').json()==[]
def test_task_and_optimistic_update(client):
 t=p(client,'/projects/p1/tasks',{'title':'a'}).json();r=client.patch('/tasks/'+t['id'],data=json.dumps({'title':'b','version':1}),content_type='application/json',headers=AUTH);assert r.json()['version']==2
def test_stale_version_conflicts(client):
 t=p(client,'/projects/p1/tasks',{'title':'a'}).json();client.patch('/tasks/'+t['id'],data=json.dumps({'title':'b','version':1}),content_type='application/json',headers=AUTH);assert client.patch('/tasks/'+t['id'],data=json.dumps({'title':'c','version':1}),content_type='application/json',headers=AUTH).status_code==409
def test_cursor_pages(client):
 p(client,'/projects/p1/tasks',{'title':'a'});p(client,'/projects/p1/tasks',{'title':'b'});assert len(client.get('/tasks?limit=1').json()['items'])==1
