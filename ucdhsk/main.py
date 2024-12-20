import genanki
import json
import logging
import os
import pinyin_jyutping
import subprocess
import sys
import time
import urllib.parse

logger = logging.getLogger(__name__)

VERSION = "2.0.0"

CSS="""

hr {
 height: 3px;
 margin-top: 20px;
 margin-bottom: 20px;
}


.hanzi {
 font-family: Kai;  
 font-size: 3rem;
 margin-top: 20px;
}

.hanzi-smaller {
 font-family: Kai;  
 font-size: 2rem;
 margin-top: 20px;
}

.pinyin {
 font-family: Palatino; 
 font-size: 2rem; 
 color: magenta;
}

.card {
  padding: 1rem;
}

img {
max-width: 300px;
max-height: 250px;
}

.mobile img {
max-width: 50vw;
}

"""

def download_audio_files():
    data_filepath = sys.argv[1]
    audio_directory = sys.argv[2]

    with open(data_filepath) as f:
        data = json.load(f)
   
    if not os.path.isdir(audio_directory):
        os.mkdir(audio_directory)

    for entry in data:
        word = entry['word']
        identifier = entry['id'] 
        audio_filename = f"{identifier}.mp3"
        audio_filepath = f"{audio_directory}/{audio_filename}"

        if not os.path.isfile(audio_filepath):
            print(f"downloading audio for {word}")
            url_params = urllib.parse.urlencode({"ie": "UTF-8", "client": "tw-ob", "tl": "zh-CN", "q": word})
            subprocess.run(["wget", f"https://translate.google.com/translate_tts?{url_params}", "-O", audio_filepath], check=True)
        
            time.sleep(5)
        
        sentence = entry.get('sentence')
        if sentence:
            audio_filename = f"{identifier}_sentence.mp3"
            audio_filepath = f"{audio_directory}/{audio_filename}"

            if not os.path.isfile(audio_filepath):
                print(f"downloading audio for sentence {sentence}")
                url_params = urllib.parse.urlencode({"ie": "UTF-8", "client": "tw-ob", "tl": "zh-CN", "q": sentence})
                subprocess.run(["wget", f"https://translate.google.com/translate_tts?{url_params}", "-O", audio_filepath], check=True)

                time.sleep(5)


def reset_ids():
    data_filepath = sys.argv[1]
    identifier = 10000

    with open(data_filepath) as f:
        data = json.load(f)

    p = pinyin_jyutping.PinyinJyutping()
    for entry in data:
        entry['id'] = identifier
        identifier += 1

    with open(data_filepath, "wt") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True))


def pinyinfy():
    data_filepath = sys.argv[1]

    with open(data_filepath) as f:
        data = json.load(f)

    p = pinyin_jyutping.PinyinJyutping()
    for entry in data:
        word = entry['word']
        pinyin = entry.get('word_pinyin')
        if not pinyin:
            entry['word_pinyin'] = p.pinyin(word)

        if 'sentence' in entry:
            sentence = entry['sentence']
            pinyin = entry.get('sentence_pinyin')
            if not pinyin:
                entry['sentence_pinyin'] = p.pinyin(sentence)

    with open(data_filepath, "wt") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True))


class MyNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


def check_images():
    data_filepath = sys.argv[1]
    image_directory = sys.argv[2]

    # Generate the notes
    with open(data_filepath) as f:
        data = json.load(f)

    for entry in data:
        image_name = entry.get('image')
        if not image_name:
            image_name = input(f"Image name for {entry['word']} - {entry['meaning']}: ")
            entry['image'] = image_name.strip()

        image_filepath = f"{image_directory}/{image_name}"
        if not os.path.isfile(image_filepath):
            logger.error("missing image for %s (id=%d): %s", entry['word'], entry['id'], image_name)

        with open(data_filepath, "wt") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True))


def make_deck():
    data_filepath = sys.argv[1]
    sounds_directory = sys.argv[2]
    images_directory = sys.argv[3]

    model = genanki.Model(
        31894723897492,
        name="UCD HSK 1.1",
        fields=[
            {'name': "Word"},
            {'name': "WordPinyin"},
            {'name': "WordMeaning"},
            {'name': "WordSound"},
            {'name': "Sentence"},
            {'name': "SentencePinyin"},
            {'name': "SentenceMeaning"},
            {'name': "SentenceSound"},
            {'name': "Image"},
        ],
        templates=[
            {
                "name": "Standard",
                "qfmt": """<span class=\"hanzi\">{{Word}}</span><br>
                {{#Sentence}}
                <hr id=\"answer\">
                <span class=\"hanzi-smaller\">{{Sentence}}</span><br>
                {{/Sentence}}
                """,
                "afmt": """<span class=\"hanzi\">{{Word}}</span><br>
                <div class=\"pinyin\">{{WordPinyin}}</div><br>
                {{WordMeaning}}<br>
                {{WordSound}} <br>
                {{#Sentence}}
                <hr id=\"answer\">
                <span class=\"hanzi-smaller\">{{Sentence}}</span><br>
                <div class=\"pinyin\">{{SentencePinyin}}</div><br>
                {{SentenceMeaning}}<br>
                {{SentenceSound}}
                </br>
                {{/Sentence}}
                {{#Image}}{{Image}}{{/Image}}"""
            }
        ],
        css=CSS
    )

    deck = genanki.Deck(1337, name="UCD HSK 1.1 Vocab")

    # Generate the notes
    with open(data_filepath) as f:
        data = json.load(f)

    media_files = []
    for entry in os.listdir(sounds_directory):
        if entry.endswith(".mp3"):
            media_files.append(f"{sounds_directory}/{entry}")

    for entry in os.listdir(images_directory):
        entry_path = f"{images_directory}/{entry}"
        if os.path.isfile(entry_path):
            media_files.append(entry_path)

    for entry in data:
        word = entry["word"]
        identifier = entry['id']
        fields = [word, entry["word_pinyin"], entry["word_meaning"], f"[sound:{identifier}.mp3]"]

        sentence = ""
        sentence_pinyin = ""
        sentence_meaning = ""
        sentence_sound = ""
        if 'sentence' in entry:
            sentence = entry['sentence']
            sentence_pinyin = entry['sentence_pinyin']
            try:
                sentence_meaning = entry['sentence_meaning']
            except:
                print(sentence)
                raise

            sentence_sound = f"[sound:{identifier}_sentence.mp3]"
            
        fields.extend([sentence,sentence_pinyin, sentence_meaning, sentence_sound])

        image_name = entry.get("image", "") 
        if image_name:
            image_field = f"<img src=\"{image_name}\"/>"
        else:
            image_field = ""
        fields.append(image_field)

        note = MyNote(model=model, fields=fields)
        deck.add_note(note)

    pkg = genanki.Package(deck)
    pkg.media_files = media_files
    filename = (deck.name + " " + VERSION).replace(' ', '.')
    pkg.write_to_file(f"{filename}.apkg")
