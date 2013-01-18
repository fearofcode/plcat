plcat
=====

plcat is a quick hack to add the contents of one YouTube playlist to one of your own from the terminal using Google's API. I couldn't find any way to do it with the current YouTube layout, hence this.

License
-------

See LICENSE.

Warning
-------

This is not robust software. It's "works on my machine" quality. I used it once and figured I'd share it because it deserves a little more than a Gist. There are so many things that can go wrong and it's like 3 in the morning as I'm typing this. This is that kind of software.

If someone wants to make this code less crappy (?) I'd of course be more than happy to accept pull requests.

Setup
-----

You'll need to make your own Google app in their API console, then download the client JSON file Google gives you in the same directory as this file. Basically, follow [the getting started instructions](https://developers.google.com/youtube/v3/getting-started) step by step. It might be confusing if you've never worked with Google's APIs before.

I set the callback URL to be `http://localhost:8080`.

The playlist you add to has to be one in your own account.

The first time you run this, the terminal should open a new browser window prompting you to grant access to this app. Click the button to allow this. It should then say something to the effect of "authorization flow completed" at which point the program should get to work.

Usage
-----

    Usage: plcat.py [options]
    
    Options:
      -h, --help   show this help message and exit
      --src=SRC    ID of source playlist to copy videos from
      --dest=DEST  ID of destination playlist to copy videos to

You can get these IDs from URLs in your browser. As of late 2012/early 2013, they should begin with `PL` or `AL`.

YouTube playlists can currently only handle 200 videos, so presumably some kind of error should occur if that condition is reached.

Sample output
-------------

Here is sample usage when trying to add a playlist of videos by an artist to an existing playlist of my own.

    warren@aurora:~/code/plcat$ python plcat.py --src=AL94UKMTqg-9DcfNysOS85s9PFm8r29meQ --dest=PLRZA2rkwJxAgXio3GY-zok0eKHiR_qyRi
    Trying to fetch contents of playlist with id AL94UKMTqg-9DcfNysOS85s9PFm8r29meQ
    Got 99 videos. Add to playlist with id PLRZA2rkwJxAgXio3GY-zok0eKHiR_qyRi? [Y/n]Y
    Trying to add video with id FkEAT69T8pA, title Xasthur- Entrance Into Nothingness (Intro Instrumental)
    Trying to add video with id av0TP3q8vEs, title Xasthur - Summon The End Of Time
    Trying to add video with id hkhs7KzgEAg, title Xasthur - This Abyss Holds the Mirror - Portal of Sorrow
    [ ... 96 more lines omitted for the sake of brevity... ]
    Done.

