# noisegen
Python program (GUI/PySide2)
It's just an audio mixer of 10 audio files playing in an infinite loop.  
I use it to create white noise by mixing 10 different audio channels, each channel with unique
audio sound :D

## screenshot

![GUI Screenshot](screenshot.png?raw=true "Gui screenshot")


## installation

    pip install -r requirements.txt  

or  

    poetry install

## running

    python main.py


## config.json
```
{
    "collection_folder": "audioset/",
    "default_album_folder": "DEMO",
    "default_channel_volume": 40,
    "auto_play": true

    "svg_path": "resources/svg/",
    "svg_btn_pause": "btn_pause.svg",
    "svg_btn_play": "btn_play.svg",
    "svg_btn_stop": "btn_stop.svg",
    "svg_app_icon": "icon.svg"
}
```

The program will scan the collection_folder for folders and try to read 'data.json' file inside.
No need to edit any svg_* configuration.

## data.json
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

## build .exe

    pyinstaller app.spec



## License ##
---

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.