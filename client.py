import asyncio, sys

async def download(torrent_file):
	
    # Read and parse ".torrent" file
    torrent = read_torrent(torrent_file)
    
    # Get peers list from tracker in ".torrent" file 
    peers_addresses = await get_peers(torrent_file)

    # Object to track peers communication/state
    peers = [Peer(addr) for addr in peers_addresses]

    # Wait for all download coroutines to finish
    await asyncio.gather(
            *[peer_download() for peer in peers] # Producer
        ) 

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download(sys.argv[1]))
    loop.close()

