"""
Utilities used throughout Compranet pipeline
"""
import os
import string
import datetime
import psycopg2
import numpy as np
import pandas as pd
#import json
#import re
#import hashlib
#import logging
#import logging.config
#from pandas.compat import range, lzip, map

import luigi
import luigi.postgres
from luigi import configuration
from luigi import six


#LOGGING_CONF = configuration.get_config().get("core", "logging_conf_file")
#logging.config.fileConfig(LOGGING_CONF)
#logger = logging.getLogger("compranet.pipeline")


def parse_cfg_string(string):
    """
    Parse a comma separated string into a list
    """
    string = string.split(",")
    return [m.strip() for m in string]
