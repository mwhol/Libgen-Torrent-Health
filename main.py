from mycode.asyncscraper import download_urls
from mycode.genlibgetter import cacheupdate
from mycode.hasher import torrentsandhashes
from mycode.scraper2 import scrape
import sys
import math


def infofetcher(hashlist, chunksize):
	chunks = math.ceil(len(hashlist)/chunksize)
	chunkedhash = [hashlist[(i*chunksize):(i+1)*chunksize] for i in range(0, chunks)]
	tracker = 'http://tracker2.wasabii.com.tw:6969/announce'
	if chunksize == 1:
		tracker = 'http://tracker1.wasabii.com.tw:6969/announce'
	results = []
	count = 1
	#We chunkify so we can be efficient in our fetching
	for x in chunkedhash:
		print("Scrape #" + str(count) + " of " + str(chunks))
		results.append(scrape(tracker, x))
		count += 1
	return(results)


def resultsformatter(listofdicts):
	#Dictionary cleanup
	#we flatten to a big dict
	results = {k:v for x in listofdicts for k,v in x.items()}	
	#and turn bytes to strings
	for key in results.keys():
		newkey = str(key)[2:-1]
		results[newkey] = results.pop(key)
	return(results)


def seedfetchingmaster(hashlist, chunksize, reruns=2):
	finaldict = {}
	hashes = hashlist
	for x in range(1, (reruns+1)):
		print("\n\nTrial #" + str(x) + " of " + str(reruns) + "\n\n")
		roughlist = infofetcher(hashes, chunksize)
		nicedict = resultsformatter(roughlist)
		#combines two dicts
		finaldict = {**finaldict, **nicedict}
		hashes = [x for x in hashlist if x not in finaldict.keys()]
		chunksize = math.ceil(chunksize/3)
	return(finaldict, hashes)


if __name__ == "__main__":
	#makes sure we are up to date with our files
	cacheupdate()
	#populate our list with filenames and hashes
	mainlist = torrentsandhashes(test=True)
	#pull just hashes
	hashes = [x[1] for x in mainlist]
	#pass hashes, return dict of seed/leech info

	#chunksize = sys.argv[1]
	#trials = sys.argv[2]
	print(type(20))

	finaldict, unfetched = seedfetchingmaster(hashes, 20, 4)

	len(unfetched)
	tocheck = [x for x in mainlist if x[1] in unfetched]
	print(tocheck)