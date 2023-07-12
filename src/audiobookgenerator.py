from dotenv import load_dotenv
import os
import requests
from PyPDF2 import PdfReader


load_dotenv()

API_KEY = os.environ.get("API_KEY")

voice_id = "HqIDqJGhZr3ntQ0HY2FU"

url = "https://api.elevenlabs.io"

header = {
    "xi-api-key": API_KEY
}

def get_book_lines():
    reader = PdfReader('book/Bret Easton Ellis - American Psycho  -Vintage (1991).pdf')
    number_of_pages = len(reader.pages)

    extracted_pages = []
    lines = []

    for page in reader.pages:
        extracted_text = page.extract_text()
        split_text = extracted_text.split('\n')
        extracted_pages.append(split_text)
    
    for page in extracted_pages:
        for line in page:
            lines.append(line)
    
    return lines

def merge_strings(strings):
    i = 0
    while i < len(strings) - 1:
        if strings[i][-2:] not in [".", "!", "?"] and strings[i][-1].isspace():
            merged_string = strings[i][:-1] + strings[i+1]
            if strings[i][-1] == ' ' or strings[i+1][0] == ' ':
                merged_string = strings[i][:-1] + ' ' + strings[i+1]
            strings[i] = merged_string
            strings.pop(i+1)
        else:
            i += 1
    return strings



def write_text_file(lines):
    # Open the file in write mode with truncate
    file = open("output/book/americanpsycho.txt", "w")

    # Write some strings to the file
    for line in lines:
        file.write(line + '\n')
        

    # Close the file when finished
    file.close()


def get_tts(string, line_count):
    digit_count = len(str(line_count))
    body = {
    "text": string,
    "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.85
        }
    }
    
    response = requests.post(url + f"/v1/text-to-speech/{voice_id}", headers=header, json=body)

    # Check if the request was successful
    if response.status_code == 200:
        # Open a file to write the audio content
        with open(f'./output/audio/line{i:0{digit_count}d}.mp3', 'wb') as f:
            # Write the audio content to the file
            f.write(response.content)
        print(f'Audio file {i} saved successfully!')
    else:
        print(f'Request failed with status code {response.status_code}')

lines = get_book_lines()
lines = merge_strings(lines)
write_text_file(lines)
line_count = len(lines)

for i in range(0,20):
    get_tts(lines[i], line_count)
    print(lines[i] + '\n')
    