import json
import random


class Player:
	"""Describes players and Monsters"""
	def __init__(self, name="entity", typ=None, skill=1, money=0, location=None, health=20):
		try: 
			self.data = json.load(open(f'data/{name.lower()}.json'))
		except FileNotFoundError:
			self.data = {
				"name":name,
				"type":typ,
				"skill":skill,
				"health":health,
				"inventory":{},
				"money":money,
				"location":location
				}
	def take_damage(self, amount):
		self.data['health'] -= amount

	def _test_if_killed(self, other):
		"""Tests if a player kills another and drops loot"""
		if other.data['health'] != None:
			if other.data['health'] <= 0:
				self.data['skill'] += 1
				other.data['health'] = None

				characters = json.load(open('gameset/characters.json'))
				if other.data['type'] in characters['player']:
					print(other.data['inventory'])
				elif other.data['type'] in characters['CPU']:
					loot_table = json.load(open(f'gameset/loot_tables/{other.data["type"]}.json'))
					item = loot_table[random.choice(list(loot_table.keys()))]
					if random.randint(1, item['roll']) == 1:
						self.give_item(item['item'], random.randint(1,item['amount']))

	def attack(self, other):
		"""Attacks other players or monsters, and drops their loot"""
		if other.data['health'] != None:
			if other.data['health'] <= 0:
				self._test_if_killed(other)

			else:
				if self.data['skill'] == other.data['skill']:
					BT = json.load(open('gameset/battle_table.json'))
					result = BT[self.data['type']][other.data['type']]
					if result == True:
						other.take_damage(self.data['skill'])
						self._test_if_killed(other)
						return 'You wounded that villan!'
					elif result == 'random':
						if random.randint(0, 1) == 1:
							other.take_damage(self.data['skill'])
							self._test_if_killed(other)
							return 'You wounded that villan!'
							
						else:
							self.take_damage(other.data['skill'])
							return 'Ouch! That hurts!'
					else:
						self.take_damage(other.data['skill'])
						return 'Ouch! That hurts!'
				elif self.data['skill'] < other.data['skill']:
					self.take_damage(other.data['skill'])
					return 'Ouch! That hurts!'
				else:
					other.take_damage(self.data['skill'])
					self._test_if_killed(other)
					return 'You wounded that villan!'
	def use_item(self, item):
		"""Returns True if that player has an item.
		When it returns True it also removes the 
		item from the player's inventory."""
		canUse = False
		try:
			if self.data['inventory'][item] != None:
				canUse = True
				if self.data['inventory'][item]['amount'] == 1:
					del self.data['inventory'][item]
				else:
					self.data['inventory'][item]['amount']-=1
		except:
			pass
		return canUse

	def give_item(self, item, count=1):
		try:
			if self.data['inventory'][item] != None:
				self.data['inventory'][item]['amount'] += count
		except:
			self.data['inventory'][item] = {'amount':count}


	def save_data(self):
		"""Saves player's data to a file"""
		with open(f'data/{self.data["name"].lower()}.json', 'w') as file_object:
			json.dump(self.data, file_object)

	