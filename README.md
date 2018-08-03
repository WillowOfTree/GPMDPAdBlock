# GPMDPAdBlock
AdBlock for Google Play Music Desktop Player
### Why?
I hate ads, I wanted less of them in my music.
### How?
Starts an HTTPS proxy on the localhost that causes YouTube's ad servers to return a 404
##
This server is not meant to be used in any sort of application besides [GPMDP](https://github.com/MarshallOfSound/Google-Play-Music-Desktop-Player-UNOFFICIAL-), seeing as it tries to launch the program once the proxy is up and running. The proxy is also set to shut down as soon as you quit the client.

## Requirements:
* Python 2.x
* [GPMDP](https://github.com/MarshallOfSound/Google-Play-Music-Desktop-Player-UNOFFICIAL-)
* `psutil >= 5.4.6`

This program only works on Windows right now, I might start trying to get it to work on Linux and Mac

## Installation:
Just install the requirements and run the script, unless you want to download the EXE I'll have packaged in the releases.
If you want to install the EXE, just download it and run it from wherever, there's nothing to setup, it looks in the default installation directory ~~not sure if you can even change it~~, and runs the updater with the proxy. If you find a host that I don't have blocked, post it in issues, I'll update the blacklist.

## Credits:
[GPMDP](https://github.com/MarshallOfSound/Google-Play-Music-Desktop-Player-UNOFFICIAL-) is amazing, I love it, and I support that they don't want to add adblock natively. I just don't want ads.
[inaz2/proxy2](https://github.com/inaz2/proxy2/) was the base for the proxy, just slimmed down to the point it didn't error.
Basically all of Reddit for the hosts, they're pretty good at linking them to people.
