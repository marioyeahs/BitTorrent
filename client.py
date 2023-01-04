import asyncio, sys

async def download(torrent_file):
	
    # Read and parse ".torrent" file
    torrent = read_torrent(torrent_file)
    
    # Get peers list from tracker in ".torrent" file 
    peers_addresses = await get_peers(torrent_file)

    # Queue for storing downloaded file pieces
    file_pieces_queue = asyncio.Queue()

    # Object to coordinate writing file to disk
    file_saver = FileSaver(file_pieces_queue)

    # Object to track peers communication/state
    peers = [Peer(addr, file_pieces_queue) for addr in peers_addresses]

    # Wait for all download coroutines to finish
    await asyncio.gather(
            *([peer_download() for peer in peers] +  # Producer
            [file_saver.start()])                    # Consumer
        ) 

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download(sys.argv[1]))
    loop.close()

