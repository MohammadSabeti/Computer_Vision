
# DOCUMENT: *** JSON-minify : ***
		# `JSON-minify` minifies blocks of JSON-like content into valid JSON by removing
		# all whitespace *and* JS-style comments (single-line `//` and multi-line
		# `/* .. */`).
		# With `JSON-minify`, you can maintain developer-friendly JSON documents, but
		# minify them before parsing or transmitting them over-the-wire.

# NOTE: json.loads() : 
		# json. loads() method can be used to parse a valid JSON string and
  		# convert it into a Python Dictionary



# import the necessary packages
from json_minify import json_minify
import json

class Conf:
	def __init__(self, confPath):
		# load and store the configuration and update the object's
		# dictionary
		conf = json.loads(json_minify(open(confPath).read()))
		self.__dict__.update(conf)

	def __getitem__(self, k):
		# return the value associated with the supplied key
		return self.__dict__.get(k, None)