# CoolFoursquareBro #

This is a python twitter bot, written in Python, inspired by the following tweet by the ever-amusing [@iamdevloper](https://twitter.com/iamdevloper]) : 

[![@iamdevloper](http://barryoneill.net/coolfoursquarebro_tweetref.png)](https://twitter.com/iamdevloper/statuses/400696778196275200)

This module queries the target user's recent tweets, and if any are determined to be foursquare 
noise, they get responded to in the manner above (the messages are configurable!)

### Disclaimer ###

I wrote this script to get a bit more python practice, and also to have a bit of fun with a friend 
who's a foursquare fan  (and has a good sense of humour).  It's up to you to make sure that you
**don't use this script in a spammy/harassing way, and in a way that obeys 
[Twitter's T&C](https://dev.twitter.com/terms/api-terms)**. :hear_no_evil:   


### Requirements ###

* Python 2.5 to 2.7 (the python-twitter module isn't fully Python 3 ready yet) 
* The [python-twitter](https://github.com/bear/python-twitter) module which has its own dependencies:
	* [SimpleJson](http://cheeseshop.python.org/pypi/simplejson), [Requests OAuthlib](https://requests-oauthlib.readthedocs.org/en/latest/), [HTTPLib2](http://code.google.com/p/httplib2/), [Requests](http://docs.python-requests.org/en/latest/)
* If you wish to use the provided **runner.py** script, you'll also need [PyYAML](http://pyyaml.org/).
* If you don't already have one, you'll need to setup your twitter developer account.  
	* Sign into the [developer apps dashboard](https://dev.twitter.com/apps) with the bot's twitter account.  
	* Create a new 'Application'.  Under the **Settings** tab, make sure the *Application Type* is 'Read and Write'.  
  	* Back in the **Details** tab, click the **Create My Access Token** button.  You'll need the values on
  	  this page for your configuration (below). 



### Usage ###

```python

	from coolfoursquarebro import CoolFoursquareBro

    conf = {
        # [required] taken from your twitter developer app page
        'twitter_consumer_key': 'abcde12345abcde12345',
        'twitter_consumer_secret': 'abcde12345abcde12345abcde12345abcde12345',
        'twitter_access_token': 'abcde12345abcde12345abcde12345abcde12345abcde12345',
        'twitter_access_token_secret': 'abcde12345abcde12345abcde12345abcde12345abcde123',

        # [required] stores the last seen tweet info (created on first run)
        'db': '/tmp/file.db',

        # [required] the victim's twitter id (use http://gettwitterid.com/ to look up)
        'target_userid': 12345678,

        # [optional] useful for first run/testing, prevents responses to tweets older than this id
        # 'lastseen_startval': 0,

        # [optional] default response text text
        'coolstory_responsedefault': 'cool story, bro',

        # [optional] if the tweet text contains one of these keys, the value will be used instead
        'coolstory_responses': {
            'McDonald\'s': 'cool diet, bro',
            'deli': 'cool sandwich, bro'
        }
    }


	....
	
    bot = coolfoursquarebro.CoolFoursquareBro(conf)
	
    bot.cool_story_bro()  # supply dry_run=True for testing
}

```

### Scheduling the Bot ###

While the above could be shoved in a *while*/*sleep* loop, I also wrote **runner.py** to run the
bot from a cron job, reading the config from a file and doing propriate logging. 

Here's a sample cron entry to run the bot every 2 minutes (watch out for 
[Twitter's rate limiting rules](https://dev.twitter.com/docs/rate-limiting/1.1)!):

	*/2 * * * * /usr/bin/python /path/to/runner.py >> /path/to/runner.log 2>&1
	
It will look for a file called **coolfoursquarebro.yaml** in your home directory, 
but you could also use the **-c /path/to/config.yaml** argument.   The configuration is the same,
as the above, except it's in yaml format:

	# [required] taken from your twitter developer app page
	twitter_consumer_key: abcde12345abcde12345
	twitter_consumer_secret: abcde12345abcde12345abcde12345abcde12345
	twitter_access_token: abcde12345abcde12345abcde12345abcde12345abcde12345
	twitter_access_token_secret: abcde12345abcde12345abcde12345abcde12345abcde123
	
	# [required] stores the last seen tweet info (created on first run)
	db: /tmp/file.db
	
	# [required] the victim's twitter id (use http://gettwitterid.com/ to look up)
	target_userid: 12345678
	
	# [optional] useful on the first run, prevents responses to tweets older than this id
	# lastseen_startval: 0
	
	# [optional] default response text text
	coolstory_responsedefault: cool story, bro
	
	# [optional] if the tweet text contains one of these keys, the value will be used instead
	coolstory_responses:
	  McDonald\'s: cool diet, bro
	  deli: cool sandwich, bro
	

### License ###
	
	
	Licensed under the Apache License, Version 2.0 (the 'License');
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at
	
	    http://www.apache.org/licenses/LICENSE-2.0
	
	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an 'AS IS' BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.







