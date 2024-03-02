from DB import DB
from API import MMOc

'''
Sam Jeffery

Big Data Programming Assignment

02/27/2024

This program aims to fulfill the spec given to me by the professor.

 First, we must pull data from an API, which is done in the API.py file in the API class.

 Next, we must push all that data to the RedisJSON database. This is done in the DB.py file, using the sendData method.

 After that, produce three outputs:

 Output #1 -> getGenres -> Count the total number of genres for each game present in the database. Produce a basic bar graph with counts.
 
 For the next two outputs, we are using searching and querying. To do so, we first create two indexes.

 Output #2 -> findDevs -> Queries the database to find games that are made by the specific developer "Blizzard Entertainment." Returns the list of games.

 Output #3 -> findFree -> Queries the database to find games that contain the word 'free' in their description. Returns the list of games.

'''



#DB init
m = MMOc()
gamesDB = DB()

#clear DB for integrity
gamesDB.clear()



# DB Functions
gamesDB.sendData(m.getGames())
gamesDB.drop_index()
gamesDB.create_search_index()
gamesDB.findFree()
gamesDB.findDevs()
gamesDB.getGenres()