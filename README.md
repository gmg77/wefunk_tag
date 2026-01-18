# wefunk_tag
Python script to use JSON file to retag MP3 files obtained from wefunkradio.com

WEFUNK is a Hip Hop, Funk & Soul mix show broadcasting from Montreal. Tune in and enjoy underground hip hop, classic funk and rare grooves.

Prerequisites
-------------
* JSON file see https://github.com/gmg77/wefunk_pl
* Python
* mutagen library

Quickstart
--------------
1. Script will read the JSON file containing all the show data.
2. Scan a sub directory named mp3s for matching files (based on the filename structure frome wefunkradio.com)
3. Format the show information (DJs, description, playlist) into a readable text block and write that text block into the ID3 tag of the MP3 file.
4. output txt file work summary
5. output nfo file for each mp3

pip install mutagen

python wefunktag.py

select JSON file at prompt

Shoutouts
------
Professor Groove, DJ Static and the wefunkradio crew for brining the funk soul and hiphop since 1996!

https://wefunkradio.com
