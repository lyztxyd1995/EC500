import tweepy
from tweepy import OAuthHandler
import json
import wget
import os
import io

from google.cloud import vision
from google.cloud.vision import types

consumer_key = 'DFmJEyJHWEOsF6aJG2dR3nwNd'
consumer_secret = '5ZO9zQz285nHzyC5sN1tT60Y9imbW66pqJHtARO4cA2ZJoHIet'
access_token = '902865296595320832-Cu3uGmxAhpJ72Mk5YKus4hN8PDkbB6e'
access_secret = 'E7i8WMJ9N85927H2cs3Iu4OQJ6zUSDGjJKISbiMfHe6We'
GOOGLE_APPLICATION_CREDENTIALS="Around-809999446769.json"

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
 
# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
# User() is the data model for a user profil
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
# You need to do it for all the models you need
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

tweets = api.user_timeline(screen_name='miguelmalvarez',
                           count=200, include_rts=False,
                           exclude_replies=True)

last_id = tweets[-1].id
 
while (True):
    more_tweets = api.user_timeline(screen_name='osama_amaso',
                                count=200,
                                include_rts=False,
                                exclude_replies=True,
                                max_id=last_id-1)
# There are no more tweets
    if (len(more_tweets) == 0):
	    break
    else:
        last_id = more_tweets[-1].id-1
        tweets = tweets + more_tweets

media_files = set()
for status in tweets:
    media = status.entities.get('media', [])
    if(len(media) > 0):
        media_files.add(media[0]['media_url'])


for media_file in media_files:
    wget.download(media_file)

os.system('ffmpeg -framerate 1 -pattern_type glob -i "*.jpg"   -c:v libx264 -r 30 -pix_fmt yuv420p image2video.mp4')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/yizeliu/Desktop/Around-809999446769.json"

client = vision.ImageAnnotatorClient()

file = open('Label_Detection.txt', 'w')

file_name = os.path.join(
    os.path.dirname(__file__),
    'su.jpg')

ITEMS = os.listdir("./")

for image_file_name in ITEMS:
    if image_file_name.endswith(".jpg"):
        with io.open(image_file_name, 'rb') as image_file:
            content = image_file.read()
            image = types.Image(content=content)
            response = client.label_detection(image=image)
            file.write("Labels for " + image_file_name + " :\n")
            for label in response.label_annotations:
                file.write(label.description + " ")
            file.write("\n")