from pymongo import MongoClient
import assignment1
import sys, os


# Initialize Mongodb client
client = MongoClient()	# Initialize client in localhost
db = client.twitter_db

# Collect twitter data
def twitter_mongo():
		# Clear current information Collection
	info = db.information
	info.delete_many({})
	data_collection = db.data
	data_collection.delete_many({})

	dictionary = {}

	# Getting access information
	consumer_key = "*"
	consumer_secret = "*"
	access_token = "*-ZtCaU3ofNCNZg3tDe21MOAPo7A2IeBe"
	access_secret = "*"

	dictionary['keys'] = [consumer_key, consumer_secret, access_token, access_secret]

	# Getting study information
	number_tweets = input('Please enter number of tweets to analyze\n')
	handles = input('Please enter twitter handles separated by spaces\n')
	handles = handles.split(' ')

	dictionary['study'] = [number_tweets, handles]
	dictionary['data'] = []

	info.insert(dictionary)
	for t in info.find():
		print(t)
	return 0
	handles = db.information.find({})
	info = db.information

	for h in handles:
		number_tweets = h['study'][0]
		twitter_names = h['study'][1]

	data = []

	# Surpress output
	old_stdout = sys.stdout
	old_stderr = sys.stderr
	sys.stdout = os.devnull
	sys.stderr = os.devnull

	# Gathering twitter data
	for name in twitter_names:
		data.append(hw1_api.get_all_tweets(name, int(number_tweets)))

	print(data)
	# Updating twitter_db in mongo
	data_collection = db.data
	# Format data
	final = {}
	index = 0
	for name in twitter_names:
		final[name] = data[index]

	data_collection.insert(final)

	# Restoring standard output
	sys.stdout = old_stdout
	sys.stderr = old_stderr

	return 0


if __name__ == '__main__':	
	data = twitter_mongo()
	