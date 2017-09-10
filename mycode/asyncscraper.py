
import aiohttp
import asyncio

#https://gist.github.com/thelastpenguin/a14c48180f733096a22df5e07a15730e

async def fetch(session, url):
    with aiohttp.Timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def fetch_all(session, urls, loop):
    results = await asyncio.gather(
        *[fetch(session, url) for url in urls],
        return_exceptions=True  # default is false, that would raise
    )

    # for testing purposes only
    # gather returns results in the order of coros
    for idx, url in enumerate(urls):
        print('{}: {}'.format(url, 'ERR' if isinstance(results[idx], Exception) else 'OK'))
    return results

def download_urls(urls): # returns a dictionary mapping a url -> result text
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        the_results = loop.run_until_complete(
            fetch_all(session, urls, loop))
        return(the_results)