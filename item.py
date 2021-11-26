import json
from player import Player
import random

class Item:
	def __init__(self, name):
		self.properties = json.load(open(f'gameset/items/{name.replace(" ", "_")}.json'))
	def execute(self, owner):
		fullcommand = self.properties['execute']
		command = fullcommand[:fullcommand.find(':')]
		argument = fullcommand[fullcommand.find(':')+1:fullcommand.find(' ')]
		value = fullcommand[fullcommand.find(' ')+1:]
		if value[:value.find(':')] == 'random':
			value = random.randint(int(value[value.find(':')+1:value.find(',')]), int(value[value.find(',')+1:]))
		

		if command == 'add':
			owner.data[argument] += int(value)
		elif command == 'set':
			owner.data[argument] = value
		
		owner.save_data()



