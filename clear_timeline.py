import tweepy
from bot import authorize_twitter, set_last_tweet_id, my_username

def wipe_timeline():
    """Simple function for wiping everything from a timeline (useful when dev testing)"""
    api = authorize_twitter()
    
    count = 0
    while True:
        my_timeline = api.user_timeline(my_username)
        
        if len(my_timeline) == 0:
            break   # exit if timeline is empty
        
        for tweet in my_timeline:
            api.destroy_status(tweet.id)
            print("Deleted tweet ID: " + str(tweet.id))
            count += 1
            
    # reset last_tweet_id
    set_last_tweet_id(1)
    
    print(str(count) + " tweets deleted!")
    return
    
if __name__ == "__main__":
    wipe_timeline()