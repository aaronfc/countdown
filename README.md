countdown
=========
Countdown application used during HackMeUps at [Tuenti](http://www.tuenti.com).

## STATUS
[PoC](https://en.wikipedia.org/wiki/Proof_of_concept)

## TODO (by priority)
- [ ] Prepare to listen to ExternalEvents (REST API)
- [ ] Improve UI (shortcuts)
- [ ] Figure out how the h#!% the imports should work to avoid ./run script
- [ ] Add proper logging
- [ ] Add minimal testing
- [ ] Cleanup hearts code and isolate logic from representation
- [ ] Isolate access to config.py

## Whishlist
- [ ] Support negative feedback (broken hearts or smiley shits)
- [ ] Allow text comments (maybe spoken?)
- [ ] Clap-o-meter (mic)
- [ ] Sync data from spreadsheet

## Troubleshoot on fresh install
- You need to install python-pygame dependencies.
`sudo apt-get build-dep python-pygame`
NOTE: You might need to enable deb-src on your `/etc/apt/sources.list`
- You need to install cython manually. Dependencies on requirements.txt doesn't seem to work :(
`pip install cython`
- You need to install kivy dependencies. Take a look at: https://kivy.org/docs/installation/installation.html
`sudo apt-get install python-setuptools python-pygame python-opengl \
  python-gst0.10 python-enchant gstreamer0.10-plugins-good python-dev \
  build-essential libgl1-mesa-dev libgles2-mesa-dev zlib1g-dev python-pip`
- Link correctly GL library.
`sudo ln -s /usr/lib/libGL.so.1 /usr/lib/libGL.so`
