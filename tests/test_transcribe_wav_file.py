import aiohttp
import json
from pydub import AudioSegment
from io import BytesIO

import pytest

from logic.rhasspy_client import RhasspyClient

@pytest.mark.asyncio
async def test_transcribe_wav_file():
    # Download WAV files
    urls = [
        "https://evolution.voxeo.com/library/audio/prompts/numbers/0.wav",
        "https://evolution.voxeo.com/library/audio/prompts/numbers/1.wav",
        "https://evolution.voxeo.com/library/audio/prompts/numbers/2.wav",
        "https://evolution.voxeo.com/library/audio/prompts/numbers/3.wav",
        "https://evolution.voxeo.com/library/audio/prompts/numbers/4.wav",
        "https://evolution.voxeo.com/library/audio/prompts/numbers/5.wav",
    ]
    files = []
    
    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        for url in urls:
            async with session.get(url) as response:
                assert response.status == 200
                data = await response.read()
                audio_segment = AudioSegment.from_file(BytesIO(data))
                audio_segment = audio_segment.set_frame_rate(16000)
                audio_segment = audio_segment.set_channels(1)
                audio_segment = audio_segment.set_sample_width(2)
                wav_data = audio_segment.export(format="wav").read()
                files.append(wav_data)

    # Initialize RhasspyClient
    client = RhasspyClient("http://localhost",12101,"/api")

    # Transcribe WAV files
    expected_results = ["zero", "one", "two", "three", "four", "five"]
    for i, file in enumerate(files):
        result = await client.transcribe_wav_file(file)
        response_dict = json.loads(result)
        response = response_dict["text"]
        print(f"Transcribed text: {response}")
        assert response == expected_results[i]
