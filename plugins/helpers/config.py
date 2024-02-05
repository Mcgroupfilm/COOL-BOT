import os
from os import environ
from dotenv import load_dotenv
load_dotenv()



API_ID = int(environ.get("API_ID", "24482882"))
API_HASH = environ.get("API_HASH", "27bd653cd164958dbfe7c942546e018d")
BOT_TOKEN = environ.get("BOT_TOKEN", "5940017882:AAE2PQtK5g33K5tvgPMaoaS1s6XipU5w-tE")
ADMINS = int(environ.get("ADMINS", "1180882237"))          
CAPTION = environ.get("CAPTION", "")

# for thumbnail ( back end is MrMKN brain 😉)
DOWNLOAD_LOCATION = "./DOWNLOADS"


# mdisk
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MDISK_API = os.environ.get("MDISK_API")
MDISK_CHANNEL = list(int(i.strip()) for i in os.environ.get("MDISK_CHANNEL").split(" ")) if os.environ.get("CHANNEL_ID") else []
FORWARD_MESSAGE = bool(os.environ.get("FORWARD_MESSAGE"))
ADMINS = list(int(i.strip()) for i in os.environ.get("ADMINS").split(",")) if os.environ.get("ADMINS") else []
SOURCE_CODE = "💕SHARE AND SUPPORT💕"
CHANNELS = bool(os.environ.get("CHANNELS"))


# attach


class Config(object):
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "5940017882:AAE2PQtK5g33K5tvgPMaoaS1s6XipU5w-tE")
  #CHANNEL_USERNAME without '@'
  CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME", "bigmoviesworld")
