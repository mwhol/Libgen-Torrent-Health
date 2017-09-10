import bencoding
from io import BytesIO
import binascii
import hashlib
import os

#From: https://stackoverflow.com/questions/2572521/extract-the-sha1-hash-from-a-torrent-file
def hash(filepath):
	with open(filepath, "rb") as f:
		print(filepath)
		data = bencoding.bdecode(f.read())
	info = data[b'info']
	binfo = bencoding.bencode(info)
	hashed_info = hashlib.sha1(binfo).hexdigest()
	return(hashed_info)

def readtorrents(test, path="cache/"):
	torrents = os.listdir(path)
	torrents = [[x] for x in torrents if ".torrent" in x]
	if test == True:
		torrents = torrents[:100]
	torrents.sort()
	return(torrents)

def hashtolist(torrents):
	for x in torrents:
		hashcode = hash("cache/" + x[0])
		x.append(hashcode)
	return(torrents)

def torrentsandhashes(test=False):
	files = readtorrents(test)
	formatted_list = hashtolist(files)
	return(formatted_list)