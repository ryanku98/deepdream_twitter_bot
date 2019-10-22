# bot

## repost
```python
repost()
```
Checks 20 most recent @deepdreamrepost mentions and reposts deepdream versions of tweeted images
## authorize_twitter
```python
authorize_twitter()
```
Uses OAuth2 to get access to Twitter account
## get_last_tweet_id
```python
get_last_tweet_id()
```
Retrieves ID of most recently processed tweet
## set_last_tweet_id
```python
set_last_tweet_id(last_id)
```
Saves ID of the most recently processed tweet
## deepdream
```python
deepdream(media_url)
```
Sends an image through DeepAI's deepdream API and returns the locally saved file filename
## get_tweet_url
```python
get_tweet_url(username, id)
```
Returns tweet link or corresponding username and ID
## get_image_type
```python
get_image_type(link_str)
```
Returns the tail of link for appropriate media file extension
## get_hashtags
```python
get_hashtags(hash_dict, media_url)
```
Extracts hashtags from JSON hashtag dictionary and Azure image recognition API and returns the equivalent hashtag string
## delete_media
```python
delete_media()
```
Searches for all existing media files and deletes them
## print_counters
```python
print_counters(tweets, errors)
```
Prints tweet_count and error_count if either are greater than 0
