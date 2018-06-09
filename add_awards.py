#! /usr/bin/env python
# -*- coding: utf-8 -*-
import csv
from app import db
from app.models import Task

all_spheres = ['karate_type',
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
arr = []
list = {}
cont = ''
copy_cont = ''
i = 0
j = 0
cur_sphere = ''
last_title = ''
with open('awards.csv', 'r') as file:
	line = csv.DictReader(file)
	for row in line:
		title = row['Название группы (достижения)']
		if (title != '') | (row['сфера'] != ''):
			if(( i != 0) & (cont != '') & (last_title != '')):
				list[i-1] = {'task_type' : cur_sphere, 'container' : cont, 'title' : last_title}
			last_title = title
			i += 1
			copy_cont = cont
			cont = ''


		if row['Суть ачивки'] != '':
			cont += row['Суть ачивки'] + '/'
		if(row['сфера'] != ''):
			cur_sphere = all_spheres[j]
			j += 1

for val in list:
	try:
		print(list[val]['title'])
		t = Task(title=list[val]['title'], container=list[val]['container'], task_type=list[val]['task_type'], price=0)
		db.session.add(t)
		db.session.commit()
	except:
		print('error ' + str(val))

t = Task(title=last_title, container=copy_cont, task_type=cur_sphere, price=0)
db.session.add(t)
db.session.commit()