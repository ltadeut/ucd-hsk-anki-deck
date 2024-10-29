# UCD HSK Anki Deck

I started UCD's HSK 1.1 class in October 2024 and wanted a way to memorize the vocab learned in classes.
This repository contains the code needed to generate the deck programatically.

The program is fed the `data.json` file in the root of this directory to do its work.

Images and sound assets are not included with this repository due to prevent any copyright trouble
(even though they are inside the deck package, meh).

## How does this work?

My main goal with learning Chinese is to be able to read, so the cards emphasize that.

The front of the card has the word (or sentence) written in Chinese characters:

![](_assets/front.png)


The back of the card shows you the reading (pinyin), the meaning, and an audio file so you can hear it. 

![](_assets/back.png)

Most cards have an image included to help associate the character with the meaning.

## How do I get the Anki deck?

## Caveats

### Pinyin

I was lazy to go one by one so I wrote a program to generate the Pinyin reading
from the Chinese characters. It should be correct for the most part, but the
reading is picked based on probability (more frequent readings in common speech
take precedence), so it might not always be correct.

Use that to check your knowledge ;)
