import json

class Map:
	def __init__(self):
		self.map = json.load(open('gameset/map/map.json'))
	def get_town(self, town):
		try:
			return self.map['towns'][town]
		except:
			print(f'{town} doesn\'t exist!')
	def get_shop(self, town, shop):
		try:
			return json.load(open(f'gameset/map/{town.lower()}/{self.get_town(town)["shops"][shop]}'))

		except:
			print(f'Town: {town}, or shop: {shop} do not exist!')