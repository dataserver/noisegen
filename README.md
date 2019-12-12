# noisegen
It's an audio mixer 10 audio files playing in an infinite loop.
I use to create white noise.


# config.ini
collection_dir = ./subdirectory_with_albums/
album_dir = ENLIA
volume = 40
auto_play = 1

- create a data.json file about the album.

# data.json
supported [audio formats](http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound)
``
{
    "title": "The album's name",
    "files": [
        {
            "channel": 0,
            "title": "Sub-bass",
            "file": "0a.ogg"
        },
        {
            "channel": 1,
            "title": "Low Bass",
            "file": "1a.ogg"
        },
...
``

# Volume control
- Use a logarithmic scale

