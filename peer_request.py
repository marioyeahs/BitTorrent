import aiohttp

torrent = get_torrent_file()

async def request_peers(self):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(tracker_url, params=params)
        resp_data = await resp.read()
        peers = bencoder.decode(resp_data)
        return peers