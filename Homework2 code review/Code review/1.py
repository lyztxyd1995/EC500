import sys
import io
import tweepy
import json
import wget
import subprocess
import glob
import google.cloud.vision #import types


#Twitter API credentials
consumer_key = 'DFmJEyJHWEOsF6aJG2dR3nwNd'
consumer_secret = '5ZO9zQz285nHzyC5sN1tT60Y9imbW66pqJHtARO4cA2ZJoHIet'
access_key = '902865296595320832-Cu3uGmxAhpJ72Mk5YKus4hN8PDkbB6e'
access_secret = 'E7i8WMJ9N85927H2cs3Iu4OQJ6zUSDGjJKISbiMfHe6We'
GOOGLE_APPLICATION_CREDENTIALS="Alzheimer's-683341b411e6.json"



def get_tweets2vid(screen_name = "@Twitter", number_tweets = 10, rate = 2):
	# max number of possible tweets is 3240
	if number_tweets > 100 or number_tweets < 1:
		# print "Count is invalid: use a count between 1 and 100"
		return None
	elif not screen_name[0] == '@':
		# print "Enter valid Twitter Handle. Example: '@Twitter'"
		return None
	elif rate > 20 or rate < 0:
		# print "Try another rate"
		return None
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	# list of tweets
	tweets = []
	pictures = 0
	media_files = set()
	validuser = api.user_timeline(screen_name = screen_name, count = 1)
	if len(validuser) == 0:
		# print "This user does not exist or has no tweets."
		return None

	oldest = validuser[0].id - 1


	#iterate through tweets
	while pictures < number_tweets:
		new_tweets = api.user_timeline(screen_name = screen_name, count = number_tweets, max_id = oldest)

		#filter through recent tweets
		for newtweet in new_tweets:
			try:
				media = newtweet.entities.get('media',[])
				if (len(media) > 0):
					media_files.add(media[0]['media_url'])
					pictures += 1
			except (RuntimeError, TypeError,NameError):
				pass
			else:
				continue
		if len(new_tweets) > 1:
			oldest = new_tweets[-1].id - 1


	i = 0
	f = open('tweet_urls.txt','w')
	for media_file in media_files:
		wget.download(media_file, 'image'+str(i+1)+'.jpg')
		f.write(media_file)
		i+=1
	try: 
		# print "I'm here"
		#ffmpeg_process = "./ffmpeg -y -framerate 20 -i image%d.jpg outputvideo.mp4"
		# os.system('ffmpeg -framerate 1 -pattern_type glob -i "*.jpg"   -c:v libx264 -r 30 -pix_fmt yuv420p image2video.mp4')
		ffmpeg_command = ["ffmpeg", "-y","-framerate","20","-i","image%d.jpg","outputvid.mp4"] 
		subprocess.call(ffmpeg_command)
	except (RuntimeError, TypeError,NameError):
		# print "Could not create video for ffmpeg issues"
		pass
	else:
		print("")
		
	#ffmpeg -y -framerate 20 -i image%2d.jpg outputvideo.mp4


	return media_files 


def googlelabels(description_count = 2):
	# Instantiate client
	client = google.cloud.vision.ImageAnnotatorClient()

	outputdesc = {}

	for filename in glob.glob('*.jpg'):
		image_file_name = filename
		with io.open(image_file_name, 'rb') as image_file:
			content = image_file.read()

		# Use Vision to label the image based on content.
		image = google.cloud.vision.types.Image(content=content)
		response = client.label_detection(image=image)

		image_desc = []
		for label in response.label_annotations:
			if len(image_desc) < description_count:
				features = {}
				features['mid'] = label.mid
				features['description'] = label.description 
				features['score'] = str(label.score)
				features['topicality'] = str(label.topicality)
				image_desc.append(features)
			else:
				break
		if len(image_desc) == None:
			print ("There are no labels available")
		else:
			outputdesc[filename] = image_desc
	with open('labels.json','w') as outfile:
		json.dump(outputdesc, outfile, indent = 4, sort_keys = True)

	return outfile




if len(sys.argv) >= 1:
	if len(sys.argv) > 5:
		print('1')
	if len(sys.argv) == 5:
		screen_name = sys.argv[1]
		number_tweets = sys.argv[2]
		rate = sys.argv[3]
		description_count = sys.argv[4]
		urls = get_tweets2vid(screen_name, number_tweets, rate)
		goog = googlelabels(description_count)
	elif len(sys.argv) == 4:
		screen_name = sys.argv[1]
		number_tweets = sys.argv[2]
		rate = sys.argv[3]
		urls = get_tweets2vid(screen_name, number_tweets, rate)
		goog = googlelabels()
	elif len(sys.argv) == 3:
		screen_name = sys.argv[1]
		number_tweets = sys.argv[2]
		urls = get_tweets2vid(screen_name, number_tweets)
		goog = googlelabels()
	elif len(sys.argv) == 2:
		screen_name = sys.argv[1]
		urls = get_tweets2vid(screen_name)
		goog = googlelabels()
	elif len(sys.argv) == 1:
		urls = get_tweets2vid()
		goog = googlelabels()