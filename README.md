# UCD HSK Anki Deck

I started UCD's HSK 1.1 class on October 2024 and wanted a better way to memorize the vocab learned in classes.
This repository contains the code needed to generate an Anki deck programatically.

The program is fed the `data.json` file to do its work.

Images and sound assets are not included with this repository because copyright (even though they are inside the deck package, meh).

## How do I use this?

My main goal with learning Chinese is to be able to read, so the cards emphasize that.

The front of the card has the word (or sentence) written in Chinese characters:

![](_assets/front.png)


The back of the card shows you the reading (pinyin), the meaning, and an audio file so you can hear it. 

![](_assets/back.png)

Most cards have an image included to help associate the character with the meaning.

## How do I get the Anki deck?

Head to the [releases page](https://github.com/ltadeut/ucd-hsk-anki-deck/releases) and look for the latest version.

You'll want to download the file ending in `.apkg`. That's the Anki package containing the deck.

Once you have the file it's just a matter of importing the deck.

## Caveats

### Pinyin

I was lazy to go one by one so I wrote a program to generate the Pinyin reading
from the Chinese characters. It should be correct for the most part, but the
reading is picked based on probability (more frequent readings in common speech
take precedence) so there may be mistakes.

I did a quick pass over them and they seemed correct enough.

Use that to check your knowledge ;)
