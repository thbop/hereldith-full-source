import json
from map import Map

class Shop:
	def __init__(self, town, shop):
		self.map = Map()
		self.shop = self.map.get_shop(town, shop)

	def buy(self, player, item):
		if item in self.shop['wares'].keys():
			if player.data['money']-self.shop['wares'][item]['price'] < 0:
				return 'Cannot buy this item, not enough money!'
			else:
				player.data['money'] -= self.shop['wares'][item]['price']
				player.give_item(item)
				player.save_data()
				return 'Enjoy that!'
		else:
			return f'I don\'t have a "{item}"'
	def sell(self, player, item):
		if item in self.shop['wares'].keys():
			if player.use_item(item):
				player.data['money'] += self.shop['wares'][item]['price']
				player.save_data()
				return f'Here\'s {self.shop["wares"][item]["price"]} coins.'
			else:
				return f'You don\'t have a "{item}"'
		else:
			return f'Sorry, I don\'t know the price of {item}s.'



