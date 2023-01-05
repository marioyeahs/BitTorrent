import asyncio, sys

class Peer(object):
    def __init__(self,host,port,file_queue):
        self.host = host
        self.port = port
        self.file_queue = file_queue

        # Denotes if peer is choking us
        self.peer_choking = True

        # Denotes if we hve informed our peer that we are interested
        self.am_interested = False

    async def downloaded(self):
        reader, writer = await asyncio.open_connection(
            self.host, self.port
        )
        handshake = b' '.join([
            chr(19).encode(),
            b'BitTorrent protocol',
            (chr(0) * 8).encode(),
            info_hash,
            PEER_ID.encode()
        ])

        # Send handshake
        writer.write(handshake)
        await writer.drain()

        # Read and validate response
        peer_handshake = await reader.read(68)
        self.validate(peer_handshake)

        # Start exchanging messages...

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

