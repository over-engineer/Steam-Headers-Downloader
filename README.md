# Steam Headers Downloader
A script to download Steam header images

## Usage
Run it using `python steam_headers_download.py`. You need [Python 2.7](https://www.python.org/download/releases/2.7/) to run this script.

## How does it work?
It basically gets a list of the games you own using your username `http://steamcommunity.com/id/[username]/games?tab=all&xml=1` and then downloads the header image of each game from `http://cdn.akamai.steamstatic.com/steam/apps/[appID]/header.jpg`

## Why is it useful?
I use [OblyTile](http://forum.xda-developers.com/showthread.php?t=1899865) to pin tiles for my Steam games. I wrote this script to get the header images of my games, so I can use them as tiles on my Windows 8.1 start screen.

## License
The MIT License, check the **LICENSE** file.

*Steam headers downloader* is not affiliated with Steam or Valve Corporation. Valve and Steam are trademarks and/or registered trademarks of Valve Corporation.
