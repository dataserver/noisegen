# noisegen
Python program (GUI/PySide2)
It's just an audio mixer of 10 audio files playing in an infinite loop.  
I use to create white noise because mixing 10 different audio can only create noises :D

# screenshot

![GUI Screenshot](https://github.com/dataserver/noisegen/blob/master/screenshot.png?raw=true "Gui screenshot")

# config.ini
```
collection_dir = ./audioset/
album_dir = DEMO
volume = 40
auto_play = 1
```

The program will scan the collection_dir for subdirectories and try to read 'data.json' file inside.

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
```

# Volume control
- Use a logarithmic scale
