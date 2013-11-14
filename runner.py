"""
Runner script for CoolFoursquareBro

Copyright (C) 2013 Barry O'Neill
Author: Barry O'Neill <barry@barryoneill.net>
URL: <https://github.com/barryoneill/CoolFoursquareBro>
For license information, see LICENSE.txt
"""
from __future__ import print_function, unicode_literals
import os
import yaml
import argparse
import logging
from coolfoursquarebro import CoolFoursquareBro
from os.path import expanduser

DEFAULT_CONFIG = os.path.join(expanduser("~"), 'coolfoursquarebro.yaml')

if __name__ == '__main__':

    # default to ~/coolfoursquarebro-sample.yaml
    parser = argparse.ArgumentParser(description='CoolFoursquare Brotest')
    parser.add_argument('-c', dest='config', action='store', default=DEFAULT_CONFIG,
                        help='Path to config file, defaults to  \'{}\''.format(DEFAULT_CONFIG))
    args = parser.parse_args()

    # setup some console logging, everything is INFO, except for CoolFoursquareBro which is DEBUG
    logging.getLogger('').setLevel(logging.INFO)
    logger = logging.getLogger(CoolFoursquareBro.__module__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s](%(levelname)s) %(message)s'))
    logger.addHandler(handler)

    logger.info('--------------------- starting run ---------------------------')

    try:
        conf = yaml.load(open(args.config).read())

        bot = CoolFoursquareBro(conf)

        bot.cool_story_bro(dry_run=False)

    except Exception, e:

        logger.exception('Error {}'.format(e.message))

    logger.info('--------------------- finished run ---------------------------')