
from requests import Session


''' 
MMOc

MMO API object class

'''
class MMOc:

	def __init__(self):

		'''
		init

		Connects to the API URL using a session through the requests library.

		'''

		self.apiurl =  'https://www.mmobomb.com/api1/'
		self.session = Session()

	def getGames(self):
		'''
		Gets all PC platform games from the API, and closes the session.

		Returns a full list of JSON objects.

		'''
		url = self.apiurl + '/games?platform=pc'
		r = self.session.get(url)
		# Was following the tutorial and was trying pretty print. too many entries to print though!
		#pp(r.json())
		data = r.json()
		self.session.close()
		return data

