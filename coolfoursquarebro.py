"""
CoolFoursquareBro twitter bot, replies to foursquare tweets by a specific user with 'cool story bro' responses.

Copyright (C) 2013 Barry O'Neill
Author: Barry O'Neill <barry@barryoneill.net>
URL: <https://github.com/barryoneill/CoolFoursquareBro>
For license information, see LICENSE.txt
"""
from __future__ import print_function, unicode_literals
import twitter
import logging
import shelve

required_config_keys = ['twitter_consumer_key', 'twitter_consumer_secret',
                        'twitter_access_token', 'twitter_access_token_secret',
                        'db', 'target_userid']


class CoolFoursquareBro(object):
    def __init__(self, config):
        """
        Dictionary containing configuration, see 'coolfoursquarebro-sample.yaml' for options
        """

        self.config = config

        if not config:
            raise ValueError('Required config parameter missing')

        # catch config errors early
        missing_keys = set(required_config_keys) - set(config.keys())
        if missing_keys:
            raise KeyError('Following config keys are missing: {}'.format(', '.join(missing_keys)))

        if not all(key in config for key in required_config_keys):
            raise KeyError('Invalid configuration, required keys: {}'.format(required_config_keys))

        self.log = logging.getLogger(__name__)

        self.twitter_api = twitter.Api(consumer_key=self.config['twitter_consumer_key'],
                                       consumer_secret=self.config['twitter_consumer_secret'],
                                       access_token_key=self.config['twitter_access_token'],
                                       access_token_secret=self.config['twitter_access_token_secret'])

    @staticmethod
    def __is_foursquare_tweet(tweet):
        """
        returns True if the supplied twitter.Status object is a foursquare tweet
        """

        # rather than pattern match the tweet text, I'm going to crudely search for 'foursquare' in the client info
        return 'foursquare' in tweet.source.lower()

    @staticmethod
    def __create_unique_token(tweet):
        """
        Given this app generally sends the same 'cool story bro' message, twitter will reject all but the first
        with a 187 'duplicate' status code. This method should return a token which (appended to the reply to the
        provided twitter.Status) will make it unique.

        This impl is a bit of a hack. I make list[10] of different unicode chars that generate space characters.
        and return a string where each digit in the id is mapped to the corresponding space.
        """

        spaces0to9 = ['\u0020', '\u00A0', '\u2000', '\u2001', '\u2002',
                      '\u2003', '\u2004', '\u2005', '\u2006', '\u2007']

        # other spaces that can be used if some clients start rendering displayable chars
        # '\u2008', '\u2009', '\u200A', '\u200B', '\u202F', '\u205F', '\u3000'

        number_str = str(tweet.id)

        token_chars = []
        for c in number_str:
            token_chars += spaces0to9[int(c)]

        return ''.join(token_chars)

    def __create_response_text(self, tweet):
        """
        generate the response text for the supplied twitter.Status
        """

        # default to 'cool story bro', or whatever the config says the default is
        resp_text = self.config.get('coolstory_responsedefault', 'cool story, bro')

        # override, if the user has mapped a keyword match to an alternate text
        if 'coolstory_responses' in self.config:
            responses = self.config['coolstory_responses']

            for (place, response) in responses.items():
                if place.lower() in tweet.text.lower():
                    resp_text = response
                    break

        # '@{handle} cool story bro {uniquetoken}'
        return u'@{} {} {}'.format(tweet.user.screen_name, resp_text, self.__create_unique_token(tweet))

    def cool_story_bro(self, dry_run=False):
        """
        Query the user's recent tweets, and if a foursquare tweet is found, reply to it.  Records the
        last seen tweet info in a file, so the next run doesn't repeat itself.
        Set dry_run=True to prevent sending of tweets (last seen tweet is still recorded & obeyed)
        """

        db_lastseen_key = 'LAST_SEEN_ID'.encode('ascii')  # 'shelf' module struggles with unicode

        db = shelve.open(self.config['db'], writeback=False)

        target_userid = self.config['target_userid']

        # pick up at the last tweet we saw. If none, start at the configured tweet.  If none, query max 20 back
        last_seen_id = db.get(db_lastseen_key, self.config.get('lastseen_startval', 0))

        self.log.debug('Querying tweets for user {} since ID {}'.format(target_userid, last_seen_id))

        tweets = self.twitter_api.GetUserTimeline(target_userid, count=10,
                                                  since_id=last_seen_id, include_rts=False,
                                                  trim_user=False, exclude_replies=True)

        if not tweets:
            self.log.info('No tweets since last check')

        else:

            self.log.debug('Processing {} candidate tweets'.format(len(tweets)))

            # ensure oldest to newest
            tweets.sort(key=lambda tweet: tweet.id, reverse=False)

            # persist the 'max' id before doing anything - better to miss out on a few opportunities to be clever
            # than to spam the user on repeat calls if something failed on a previous run.
            newest = tweets[-1]
            db[db_lastseen_key] = newest.id
            self.log.info('Marked tweet {} as the max ID, text:{}'.format(newest.id, newest.text))

            fs_tweets = [t for t in tweets if self.__is_foursquare_tweet(t)]

            if not fs_tweets:
                self.log.info('No foursquare tweets.')
            else:
                self.log.info('Got {} foursquare tweets!'.format(len(fs_tweets)))

                for fs_tweet in fs_tweets:
                    resp_txt = self.__create_response_text(fs_tweet)

                    log_msg = 'text:\'{}\' in response to id:{} msg:\'{}\''.format(resp_txt, fs_tweet.id, fs_tweet.text)

                    if dry_run:
                        self.log.info('[dry run, no tweet sent]{}'.format(log_msg))
                    else:
                        self.log.warn('[sending tweet]{}'.format(log_msg))
                        resp_tweet = self.twitter_api.PostUpdate(resp_txt, in_reply_to_status_id=fs_tweet.id)
                        self.log.debug("tweet sent, id: {}".format(resp_tweet.id))
