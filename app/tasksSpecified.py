import json
from app import app
from app.models import Task

def getTasks(type):
	types = ['karate_type',
				'creation_type',
				'learning_type',
				'network_type',
				'events_type',
				'mindClub_type',
				'business_type',
				'lifeStyle_type',
				'else_type',
				'collective_type',
				'improving_type']
	if type not in types:
		return "error"
	list = {}
	tasks = Task.query.filter_by(task_type=type)
	i = 1
	for t in tasks:
		list[i] = {'task_type' : t.task_type, 'container' : t.container, 'title' : t.title, 'price' : t.price}
		i += 1
	list[0] = str(i)
	json_data = json.dumps(list)
	return list

