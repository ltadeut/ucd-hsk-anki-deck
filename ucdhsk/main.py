import pinyin_jyutping
import json
import sys
import os
import genanki

CSS="""

hr {
 height: 3px;
 border: none;
 margin-top: 20px;
 margin-bottom: 20px;
}


.hanzi {
 font-family: Kai;  
 font-size: 3rem;
 margin-top: 20px;
}

.pinyin {
 font-family: Palatino; 
 font-size: 2rem; 
 color: magenta;
}

.card {
  padding: 2rem;
  text-align: center;
}

img {
max-width: 300px;
max-height: 250px;
}

.mobile img {
max-width: 50vw;
}

"""

def pinyinfy():
    data_filepath = sys.argv[1]
    output_filepath = sys.argv[2]

    with open(data_filepath) as f:
        data = json.load(f)

    p = pinyin_jyutping.PinyinJyutping()
    for entry in data:
        hanzi = entry['hanzi']

        pinyin = entry.get('pinyin')
        if not pinyin:
            entry['pinyin'] = p.pinyin(hanzi)


    with open(output_filepath, "wt") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


class MyNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


def check_images():
    data_filepath = sys.argv[1]


    # Generate the notes
    with open(data_filepath) as f:
        data = json.load(f)

    for entry in data:
        image_filepath = entry.get('image')
        if not image_filepath:
            continue

        if not os.path.isfile(image_filepath):
            input(f"missing file {image_filepath}...")


def make_deck():
    data_filepath = sys.argv[1]
    sounds_directory = sys.argv[2]
    images_directory = sys.argv[3]

    model = genanki.Model(
        31894723897492,
        name="UCD HSK 1.1",
        fields=[
            {'name': "Hanzi"},
            {'name': "Pinyin"},
            {'name': "Meaning"},
            {'name': "Sound"},
            {'name': "Image"},
        ],
        templates=[
            {
                "name": "Standard",
                "qfmt": "<span class=\"hanzi\">{{Hanzi}}</span>",
                "afmt": """{{FrontSide}}
                <hr id=\"answer\">
                <div class=\"pinyin\">{{Pinyin}}</div>
                <br>

                {{Meaning}}

                </br>
                </br>
                {{Sound}}
                </br>
                </br>
                {{#Image}}{{Image}}{{/Image}}"""
            }
        ],
        css=CSS
    )

    deck = genanki.Deck(1337, name="UCD HSK 1.1 Vocab - V1")

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
        hanzi = entry["hanzi"]
        identifier = entry['id']
        fields = [hanzi, entry["pinyin"], entry["meaning"], f"[sound:{identifier}.mp3]"]
        image_filepath = entry.get("image") 

        image_field = ""
        if image_filepath:
            _, _, image_name = image_filepath.partition("/")
            image_field = f"<img src=\"{image_name}\"/>"
        fields.append(image_field)


        note = MyNote(model=model, fields=fields)
        deck.add_note(note)

    pkg = genanki.Package(deck)
    pkg.media_files = media_files
    pkg.write_to_file(f"{deck.name}.apkg")
