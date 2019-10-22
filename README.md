# [Deep Dream Twitter Bot](https://twitter.com/deepdreamrepost)
[![Generic badge](https://img.shields.io/badge/help-me-critical.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/idontknow-whatimdoing-ee00ee.svg)](https://shields.io/)

Tweet an image to [@deepdreamrepost](https://twitter.com/deepdreamrepost) to see the Deep Dream version!

### Local Installation ###
#### Dependencies ####
Install dependencies with pip:
```bash
pip3 install -r requirements.txt
```
Fill in the six [config files](https://github.com/ryanku98/deepdream_twitter_bot/tree/master/config) for your API keys and secrets.
Fill in [last_tweet_id.txt](https://github.com/ryanku98/deepdream_twitter_bot/blob/master/config/last_tweet_id.txt) an ID if known; If unknown, fill with 1 or leave blank.

Run a one-off tweeting process with
```bash
python3 bot.py
```
or have the bot check for mentions every minute with
```bash
python3 scheduler.py
```

Finally, please report any bugs [here](https://github.com/ryanku98/deepdream_twitter_bot/issues)!
### [Happy Tweeting!](https://twitter.com/) ###