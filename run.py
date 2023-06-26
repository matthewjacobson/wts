#------------------------------------------#
#------------ CONFIG VARIABLES ------------#
#------------------------------------------#

import os
from dotenv import load_dotenv
load_dotenv()

DIRECTORY_PATH = os.path.realpath(os.path.dirname(__file__))

# mongodb
ATLAS_USERNAME = os.environ.get("atlas-username")
ATLAS_PASSWORD = os.environ.get("atlas-password")
ATLAS_URI = f"mongodb+srv://{ATLAS_USERNAME}:{ATLAS_PASSWORD}@wts-webapp.bov55.mongodb.net/?retryWrites=true&w=majority"
ATLAS_DB_NAME = "wts-artyard"
ATLAS_COLLECTION_NAME = "data"
ATLAS_DOCUMENT_LIMIT = 40

# svg
# X_DATA_IN_MIN = -6.07
# X_DATA_IN_MAX = 4.22
# Y_DATA_IN_MIN = -1.11
# Y_DATA_IN_MAX = 18.09
X_DATA_IN_MIN = -4.2
X_DATA_IN_MAX = 2.2
Y_DATA_IN_MIN = 1.5
Y_DATA_IN_MAX = 14
SVG_PADDING_INCHES = 0.25
SVG_WIDTH_INCHES = 23.4
SVG_HEIGHT_INCHES = 33.1
SVG_DPI = 100
SVG_WIDTH_PIXELS = int(SVG_DPI * SVG_WIDTH_INCHES)
SVG_HEIGHT_PIXELS = int(SVG_DPI * SVG_HEIGHT_INCHES)

# axidraw - https://axidraw.com/doc/py_api/#options-general
AXIDRAW_OPTIONS = {
	"speed_pendown": 1,		# Maximum XY speed when the pen is down (plotting).
	"speed_penup": 1,		# Maximum XY speed when the pen is up.
	"accel": 1,				# Relative acceleration/deceleration speed.
	"pen_pos_down": 10,		# Pen height when the pen is down (plotting).
	"pen_pos_up": 90,		# Pen height when the pen is up.
	"pen_rate_lower": 1,	# Speed of lowering the pen-lift motor.
	"pen_rate_raise": 1,	# Speed of raising the pen-lift motor.
	"pen_delay_down": 0,	# Added delay after lowering pen.
	"pen_delay_up": 70,		# Added delay after raising pen.
	"const_speed": True,	# Option: Use constant speed when pen is down.
	"model": 5,				# Select model of AxiDraw hardware.
	"penlift": 1,			# Pen lift servo configuration
	"port": None,			# Specify a USB port or AxiDraw to use.
	"port_config": 0		# Override how the USB ports are located.
}

#------------------------------------------#



#-------------------------------------------#
#-------------- LOGGING SETUP --------------#
#-------------------------------------------#

import logging
import time
import json

def create_log():

	for handler in logging.root.handlers[:]:
		logging.root.removeHandler(handler)

	log_timestamp = int(time.time())

	logging.basicConfig(
		filename=f"{DIRECTORY_PATH}/logs/{log_timestamp}_log.txt",
		encoding="utf-8",
		level=logging.DEBUG
	)

	logging.info("config:")
	logging.info("	mongodb:")
	logging.info(f"		ATLAS_URI: {ATLAS_URI}")
	logging.info(f"		ATLAS_DB_NAME: {ATLAS_DB_NAME}")
	logging.info(f"		ATLAS_COLLECTION_NAME: {ATLAS_COLLECTION_NAME}")
	logging.info(f"		ATLAS_DOCUMENT_LIMIT: {ATLAS_DOCUMENT_LIMIT}")
	logging.info("	svg:")
	logging.info(f"		SVG_WIDTH_INCHES: {SVG_WIDTH_INCHES}")
	logging.info(f"		SVG_HEIGHT_INCHES: {SVG_HEIGHT_INCHES}")
	logging.info(f"		SVG_DPI: {SVG_DPI}")
	logging.info(f"		SVG_WIDTH_PIXELS: {SVG_WIDTH_PIXELS}")
	logging.info(f"		SVG_HEIGHT_PIXELS: {SVG_HEIGHT_PIXELS}")
	logging.info("	axidraw:")
	logging.info(f"		AXIDRAW_OPTIONS: \n{json.dumps(AXIDRAW_OPTIONS, indent=4)}")

	return log_timestamp

#-------------------------------------------#



#-------------------------------------------#
#------------ MONGODB DATA PULL ------------#
#-------------------------------------------#

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def get_data():

	logging.info("Starting data pull from MongoDB")

	# create a new client
	client = MongoClient(ATLAS_URI, server_api=ServerApi("1"))

	# Send a ping to confirm a successful connection
	try:
		client.admin.command("ping")
		logging.info("Pinged your deployment. Successfully connected to MongoDB...")
	except Exception as e:
		logging.error(e)

	# get the database
	database = client[ATLAS_DB_NAME]

	# get the collection
	collection = database[ATLAS_COLLECTION_NAME]

	# loop over documents and add to array - https://pymongo.readthedocs.io/en/stable/tutorial.html
	documents = [] # array to store the documents
	for document in collection.find(limit=ATLAS_DOCUMENT_LIMIT).sort("_id", -1):
		documents.append(document)

	return documents

#-------------------------------------------#



#--------------------------------------------#
#--------------- SVG CREATION ---------------#
#--------------------------------------------#

import svgwrite

# https://regex101.com/ - (?<!id=")(?<=d=")[^"]*
TEXTS = [
	{
		"title": "FIRE PREVENTION",
		"rotate": "0",
		"scale": 5,
		"translate": [-1.7989377289377326, 4.077399267399268],
		"paths": ["M -42.998 -3.50094 L -42.998 3.50521 M -42.998 -3.50094 L -38.6588 -3.50094 M -42.998 -0.15661 L -40.331 -0.15661","M -36.9972 -3.50094 L -36.9972 3.50521","M -34.3302 -3.50094 L -34.3302 3.50521 M -34.3302 -3.50094 L -31.3246 -3.50094 L -30.3298 -3.16227 L -29.9911 -2.8236 L -29.6524 -2.16744 L -29.6524 -1.49011 L -29.9911 -0.83394 L -30.3298 -0.49528 L -31.3246 -0.15661 L -34.3302 -0.15661 M -31.9913 -0.15661 L -29.6524 3.50521","M -27.3241 -3.50094 L -27.3241 3.50521 M -27.3241 -3.50094 L -22.9849 -3.50094 M -27.3241 -0.15661 L -24.6571 -0.15661 M -27.3241 3.50521 L -22.9849 3.50521","M -16.9948 -3.50094 L -16.9948 3.50521 M -16.9948 -3.50094 L -13.9891 -3.50094 L -12.9943 -3.16227 L -12.6556 -2.8236 L -12.317 -2.16744 L -12.317 -1.16203 L -12.6556 -0.49528 L -12.9943 -0.15661 L -13.9891 0.17147 L -16.9948 0.17147","M -9.9887 -3.50094 L -9.9887 3.50521 M -9.9887 -3.50094 L -6.983 -3.50094 L -5.9882 -3.16227 L -5.6495 -2.8236 L -5.3109 -2.16744 L -5.3109 -1.49011 L -5.6495 -0.83394 L -5.9882 -0.49528 L -6.983 -0.15661 L -9.9887 -0.15661 M -7.6498 -0.15661 L -5.3109 3.50521","M -2.9825 -3.50094 L -2.9825 3.50521 M -2.9825 -3.50094 L 1.3567 -3.50094 M -2.9825 -0.15661 L -0.3155 -0.15661 M -2.9825 3.50521 L 1.3567 3.50521","M 2.3515 -3.50094 L 5.0185 3.50521 M 7.6855 -3.50094 L 5.0185 3.50521","M 9.347 -3.50094 L 9.347 3.50521 M 9.347 -3.50094 L 13.6862 -3.50094 M 9.347 -0.15661 L 12.014 -0.15661 M 9.347 3.50521 L 13.6862 3.50521","M 15.6758 -3.50094 L 15.6758 3.50521 M 15.6758 -3.50094 L 20.3536 3.50521 M 20.3536 -3.50094 L 20.3536 3.50521","M 24.3435 -3.50094 L 24.3435 3.50521 M 22.0152 -3.50094 L 26.6824 -3.50094","M 28.344 -3.50094 L 28.344 3.50521","M 32.6832 -3.50094 L 32.0164 -3.16227 L 31.3497 -2.49552 L 31.011 -1.82877 L 30.6829 -0.83394 L 30.6829 0.83822 L 31.011 1.83305 L 31.3497 2.50509 L 32.0164 3.17184 L 32.6832 3.50521 L 34.0167 3.50521 L 34.6834 3.17184 L 35.3502 2.50509 L 35.6888 1.83305 L 36.0169 0.83822 L 36.0169 -0.83394 L 35.6888 -1.82877 L 35.3502 -2.49552 L 34.6834 -3.16227 L 34.0167 -3.50094 Z","M 38.3452 -3.50094 L 38.3452 3.50521 M 38.3452 -3.50094 L 43.023 3.50521 M 43.023 -3.50094 L 43.023 3.50521"]
	},
	{
		"title": "PACK/UNPACK",
		"rotate": "0",
		"scale": 5,
		"translate": [-3.028529411764706, 7.079705882352942],
		"paths": ["M -36.8512 -3.99623 L -36.8512 3.00991 M -36.8512 -3.99623 L -33.8455 -3.99623 L -32.8507 -3.65757 L -32.512 -3.3189 L -32.1734 -2.66274 L -32.1734 -1.65733 L -32.512 -0.99058 L -32.8507 -0.65191 L -33.8455 -0.32383 L -36.8512 -0.32383","M -28.1729 -3.99623 L -30.8399 3.00991 M -28.1729 -3.99623 L -25.5059 3.00991 M -29.845 0.68158 L -26.5007 0.68158","M -19.1665 -2.32407 L -19.5051 -2.99082 L -20.1719 -3.65757 L -20.8386 -3.99623 L -22.1721 -3.99623 L -22.8389 -3.65757 L -23.5056 -2.99082 L -23.8443 -2.32407 L -24.1724 -1.32924 L -24.1724 0.34292 L -23.8443 1.33775 L -23.5056 2.00979 L -22.8389 2.67654 L -22.1721 3.00991 L -20.8386 3.00991 L -20.1719 2.67654 L -19.5051 2.00979 L -19.1665 1.33775","M -16.8382 -3.99623 L -16.8382 3.00991 M -12.1604 -3.99623 L -16.8382 0.68158 M -15.166 -0.99058 L -12.1604 3.00991","M -4.498 -5.32973 L -10.4881 5.33821","M -2.4978 -3.99623 L -2.4978 1.00967 L -2.1591 2.00979 L -1.4924 2.67654 L -0.4869 3.00991 L 0.1692 3.00991 L 1.1746 2.67654 L 1.8414 2.00979 L 2.18 1.00967 L 2.18 -3.99623","M 4.8364 -3.99623 L 4.8364 3.00991 M 4.8364 -3.99623 L 9.5142 3.00991 M 9.5142 -3.99623 L 9.5142 3.00991","M 12.1706 -3.99623 L 12.1706 3.00991 M 12.1706 -3.99623 L 15.1763 -3.99623 L 16.1711 -3.65757 L 16.5098 -3.3189 L 16.8484 -2.66274 L 16.8484 -1.65733 L 16.5098 -0.99058 L 16.1711 -0.65191 L 15.1763 -0.32383 L 12.1706 -0.32383","M 20.849 -3.99623 L 18.182 3.00991 M 20.849 -3.99623 L 23.516 3.00991 M 19.1768 0.68158 L 22.5211 0.68158","M 29.8553 -2.32407 L 29.5167 -2.99082 L 28.8499 -3.65757 L 28.1832 -3.99623 L 26.8497 -3.99623 L 26.1829 -3.65757 L 25.5162 -2.99082 L 25.1775 -2.32407 L 24.8494 -1.32924 L 24.8494 0.34292 L 25.1775 1.33775 L 25.5162 2.00979 L 26.1829 2.67654 L 26.8497 3.00991 L 28.1832 3.00991 L 28.8499 2.67654 L 29.5167 2.00979 L 29.8553 1.33775","M 32.1837 -3.99623 L 32.1837 3.00991 M 36.8615 -3.99623 L 32.1837 0.68158 M 33.8559 -0.99058 L 36.8615 3.00991"]
	},
	{
		"title": "MONOLITH",
		"rotate": "0",
		"scale": 5,
		"translate": [-0.4233333333333331, 6.523589743589747],
		"paths": ["M -24.1766 -3.50094 L -24.1766 3.50521 M -24.1766 -3.50094 L -21.5096 3.50521 M -18.8426 -3.50094 L -21.5096 3.50521 M -18.8426 -3.50094 L -18.8426 3.50521","M -14.5034 -3.50094 L -15.1702 -3.16227 L -15.8369 -2.49552 L -16.1756 -1.82877 L -16.5037 -0.83394 L -16.5037 0.83822 L -16.1756 1.83305 L -15.8369 2.50509 L -15.1702 3.17184 L -14.5034 3.50521 L -13.1699 3.50521 L -12.5032 3.17184 L -11.8365 2.50509 L -11.4978 1.83305 L -11.1697 0.83822 L -11.1697 -0.83394 L -11.4978 -1.82877 L -11.8365 -2.49552 L -12.5032 -3.16227 L -13.1699 -3.50094 Z","M -8.8414 -3.50094 L -8.8414 3.50521 M -8.8414 -3.50094 L -4.1636 3.50521 M -4.1636 -3.50094 L -4.1636 3.50521","M 0.165 -3.50094 L -0.5018 -3.16227 L -1.1685 -2.49552 L -1.5072 -1.82877 L -1.8353 -0.83394 L -1.8353 0.83822 L -1.5072 1.83305 L -1.1685 2.50509 L -0.5018 3.17184 L 0.165 3.50521 L 1.4985 3.50521 L 2.1652 3.17184 L 2.832 2.50509 L 3.1706 1.83305 L 3.4987 0.83822 L 3.4987 -0.83394 L 3.1706 -1.82877 L 2.832 -2.49552 L 2.1652 -3.16227 L 1.4985 -3.50094 Z","M 5.8271 -3.50094 L 5.8271 3.50521 M 5.8271 3.50521 L 9.8276 3.50521","M 11.4997 -3.50094 L 11.4997 3.50521","M 15.5002 -3.50094 L 15.5002 3.50521 M 13.1719 -3.50094 L 17.8391 -3.50094","M 19.5007 -3.50094 L 19.5007 3.50521 M 24.1785 -3.50094 L 24.1785 3.50521 M 19.5007 -0.15661 L 24.1785 -0.15661"]
	},
	{
		"title": "HOUSE FIRE",
		"rotate": "0",
		"scale": 5,
		"translate": [-3.882564102564104, 10.501025641025636],
		"paths": ["M -29.5106 -3.50094 L -29.5106 3.50521 M -24.8328 -3.50094 L -24.8328 3.50521 M -29.5106 -0.15661 L -24.8328 -0.15661","M -20.5042 -3.50094 L -21.1709 -3.16227 L -21.8377 -2.49552 L -22.1763 -1.82877 L -22.5044 -0.83394 L -22.5044 0.83822 L -22.1763 1.83305 L -21.8377 2.50509 L -21.1709 3.17184 L -20.5042 3.50521 L -19.1707 3.50521 L -18.5039 3.17184 L -17.8372 2.50509 L -17.4985 1.83305 L -17.1704 0.83822 L -17.1704 -0.83394 L -17.4985 -1.82877 L -17.8372 -2.49552 L -18.5039 -3.16227 L -19.1707 -3.50094 Z","M -14.8421 -3.50094 L -14.8421 1.50497 L -14.5034 2.50509 L -13.8367 3.17184 L -12.8312 3.50521 L -12.1751 3.50521 L -11.1697 3.17184 L -10.5029 2.50509 L -10.1643 1.50497 L -10.1643 -3.50094","M -3.1687 -2.49552 L -3.8355 -3.16227 L -4.8409 -3.50094 L -6.1744 -3.50094 L -7.1692 -3.16227 L -7.836 -2.49552 L -7.836 -1.82877 L -7.5079 -1.16203 L -7.1692 -0.83394 L -6.5025 -0.49528 L -4.5022 0.17147 L -3.8355 0.49955 L -3.5074 0.83822 L -3.1687 1.50497 L -3.1687 2.50509 L -3.8355 3.17184 L -4.8409 3.50521 L -6.1744 3.50521 L -7.1692 3.17184 L -7.836 2.50509","M -0.8404 -3.50094 L -0.8404 3.50521 M -0.8404 -3.50094 L 3.4988 -3.50094 M -0.8404 -0.15661 L 1.8266 -0.15661 M -0.8404 3.50521 L 3.4988 3.50521","M 9.4889 -3.50094 L 9.4889 3.50521 M 9.4889 -3.50094 L 13.8281 -3.50094 M 9.4889 -0.15661 L 12.1559 -0.15661","M 15.4896 -3.50094 L 15.4896 3.50521","M 18.1566 -3.50094 L 18.1566 3.50521 M 18.1566 -3.50094 L 21.1623 -3.50094 L 22.1571 -3.16227 L 22.4958 -2.8236 L 22.8344 -2.16744 L 22.8344 -1.49011 L 22.4958 -0.83394 L 22.1571 -0.49528 L 21.1623 -0.15661 L 18.1566 -0.15661 M 20.4955 -0.15661 L 22.8344 3.50521","M 25.1627 -3.50094 L 25.1627 3.50521 M 25.1627 -3.50094 L 29.5019 -3.50094 M 25.1627 -0.15661 L 27.8297 -0.15661 M 25.1627 3.50521 L 29.5019 3.50521"]
	},
	{
		"title": "MONTANA",
		"rotate": "0",
		"scale": 5,
		"translate": [-1.6519999999999988, 11.513499999999993],
		"paths": ["M -22.8304 -3.50094 L -22.8304 3.50521 M -22.8304 -3.50093 L -20.1634 3.50521 M -17.4964 -3.50094 L -20.1634 3.50521 M -17.4964 -3.50094 L -17.4964 3.50521","M -13.1572 -3.50094 L -13.824 -3.16227 L -14.4907 -2.49552 L -14.8294 -1.82877 L -15.1575 -0.83394 L -15.1575 0.83822 L -14.8294 1.83305 L -14.4907 2.50509 L -13.824 3.17184 L -13.1572 3.50521 L -11.8237 3.50521 L -11.157 3.17184 L -10.4903 2.50509 L -10.1516 1.83305 L -9.8235 0.83822 L -9.8235 -0.83394 L -10.1516 -1.82877 L -10.4903 -2.49552 L -11.157 -3.16227 L -11.8237 -3.50094 Z","M -7.4952 -3.50094 L -7.4952 3.50521 M -7.4952 -3.50093 L -2.8174 3.50521 M -2.8174 -3.50093 L -2.8174 3.50521","M 1.1725 -3.50094 L 1.1725 3.50521 M -1.1558 -3.50094 L 3.5114 -3.50094","M 6.8452 -3.50094 L 4.1782 3.50521 M 6.8452 -3.50093 L 9.5122 3.50521 M 5.173 1.17688 L 8.5173 1.17688","M 11.1737 -3.50094 L 11.1737 3.50521 M 11.1737 -3.50093 L 15.8515 3.50521 M 15.8515 -3.50093 L 15.8515 3.50521","M 20.1802 -3.50094 L 17.5132 3.50521 M 20.1802 -3.50093 L 22.8472 3.50521 M 18.508 1.17688 L 21.8523 1.17688"]
	},
	{
		"title": "ABANDONED",
		"rotate": "0",
		"scale": 5,
		"translate": [-2.1572946429, 9.2146339286],
		"paths": ["M -27.3515 -3.50094 L -30.0185 3.50521 M -27.3515 -3.50094 L -24.6845 3.50521 M -29.0237 1.17688 L -25.6793 1.17688","M -23.0229 -3.50094 L -23.0229 3.50521 M -23.0229 -3.50093 L -20.0173 -3.50093 L -19.0225 -3.16227 L -18.6838 -2.8236 L -18.3451 -2.16744 L -18.3451 -1.49011 L -18.6838 -0.83394 L -19.0225 -0.49528 L -20.0173 -0.15661 M -23.0229 -0.15661 L -20.0173 -0.15661 L -19.0225 0.17147 L -18.6838 0.49955 L -18.3451 1.17688 L -18.3451 2.17171 L -18.6838 2.83846 L -19.0225 3.17184 L -20.0173 3.50521 L -23.0229 3.50521","M -14.3446 -3.50094 L -17.0116 3.50521 M -14.3446 -3.50093 L -11.6776 3.50521 M -16.0168 1.17688 L -12.6725 1.17688","M -10.0161 -3.50094 L -10.0161 3.50521 M -10.0161 -3.50093 L -5.3383 3.50521 M -5.3383 -3.50093 L -5.3383 3.50521","M -2.6819 -3.50094 L -2.6819 3.50521 M -2.6819 -3.50093 L -0.343 -3.50093 L 0.6624 -3.16227 L 1.3186 -2.49552 L 1.6573 -1.82877 L 1.9959 -0.83394 L 1.9959 0.83822 L 1.6573 1.83305 L 1.3186 2.50509 L 0.6624 3.17184 L -0.343 3.50521 L -2.6819 3.50521","M 5.9965 -3.50094 L 5.3297 -3.16227 L 4.663 -2.49552 L 4.3243 -1.82877 L 3.9962 -0.83394 L 3.9962 0.83822 L 4.3243 1.83305 L 4.663 2.50509 L 5.3297 3.17184 L 5.9965 3.50521 L 7.33 3.50521 L 7.9967 3.17184 L 8.6635 2.50509 L 9.0021 1.83305 L 9.3302 0.83822 L 9.3302 -0.83394 L 9.0021 -1.82877 L 8.6635 -2.49552 L 7.9967 -3.16227 L 7.33 -3.50094 Z","M 11.6585 -3.50094 L 11.6585 3.50521 M 11.6585 -3.50093 L 16.3363 3.50521 M 16.3363 -3.50093 L 16.3363 3.50521","M 18.9927 -3.50094 L 18.9927 3.50521 M 18.9927 -3.50093 L 23.3319 -3.50093 M 18.9927 -0.15661 L 21.6597 -0.15661 M 18.9927 3.50521 L 23.3319 3.50521","M 25.3215 -3.50094 L 25.3215 3.50521 M 25.3215 -3.50093 L 27.6604 -3.50093 L 28.6658 -3.16227 L 29.322 -2.49552 L 29.6607 -1.82877 L 29.9993 -0.83394 L 29.9993 0.83822 L 29.6607 1.83305 L 29.322 2.50509 L 28.6658 3.17184 L 27.6604 3.50521 L 25.3215 3.50521"]

	}
]

def create_svg(log_timestamp, data):
	logging.info("Starting SVG creation")

	# setup the svg object
	svg = svgwrite.Drawing(
		filename=f"{DIRECTORY_PATH}/outputs/{log_timestamp}_output.svg",
		size=(f"{SVG_WIDTH_INCHES}in", f"{SVG_HEIGHT_INCHES}in"),
		viewBox=(f"0 0 {SVG_WIDTH_PIXELS} {SVG_HEIGHT_PIXELS}"),
		profile="full"
	)

	# setup class for non-scaling-stroke
	svg.defs.add(svg.style("""
		.vectorEffectClass {
			vector-effect: non-scaling-stroke;
		}
	"""))

	# get the incoming bounds
	bounds = [10000, -10000, 10000, -10000]
	for document in data:
		for position in document["pos"]:
			if float(position["x"]) < bounds[0]:
				bounds[0] = float(position["x"])
			elif float(position["x"]) > bounds[1]:
				bounds[1] = float(position["x"])
			if float(position["y"]) < bounds[2]:
				bounds[2] = float(position["y"])
			elif float(position["y"]) > bounds[3]:
				bounds[3] = float(position["y"])

	def mapRange(t, inMin, inMax, outMin, outMax):
		return (t - inMin) / (inMax - inMin) * (outMax - outMin) + outMin;

	# calculate the aspect ratios
	in_aspect_ratio = (X_DATA_IN_MAX - X_DATA_IN_MIN) / (Y_DATA_IN_MAX - Y_DATA_IN_MIN)
	out_aspect_ratio = (SVG_WIDTH_INCHES - 2 * SVG_PADDING_INCHES) / (SVG_HEIGHT_INCHES - 2 * SVG_PADDING_INCHES)

	# calculate the bounding box
	boundingBox = {'x': 0, 'y': 0, 'w': 0, 'h': 0}
	if in_aspect_ratio < out_aspect_ratio:
		boundingBox['y'] = SVG_PADDING_INCHES * SVG_DPI
		boundingBox['h'] = SVG_HEIGHT_PIXELS - 2 * boundingBox['y']
		boundingBox['x'] = 0.5 * (SVG_WIDTH_PIXELS - in_aspect_ratio * (SVG_HEIGHT_PIXELS - 2 * SVG_PADDING_INCHES * SVG_DPI))
		boundingBox['w'] = SVG_WIDTH_PIXELS - 2 * boundingBox['x']
	else:
		boundingBox['x'] = SVG_PADDING_INCHES * SVG_DPI
		boundingBox['w'] = SVG_WIDTH_PIXELS - 2 * boundingBox['x']
		boundingBox['y'] = 0.5 * (SVG_HEIGHT_PIXELS - 1 / in_aspect_ratio * (SVG_WIDTH_PIXELS - 2 * SVG_PADDING_INCHES * SVG_DPI))
		boundingBox['h'] = SVG_HEIGHT_PIXELS - 2 * boundingBox['y']

	# add text to the svg
	for text in TEXTS:
		scale = text["scale"]
		rotate = text["rotate"]
		xTranslate = mapRange(text["translate"][0], X_DATA_IN_MIN, X_DATA_IN_MAX, boundingBox["x"], boundingBox["x"] + boundingBox["w"])
		yTranslate = mapRange(text["translate"][1], Y_DATA_IN_MIN, Y_DATA_IN_MAX, boundingBox["y"], boundingBox["y"] + boundingBox["h"])
		for path in text["paths"]:
			svg.add(svg.path(d=path, stroke="#000", fill="none", stroke_width=1, class_='vectorEffectClass', transform=f"translate({xTranslate} {yTranslate}) rotate({rotate}) scale({scale})"))

	docIndex = 0
	for document in data:
		path_positions = []
		for posIndex, position in enumerate(document["pos"]):
			x = mapRange(float(position["x"]), X_DATA_IN_MIN, X_DATA_IN_MAX, boundingBox['x'], boundingBox['x'] + boundingBox['w'])
			y = mapRange(float(position["y"]), Y_DATA_IN_MIN, Y_DATA_IN_MAX, boundingBox['y'], boundingBox['y'] + boundingBox['h'])
			if x > boundingBox["x"] and x < boundingBox["x"] + boundingBox["w"] and y > boundingBox["y"] and y < boundingBox["y"] + boundingBox["h"]:
				path_positions.append({"x": x, "y": y})
			if x < boundingBox["x"] or x > boundingBox["x"] + boundingBox["w"] or y < boundingBox["y"] or y > boundingBox["y"] + boundingBox["h"] or posIndex == len(document["pos"]):
				if len(path_positions) > 1:
					path_string = ""
					for index, position in enumerate(path_positions):
						px = position["x"]
						py = position["y"]
						if index == 0:
							path_string += f"M{px},{py}"
						else:
							path_string += f" L{px},{py}"
					svg.add(svg.path(d=path_string, stroke="#000", fill="none", stroke_width=1))
				path_positions = []

	# save the svg
	svg.save(pretty=True, indent=4)

	logging.info(f"SVG saved to {svg.filename}")

	return svg.filename

#--------------------------------------------#



#-------------------------------------------#
#------------- AXIDRAW CONTROL -------------#
#-------------------------------------------#

from pyaxidraw import axidraw

# create the axidraw class instance
axi = axidraw.AxiDraw()

def plot(svg_filename):

	logging.info("Starting axidraw control")

	# load file
	axi.plot_setup(svg_filename)

	logging.info("SVG loaded")

	# enable errors
	axi.errors.connect = True
	axi.errors.button = True
	axi.errors.keyboard = True
	axi.errors.disconnect = True

	# configure plot context
	# axi.options.speed_pendown = AXIDRAW_OPTIONS["speed_pendown"]
	# axi.options.speed_penup = AXIDRAW_OPTIONS["speed_penup"]
	# axi.options.accel = AXIDRAW_OPTIONS["accel"]
	axi.options.pen_pos_down = AXIDRAW_OPTIONS["pen_pos_down"]
	axi.options.pen_pos_up = AXIDRAW_OPTIONS["pen_pos_up"]
	# axi.options.pen_rate_lower = AXIDRAW_OPTIONS["pen_rate_lower"]
	# axi.options.pen_rate_raise = AXIDRAW_OPTIONS["pen_rate_raise"]
	# axi.options.pen_delay_down = AXIDRAW_OPTIONS["pen_delay_down"]
	# axi.options.pen_delay_up = AXIDRAW_OPTIONS["pen_delay_up"]
	axi.options.const_speed = AXIDRAW_OPTIONS["const_speed"]
	axi.options.model = AXIDRAW_OPTIONS["model"]
	# axi.options.penlift = AXIDRAW_OPTIONS["penlift"]
	# axi.options.port = AXIDRAW_OPTIONS["port"]
	# axi.options.port_config = AXIDRAW_OPTIONS["port_config"]

	# plot the file
	try:
		# axi.plot_run()
		# logging.info("plot complete")
		# axi.options.mode = "align"
		# axi.plot_run()

		# trying to add pause/resume functionality
		output_svg = axi.plot_run(True)
		return output_svg
	except RuntimeError:
		axi.options.mode = "align"
		axi.plot_run()
		logging.error(f"plot failed with error {axi.errors.code}")
		if axi.errors.code == 101:
			logging.error(f"failed to connect")
		elif axi.errors.code == 102:
			logging.error(f"failed to connect")
		elif axi.errors.code == 103:
			logging.error(f"failed to connect")
		elif axi.errors.code == 104:
			logging.error(f"failed to connect")

def resume_plot(output_svg):

	logging.info("Resuming plot")

	# load file
	axi.plot_setup(output_svg)
	
	axi.options.mode = "res_plot"

	logging.info("SVG loaded")
	
	try:
		# trying to add pause/resume functionality
		output_svg = axi.plot_run(True)
		return output_svg
	except RuntimeError:
		axi.options.mode = "align"
		axi.plot_run()
		logging.error(f"plot failed with error {axi.errors.code}")
		if axi.errors.code == 101:
			logging.error(f"failed to connect")
		elif axi.errors.code == 102:
			logging.error(f"failed to connect")
		elif axi.errors.code == 103:
			logging.error(f"failed to connect")
		elif axi.errors.code == 104:
			logging.error(f"failed to connect")
	

#-------------------------------------------#



#--------------------------------------------#
#------------- BUTTON DETECTION -------------#
#--------------------------------------------#

from gpiozero import Button
import signal

if __name__ == "__main__":

	output_svg = None
	isRunning = False
	
	def run():
		print("running")
		global isRunning, output_svg
		if not isRunning:
			isRunning = True
			log_timestamp = create_log()
			data = get_data()
			svg_filename = create_svg(log_timestamp, data)
			output_svg = plot(svg_filename)
			isRunning = False

	def resume():
		print("resuming")
		global isRunning, output_svg
		if not isRunning:
			isRunning = True
			log_timestamp = create_log()
			output_svg = resume_plot(output_svg)
			isRunning = False

	button = Button(14)
	button.when_pressed = run
	
	pause_button = Button(24)
	button.when_pressed = resume
	
	signal.pause()

#-------------------------------------------#
