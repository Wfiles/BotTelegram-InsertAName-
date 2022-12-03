import logging
from subprocess import CalledProcessError
import requests
import random
import os
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

