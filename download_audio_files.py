import urllib.parse
import json
import sys
import subprocess
import os
import time


if __name__ == '__main__':
    data_filepath = sys.argv[1]
    audio_directory = sys.argv[2]

    with open(data_filepath) as f:
        data = json.load(f)

   
    if not os.path.isdir(audio_directory):
        os.mkdir(audio_directory)

    for entry in data:
        word = entry['word']
        
        audio_filename = f"{word}.mp3"
        audio_filepath = f"{audio_directory}/{audio_filename}"

        if os.path.isfile(audio_filepath):
            continue
        
        print(f"downloading audio for {word}")

        url_params = urllib.parse.urlencode({"ie": "UTF-8", "client": "tw-ob", "tl": "zh-CN", "q": word})

        subprocess.run(["wget", f"https://translate.google.com/translate_tts?{url_params}", "-O", audio_filepath], check=True)

        time.sleep(5)
