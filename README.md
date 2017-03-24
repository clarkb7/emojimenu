# emojimenu

Select emoji using [dmenu](http://tools.suckless.org/dmenu/) and send to
clipboard using [xsel](http://www.vergenet.net/~conrad/software/xsel/) or
auto-type using [xdotool](http://www.semicomplete.com/projects/xdotool).

## Configuration
Configured emoji are stored in `~/.config/emojimenu/emoji.cfg`.

A simple [sample config](emojimenu/emoji.cfg) is installed automatically.

## Usage
```
usage: emojimenu [-h] [-c PATH] [-t] [-d ms] [-x {p,s,b} [{p,s,b} ...]]

Select and type emoji with dmenu

optional arguments:
  -h, --help            show this help message and exit
  -c PATH, --cfg PATH   Config and emoji file
  -t, --type            Auto-type emoji using xdotool
  -d ms, --delay ms     Delay between typing each character (ms)
  -x {p,s,b} [{p,s,b} ...], --clipboards {p,s,b} [{p,s,b} ...]
                        List of xsel clipboards to copy to
```
