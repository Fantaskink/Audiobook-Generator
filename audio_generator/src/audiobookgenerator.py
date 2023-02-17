from dotenv import load_dotenv
import os
import requests
from pydub import AudioSegment

load_dotenv()

API_KEY = os.environ.get("API_KEY")

voice_id = "HqIDqJGhZr3ntQ0HY2FU"

url = "https://api.elevenlabs.io"

header = {
    "xi-api-key": API_KEY
}

def get_number(filename):
    return int(filename.split('.')[0][-1])

def load_and_merge_mp3s():

    directory = "./output"

    # Get a list of all mp3 files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.mp3')]

    # Sort the files based on the number at the end of their filename
    files.sort(key=lambda x: int(x.split('.')[0][-1]))

    # Load the audio segments
    audio_segments = [AudioSegment.from_file(os.path.join(directory, f), format='mp3') for f in files]

    # Concatenate the audio segments into a single audio file
    merged_audio = audio_segments[0]
    for audio_segment in audio_segments[1:]:
        merged_audio = merged_audio + audio_segment

    output_file = os.path.join(directory, 'merged.mp3')
    merged_audio.export(output_file, format='mp3')

def get_book_lines():
    lines = []
    with open('./book/americanpsycho.txt', 'r') as file:
        for line in file:
            if line != "\n":
                lines.append(line.strip())
                
    return lines


def get_tts(string, number):
    body = {
    "text": string,
    "voice_settings": {
    "stability": 0.4,
    "similarity_boost": 0.85
        }
    }
    response = requests.post(url + f"/v1/text-to-speech/{voice_id}", headers=header, json=body)

    # Check if the request was successful
    if response.status_code == 200:
        # Open a file to write the audio content
        with open(f'./output/line{i}.mp3', 'wb') as f:
            # Write the audio content to the file
            f.write(response.content)
        print('Audio file saved successfully!')
    else:
        print(f'Request failed with status code {response.status_code}')

lines = get_book_lines()

for line in lines:
    get_tts(line, lines.index(line))

load_and_merge_mp3s()