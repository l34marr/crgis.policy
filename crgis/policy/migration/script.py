#!/usr/bin/env python
# -*- coding: utf-8 -*-

## User Config
cfgFile = 'config.cfg'
storageFile = '.storage'


## Do Not Edit Below This Line
## Unless You Know What's Doing
import datetime
import logging
import logging.handlers
import logging.config
import requests

from requests.auth import HTTPBasicAuth

from optparse import OptionParser
from sys import argv
from os.path import abspath, dirname

from ConfigParser import SafeConfigParser


## Script Run Options
parser = OptionParser()
parser.add_option('-a', '--all', dest='all',
                  action='store_true', default=False,
                  help="Full migration")

options, args = parser.parse_args()

## Config Parser Settings
storage = SafeConfigParser()
storage.read(storageFile)

cfgParser = SafeConfigParser()
cfgParser.read(cfgFile)

## Logger Settings
log_file = cfgParser.get('logging', 'log_file')
f = logging.Formatter(fmt='%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
                      datefmt="%Y-%m-%d %H:%M:%S")
handlers = [
    logging.handlers.RotatingFileHandler(log_file, encoding='utf8',
                                         maxBytes=100000, backupCount=1),
    logging.StreamHandler()
]
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
for h in handlers:
    h.setFormatter(f)
    h.setLevel(logging.DEBUG)

#logging.basicConfig(filename=log_file, level=logging.DEBUG)

## Script Settings
mazu_site_url = cfgParser.get('mazu_site_config', 'site_url')
mazu_migration_view_name = cfgParser.get(
    'mazu_site_config', 'migration_view_name')
mazu_login = cfgParser.get('mazu_site_config', 'login')
mazu_password = cfgParser.get('mazu_site_config', 'password')
mazu_dest_catalog_path = cfgParser.get('mazu_site_config', 'dest_catalog_path')

crgis_site_url = cfgParser.get('crgis_site_config', 'site_url')
crgis_catalog_path = cfgParser.get(
    'crgis_site_config', 'catalog-path')
crgis_login = cfgParser.get('crgis_site_config', 'login')
crgis_password = cfgParser.get('crgis_site_config', 'password')

miration_run_url = '%s/@@%s' % (mazu_site_url, mazu_migration_view_name)

fixdate = storage.get(
    'update_data', 'last_update_datetime')

if options.all:
    fixdate = 'None'
    logging.info(u'Full migration ...')

if fixdate == 'None':
    fixdate = '1900-01-01 00:00:01'

crgis_catalog_query = "{'path': {'query': '/crgis/temples/', 'depth': 10}, \
                        'deity_main': {'query': '天上聖母'}, \
                        'modified': {'query': '%s', 'range': 'min'}
                       }" % fixdate


def saveUpdateTime(updateTime):
    f = open(storageFile, 'w')
    storage.set(
        'update_data', 'last_update_datetime', updateTime)
    storage.write(f)
    f.close()


def getRequestData():
    data = {'remote-url': crgis_site_url,
            'remote-username': crgis_login,
            'remote-password': crgis_password,
            'catalog-path': crgis_catalog_path,
            'catalog-query': crgis_catalog_query,
            'dest_catalog_path': mazu_dest_catalog_path}
    return data


def main():
    updateTime = datetime.datetime.strftime(datetime.datetime.utcnow() -
        datetime.timedelta(hours=0, minutes=10), "%Y-%m-%d %H:%M:%S")

    logging.info(u'Start migration .... at %s' % updateTime)
    data = getRequestData()

    try:
        response = requests.post(
            miration_run_url, auth=(mazu_login, mazu_password), data = data)
        if (response.status_code == 200) and response.text == 'ok':
            logging.info(u'Migration finished ... ')
            saveUpdateTime(updateTime)
        else:
            logging.error(u'Migration error with cod %s and error: %s' %
                          (response.status_code, response.text))
    except:
        logging.error(u'Error connecting to Plone Site')


if __name__ == "__main__":
    main()

