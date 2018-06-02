import json
from app import app
from app.models import Task

def getTasks(type):
	types = ['karate', 'capActivity']
	if type not in types:
		return "error"
	list = {}
	tasks = Task.query.filter_by(task_type=type)
	i = 1
	for t in tasks:
		list[i] = {'title' : t.title}
	list[0] = str(i)
	json_data = json.dumps(list)
	return list

