import redis
import json
import matplotlib.pyplot as plt
from db_config import get_redis_connection
from pprint import pprint as pp

'''
DB.py

2/27/2024

Sam Jeffery

Database object class that holds operational functions and initiation.

'''
class DB:

	
	def __init__(self):

		'''
		init

		Establishes connection using db_config file

		'''
	
		self.conn = get_redis_connection()
	
	
	def sendData(self, data):
		''' 
		sendData
		in: list of JSON objects
		
		iterates through the json data and adds each object to the database, with their ID being the key.
		'''

		for i in data:
			game_id = i['id']
			id_str = str(game_id)
			obj_str = json.dumps(i)
			self.conn.execute_command('JSON.SET', f'games:{id_str}', '.', obj_str)
		

	def showData(self):

		'''
		showData -- NOT IN USE, WAS USED FOR TESTING

		Returns: all keys and their respective data.
		
		'''
		
		keys = self.conn.keys()
		for key in keys:
			try:
				data = self.conn.json().get(key)
				if data:
					decoded = json.loads(data)
					print(f"Key: {key}, \n Game Info:\n{json.dumps(decoded, indent=4)}\n")
				else:
					print(f"Key: {key} does not exist.")
			except json.JSONDecodeError:
				print(f"Error decoding JSON data for key: {key}")
			except redis.exceptions.RedisError as e:
				print(f"Error accessing key: {key} ({e})")

	

	def getSize(self):
		'''
		getSize -- NOT IN USE, WAS USED FOR TESTING.

		returns: number of keys in the database

		'''
		print("Total Size: ", (self.conn.dbsize()))

	def clear(self):
		'''
		clear

		clears all entries from the database

		Returns: success or the error message.
		
		'''
		try:
			self.conn.flushdb()
			print("Database cleared.")
		except redis.ResponseError as e:
			print("Error", e)
	
	def getGenres(self):

		'''
		getGenres -- OUTPUT #1

		Scan through each key and get its genre and add it to a dictionary with genre names and the number of apperances.

		returns: matlib bar graph plot that shows num. games 
		
		'''
		genres = {}
		for key in self.conn.scan_iter():
			json_data = self.conn.json().get(key, '.')
			genre = json_data.get('genre')

			if genre in genres:
				genres[genre] += 1
			else:
				genres[genre] = 1

		genre_keys = list(genres.keys())
		genre_values = list(genres.values())

		plt.bar(genre_keys, genre_values, color='green')
		plt.xlabel('Genre')
		plt.ylabel('Num. Games')
		plt.title('Number of Games per Genre')
		plt.xticks(rotation = 45, ha='right')
		plt.show()

	
	def create_search_index(self):

		''' 
		create_search_index

		Creates two search indexes, one for short_description and one for developer.

		Returns: error or successful statement.
		
		'''
		try:
			self.conn.execute_command('FT.CREATE idx:desc ON JSON PREFIX 1 games: SCHEMA $.short_description AS short_description TEXT')
			print(f"Description index created successfully.")
			self.conn.execute_command('FT.CREATE idx:dev ON JSON PREFIX 1 games: SCHEMA $.developer AS developer TEXT')
			print(f"Developer index created successfully.")
		except redis.exceptions.ResponseError as e:
			print(f"Erorr. ", e)

	
	def drop_index(self):
		'''
		drop_index

		Drops both indexes created by the above function.

		Returns: success or error.
		'''
		try:
			self.conn.execute_command('FT.DROPINDEX idx:desc')
			self.conn.execute_command('FT.DROPINDEX idx:dev')
			print("Indexes dropped")
		except redis.exceptions.ResponseError as e:
			print(f"Error", e)


	def findDevs(self):

		'''
		findDevs -- OUTPUT #2
		
		Uses the developer index to search for a specific developer, "Blizzard Entertainment."

		Returns: list of matching games.
		
		'''
		print("\n NOW FINDING BLIZZARD GAMES:\n")
		query = '@developer:Blizzard*'
		result = self.conn.execute_command('FT.SEARCH', 'idx:dev', query)
		pp(result)


	def findFree(self):
		'''
		findFree -- OUTPUT #3

		Uses the description index to search for the term "free" followed by a wildcard* to catch instances like 'free-to-play' or 'freetoplay'

		Returns: list of matching games.
		
		'''
		print("\n NOW FINDING FREE TO PLAY GAMES:\n")
		query = '@short_description:free*'
		result = self.conn.execute_command('FT.SEARCH', 'idx:desc', query)
		pp(result)
	

