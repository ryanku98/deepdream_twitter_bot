import tweepy   # Twitter API Python wrapper
import os       # path.exists
import requests # get
import time     # sleep

a_key_path = "config/access_key.txt"
a_sec_path = "config/access_secret.txt"
c_key_path = "config/consumer_key.txt"
c_sec_path = "config/consumer_secret.txt"
last_tweet_id_path = "config/last_tweet_id.txt"
image_file_path = "image."
deepai_api_key_path = "config/deepai_api_key.txt"
deepdream_api_url = "https://api.deepai.org/api/deepdream"
microsoft_image_description_api_url = "https://microsoft-azure-microsoft-computer-vision-v1.p.rapidapi.com/describe"
my_username = "deepdreamrepost"
tweet_count = 0
error_count = 0
api_retries = 3

def repost():
    # access Twitter keys/tokens
    a_key_file = open(a_key_path, "r")
    a_sec_file = open(a_sec_path, "r")
    c_key_file = open(c_key_path, "r")
    c_sec_file = open(c_sec_path, "r")
    a_key = a_key_file.read()
    a_sec = a_sec_file.read()
    c_key = c_key_file.read()
    c_sec = c_sec_file.read()
    a_key_file.close()
    a_sec_file.close()
    c_key_file.close()
    c_sec_file.close()
    
    # Twitter authentication
    auth = tweepy.OAuthHandler(c_key, c_sec)
    auth.set_access_token(a_key, a_sec)
    api = tweepy.API(auth)
    
    if os.path.exists(last_tweet_id_path):
        # read last tweet ID
        last_tweet_id_file = open(last_tweet_id_path, "r")
        last_tweet_id = last_tweet_id_file.read()
        last_tweet_id_file.close()
        if not last_tweet_id:
            # if empty file
            last_tweet_id = 1
        my_mentions = api.mentions_timeline(last_tweet_id, tweet_mode="extended")
    else:
        my_mentions = api.mentions_timeline(tweet_mode="extended")
    
    global tweet_count, error_count
    for mention in reversed(my_mentions):
        print("Found tweet " + get_tweet_url(mention.user.screen_name, mention.id))
        try:
            # tweets without media don't have the extended_entities attribute
            media_type = mention.extended_entities["media"][0]["type"]
        except:
            print("No media found")
            api.update_status(status="No media found - tweet me an image to see the Deep Dream generated version! If you believe this is an error, feel free to open an issue https://github.com/ryanku98/deepdream_twitter_bot/issues and link your tweet!", in_reply_to_status_id=mention.id, auto_populate_reply_metadata=True)
            set_last_tweet(mention.id)
            # update error counter
            error_count += 1
            # go to next mention
            continue

        if media_type == "video":
            print("Videos not supported")
            api.update_status(status="Videos not supported - tweet me an image instead! If you believe this is an error, feel free to open an issue https://github.com/ryanku98/deepdream_twitter_bot/issues and link your tweet!", in_reply_to_status_id=mention.id, auto_populate_reply_metadata=True)
            set_last_tweet(mention.id)
            # update error counter
            error_count += 1
        elif media_type == "photo":
            media_url = mention.extended_entities["media"][0]["media_url_https"]
            get_hashtags(mention.entities["hashtags"], media_url)
            filename = deepdream(media_url)
            # tweet deepdream photo
            t = api.update_with_media(filename, status="#deepdream " + get_hashtags(mention.entities["hashtags"], media_url))
            print("Generated " + get_tweet_url(my_username, t.id))
            # reply to original tweet with deepdream tweet
            api.update_status(status=get_tweet_url(my_username, t.id), in_reply_to_status_id=mention.id, auto_populate_reply_metadata=True)
            set_last_tweet(mention.id)
            # update counter
            tweet_count += 1
        
    delete_media()
    print_counters()
    return

# send image through deepdream API, return name of file in local storage
def deepdream(media_url):
    # set deepai metadata
    data = {"image": media_url}
    deepai_api_key_file = open(deepai_api_key_path, "r")
    headers = {"api-key": deepai_api_key_file.read()}
    deepai_api_key_file.close()
    
    # try deepai API
    for x in range(api_retries):
        r = requests.post(deepdream_api_url, data=data, headers=headers)
        if r.status_code != 200:
            print("ERROR: could not connect to Twitter")
            if x == api_retries - 1:
                print("ERROR: reached max retries, exiting...")
                exit()
            time.sleep(1.5)
            continue
        break
    
    # download image
    output_url = r.json()["output_url"]
    image = requests.get(output_url)
    filename = image_file_path + get_image_type(output_url)
    image_file = open(filename, "wb")
    image_file.write(image.content)
    image_file.close()
    
    return filename
    
def get_tweet_url(username, id):
    return "https://twitter.com/" + username + "/status/" + str(id)
    
def set_last_tweet(last_id):
    last_tweet_id_file = open(last_tweet_id_path, "w")
    last_tweet_id_file.write(str(last_id))
    last_tweet_id_file.close()
    return
    
# checks tail of link for image type, return as string to set appropriate file name
def get_image_type(link_str):
    index_of_period = link_str.rfind(".")
    return link_str[index_of_period+1 : ]
    
def get_hashtags(hash_dict, media_url):
    # first get original poster hashtags
    hash_set = set()
    for tag in hash_dict:
        hash_set.add(tag["text"])
    # set rapidapi metadata
    data = "{\"url\":\"" + media_url + "\"}"
    x_rapidapi_key_file = open("config/x_rapidapi_key.txt")
    headers = {
        "x-rapidapi-host": "microsoft-azure-microsoft-computer-vision-v1.p.rapidapi.com",
        "x-rapidapi-key": x_rapidapi_key_file.read(),
        "content-type": "application/json",
        "accept": "application/json"
    }
    x_rapidapi_key_file.close()
    # try rapidapi image recognition API
    for x in range(api_retries):
        r = requests.post(microsoft_image_description_api_url, data=data, headers=headers)
        if r.status_code != 200:
            print("ERROR: could not connect to Microsoft Azure Image Recognition API\nRetrying...")
            if x == api_retries - 1:
                print("ERROR: reached max retries, exiting...")
                exit()
            time.sleep(1.5)
            continue
        break
                
    # extract tags into set
    for tag in r.json()["description"]["tags"]:
        hash_set.add(tag)
        
    str = ""
    for tag in hash_set:
        str += "#" + tag + " "
    return str
    
def delete_media():
    if os.path.exists(image_file_path):
        os.remove(image_file_path)
        
def print_counters():
    print(str(tweet_count) + " tweets | " + str(error_count) + " errors")
    
if __name__ == "__main__":
    repost()