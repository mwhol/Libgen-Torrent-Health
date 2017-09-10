#To Gather Info on all current torrents on , make a backup
from bs4 import BeautifulSoup
import requests
import urllib
import os
import filecmp


#TODO
#CREATE URL VARIABLES
#DEFINE MAIN

def alltorrents():
	#downloads all torrents from libgen, should be run first time
	r = requests.get('http://gen.lib.rus.ec/repository_torrent/')
	c = r.content
	soup = BeautifulSoup(c, "html.parser")

	torrents = torrentnames(soup)

	torrentlinks = [("http://gen.lib.rus.ec/repository_torrent/" + x) for x in torrents]
	return(torrentlinks)

#http://gen.lib.rus.ec/repository_torrent/r_000.torrent

def torrentnames(soup):
	#support for new files, 
	torrents = []
	entries = soup.find_all("tr")
	for entry in entries:
		if entry.find("a"):
			if "torrent" in entry.find("a").get("href"):
				torrents.append(entry.find("a").get("href"))
	return(torrents)


def cacheupdate():
	#tests libgen and sees if any new torrents have been added
	urllib.request.urlretrieve("http://gen.lib.rus.ec/repository_torrent/", "cache/testfile.html")
	test = filecmp.cmp("cache/testfile.html", "cache/Index of _repository_torrent.html")
	if test != True:
		todownload = newtorrentfiles()
		torrentdownloader(todownload)
		urllib.request.urlretrieve("http://gen.lib.rus.ec/repository_torrent/", "cache/Index of _repository_torrent.html")
	return(test)

def newtorrentfiles():
	#takes old and new files and tests if cache is up to date
	soupold = BeautifulSoup(open("cache/Index of _repository_torrent.html"), "html.parser")
	soupnew = BeautifulSoup(open("cache/testfile.html"), "html.parser")

	oldfiles = torrentnames(soupold)
	newfiles = torrentnames(soupnew)

	truenewfiles = [("http://gen.lib.rus.ec/repository_torrent/" + x) for x in newfiles if x not in oldfiles]
	return(truenewfiles)

def torrentdownloader(torrentlist):
	#downloads new files to cache
	for url in torrentlist:
		filename = "cache/" + url.split("/")[-1]
		urllib.request.urlretrieve(url, filename)


