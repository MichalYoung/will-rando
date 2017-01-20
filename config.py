"""
Obtain configuration values from 
the environment or a configuration file. 

Known configuration values are:
   app_key  (a string used to cryptographically sign cookies)

Approach: We'll always have an app.conf file, but 
environment variables take precedence over the 
configuration file values.  app.conf isn't under 
git control; 'configure' is. 

"""
import os
import logging
import configparser

config_file_path = "app.conf"

logging.basicConfig(level=logging.INFO)

config_keys = [ "app_key", "debug", "port", "host" ]
config_dict = { }

# The only API function
#
def get(key):
    return config_dict[key]

config = configparser.ConfigParser()
config.read(config_file_path)
translations = { "true": True, "false": False }

# Environment variables override configuration file entries
# 
for key in config_keys:
    if key in os.environ:
        val = os.environ[key]
    else:
        val= config['DEFAULT'][key]
    if val in translations:
        val = translations[val]
    config_dict[key] = val




    


