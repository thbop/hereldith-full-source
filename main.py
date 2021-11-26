from player import Player
from monster import Monster
from item import Item
from map import Map
from shop import Shop
import os
from sys import platform
import json
from time import sleep
import random
import keyboard



if platform == "linux" or platform == "linux2":
    clear = 'clear'
elif platform == "darwin":
    print('Mac OS currently isn\'t supported.')
    input()
    quit()
elif platform == "win32":
    clear = 'cls'

# map_ = Map()
# player = Player('OramI')

def travel(player, current, to):
	roads = map_.get_town(current)['roads']
	if to in roads.keys():
		danger = map_.get_town(current)['roads'][to]['danger']
		if not random.randint(0, danger) == danger:
			return Monster('rentity', random.choice(json.load(open('gameset/characters.json'))['CPU']), skill=random.randint(0, danger), health=1)#random.randint(0, danger)
		else:
			player.data['location'] = to
			player.save_data()
			return 'clear'

	else:
		return 'error'

# travel = travel(player, player.data['location'], 'Elthresdorr')
# print(travel)
# if travel == 'clear' or travel == 'error':
# 	pass
# else:
# 	print('Fight time')





# player = Player('OramI', 'Wizard', location='Elthresdorr')

# i = 'Long Stick'
# if player.use_item(i):
# 	print('used')
# 	Item(i).execute(player)


# troll = Monster('Troll','Troll')
# goblin = Monster('Goblin', 'Goblin')

# player.attack(troll)

# map_ = Map()

# print(map_.get_shop('Elthresdorr', 'Knives'))


# player.save_data()
# troll.save_data()
# goblin.save_data()

keyboard.press_and_release('F11')
os.system(clear)
print(open('gui/splash.txt').read())
sleep(4)
os.system(clear)

mmm = ''


while True:
	print(open('gui/title.txt').read())
	print('Welcome to Hereldith!')
	menu = input(f'Type "load" to load a current character.\nType "new" to create a new character.{mmm}\n')
	if menu == 'new':
		while True:
			name = input('What is your character\'s name? ')
			if not name.lower()+'.json' in os.listdir('data/'):
				break
			else:
				print('That character already exists!')

		characters = json.load(open('gameset/characters.json'))['player']
		print('Classes:')
		for char in characters:
			print(f'\t{char}')

		while True:
			typ = input(f'What is {name}\'s class? ')
			if typ in characters:
				break
			else:
				print('Not a class, silly!')
		player = Player(name, typ, location=list(json.load(open('gameset/map/map.json'))['towns'].keys())[0])
		player.save_data()
		break
	elif menu == 'load':
		if os.listdir('data/') == []:
			mmm = '\nYou don\'t have any characters!'
			os.system(clear)
		else:
			characters = json.load(open('gameset/characters.json'))['player']
			my_char = []
			print('Characters:')
			for char in os.listdir('data/'):
				if json.load(open(f'data/{char}'))['type'] in characters:
					print(f'\t{json.load(open(f"data/{char}"))["name"]}')
					my_char.append(json.load(open(f"data/{char}"))["name"])
			while True:
				name = input('What\'s the character do you want to play as?\n')
				if name in my_char:
					player = Player(name)
					break
				else:
					print('That\'s not one of your characters!')
			break
	elif menu == 'quit':
		os.system(clear)
		quit()
	else:
		mmm = '\nThat\'s not a command, silly!'
		os.system(clear)

map_ = Map()

os.system(clear)




mmm = ''
while True:
	os.system(clear)

	roads = ''
	for road in map_.get_town(player.data["location"])['roads'].keys(): roads+='\n\t\t'+road
	shops = ''
	for shop in map_.get_town(player.data["location"])['shops'].keys(): shops+='\n\t\t'+shop
	if shops == '':
		shops = ' No shops here.'
	inv = ''
	items = list(player.data['inventory'].keys())
	for item in items:
		inv += f'\n\t{item}: {player.data["inventory"][item]["amount"]}'
	if inv == '':
		inv = ' Nothing here.'

	info = f'''[INFO]:
\tName: {player.data["name"]}
\tHealth: {player.data["health"]}
\tSkill: {player.data["skill"]}
\tMoney: {player.data["money"]}
[TOWN]:
\tName: {player.data["location"]}
\tRoads:{roads}
\tShops:{shops}
[INVENTORY]:{inv}{mmm}'''

	print(open('gui/title_small.txt').read())
	print(info)

	ui = input()

	if ui == 'quit':
		player.save_data()
		os.system(clear)
		quit()

	elif ui[:ui.find(' ')] == 'use':
		i = ui[ui.find(' ')+1:]
		if player.use_item(i):
			Item(i).execute(player)
		player.save_data()

	elif ui[:ui.find(' ')] == 'shop':
		if ui[ui.find(' ')+1:] in map_.get_town(player.data['location'])['shops'].keys():
			shop = Shop(player.data['location'], ui[ui.find(' ')+1:])
			
			shopinv = ''
			for ware in shop.shop['wares'].keys(): shopinv += f'\n\t{ware} - price: {shop.shop["wares"][ware]["price"]}'
			shopwaregui = f'[SHOP WARES]:{shopinv}'

			print(f'{shop.shop["owner"]}: Hello! Welcome to my shop, {shop.shop["name"]}! {shop.shop["description"]}\n')
			while True:
				ui = input(f'{shop.shop["owner"]}: How may I help you? ')
				if ui == 'leave':
					mmm = f'\n{shop.shop["owner"]}: Good bye!'
					break
				elif ui == 'buy':
					print(shopwaregui)

					ui = input(f'\n{shop.shop["owner"]}: What do you want to buy? ')
					if ui == 'nothing':
						print(f'{shop.shop["owner"]}: Ok.')
					else:
						print(f'{shop.shop["owner"]}: {shop.buy(player, ui)}')
				elif ui == 'sell':
					print(shopwaregui)
					
					ui = input(f'\n{shop.shop["owner"]}: What do you want to sell? ')
					if ui == 'nothing':
						print(f'{shop.shop["owner"]}: Ok.')
					else:
						print(f'{shop.shop["owner"]}: {shop.sell(player, ui)}')
				else:
					print(f'{shop.shop["owner"]}: You can "buy" things, "sell" things, or you may "leave".')
			player.save_data()

	traveling = {'bool':False,'to':None}

	if ui == 'travel':
		print('PRO TIP: Try using travel with the syntax:\ntravel <place>\n')
		ui = input('Where to? ')
		traveling['bool'] = True
		traveling['to'] = ui
	elif ui[:ui.find(' ')] == 'travel':
		traveling['bool'] = True
		traveling['to'] = ui[ui.find(' ')+1:]
	if traveling['bool']:
		Travel = travel(player, player.data['location'], traveling['to'])
		# print(travel)
		if str(Travel) == 'clear':
			mmm = f'\nTraveled to {traveling["to"]} safely.'
		elif str(Travel) == 'error':
			mmm = f'\n"{traveling["to"]}" either does\'t exist, or you don\'t have a road that leads there.'
		else:
			print(f'You have crossed paths with an angry {Travel.data["type"]}!')
			ui = input(f'Would you like to fight the {Travel.data["type"]}, or would you want to turn back to {player.data["location"]}?\n("turn back" or "fight")\n')
			if ui.lower() == 'turn back':
				pass
			else:
				result = player.attack(Travel)
				if Travel.data['health'] == None:
					mmm = '\nYou\'ve slain that villan!'
					player.data['location'] = traveling['to']

				elif player.data['health'] <= 0:
					mmm = '\nYou died!\nRespawning...'
					playername = player.data["name"]
					typ = player.data['type']
					os.remove(f'data/{player.data["name"].lower()}.json')
					player = Player(playername, typ, location=list(json.load(open('gameset/map/map.json'))['towns'].keys())[0])
				else:
					mmm = '\n'+result
					player.data['location'] = traveling['to']

				player.save_data()




	
