# noisegen
Python program (GUI/PySide2)
It's just an audio mixer of 10 audio files playing in an infinite loop.  
I use it to create white noise by mixing 10 different audio channels, each channel with unique
audio sound :D

# screenshot

![GUI Screenshot](https://github.com/dataserver/noisegen/blob/master/screenshot.png?raw=true "Gui screenshot")

# installation
pip install -r requirements.txt  
or  
poetry install

# running
python main.py


# config.json
```
{
    "collection_folder": "audioset/",
    "default_album_folder": "DEMO",
    "default_channel_volume": 40,
    "auto_play": true

    "svg_path": "src/svg/",
    "svg_btn_pause": "btn_pause.svg",
    "svg_btn_play": "btn_play.svg",
    "svg_btn_stop": "btn_stop.svg",
    "svg_app_icon": "icon.svg"
}
```

The program will scan the collection_folder for folders and try to read 'data.json' file inside.
No need to edit any svg_* configuration.

# data.json
Check data.json file inside the DEMO folder.
- supported [audio formats](http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound)
```
{
    "title": "DEMO Rain in the Forest",
    "files": [{
            "channel": 0,
            "title": "thunderstorm",
            "file": "0.ogg"
        },
        {
            "channel": 1,
            "title": "muffled thunderstorm",
            "file": "1.ogg"
        },
        ...
...
```

# Volume control
- Use a logarithmic scale
