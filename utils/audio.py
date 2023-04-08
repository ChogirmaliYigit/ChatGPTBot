import openai
import requests

openai.api_key = "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"

file_path = "utils/audio_file.wav"
audio_file = open(file_path, "rb").read()

data = {
    'file': audio_file,
    "model": "whisper-1"
}

response = requests.post(
    "https://api.openai.com/v1/audio/transcriptions",
    headers={
        "Content-Type": "application/octet-stream",
        "Authorization": f"Bearer {openai.api_key}",
    },
    data=data,
)

print(response.json())
