import aiohttp

class RhasspyClient:
    def __init__(self, host: str = "http://localhost", port: int = 12101, endpoint: str = "/api"):
        self.host = host
        self.port = port
        self.endpoint = endpoint
        self.url = f"{host}:{port}{endpoint}"

    
    async def transcribe_wav_file(self, wav_data: bytes) -> str:
        url = f"{self.url}/speech-to-text"
        headers = {"Content-Type": "audio/wav"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=wav_data) as response:
                text = await response.text()
            return text

    def listen(self):
        # TODO: Start listening for voice input and return the recognized text
        return

