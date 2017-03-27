#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from os.path import expandvars
import argparse
import configparser
try:
    from emoji.unicode_codes import EMOJI_UNICODE, EMOJI_ALIAS_UNICODE
    _process_emoji_dic = lambda dic: set([(x.replace(':', ''), y) for x,y in dic.items()])
    IMP_EMOJI = _process_emoji_dic(EMOJI_UNICODE)
    IMP_EMOJI |= _process_emoji_dic(EMOJI_ALIAS_UNICODE)
    IMP_EMOJI = list(IMP_EMOJI)
except ImportError:
    IMP_EMOJI = []

XSEL_CLIPBOARDS=['p', 's', 'b']

def parse_cfg(cfg_path):
    config = configparser.ConfigParser()
    config.read(expandvars(cfg_path))
    return config

def dmenu_format(choices, fmt=None):
    """Format iterable @choices into '\n' delimited dmenu input
    Arguments:
        fmt - Format string for each key:choice pair
    """
    if fmt is None:
        fmt = '{}: {}'
    dmenu_line = ''
    for c in choices:
        dmenu_line += (fmt+'\n').format(c[0], c[1])
    return dmenu_line

def dmenu_select(line, dmenu_opts=None):
    """Send @line to dmenu and return selection"""
    if dmenu_opts is None:
        dmenu_opts = ['-i']
    p = Popen(['dmenu'] + dmenu_opts, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
    out,err = p.communicate(line.encode('utf-8'))
    return out.decode('utf-8')

def extract_name(choice, extract=None):
    """Extract emoji name from dmenu @choice"""
    if extract is None:
        def _extract(c):
            return c.split(':')[0]
        extract = _extract
    return extract(choice)

def get_emoji_by_name(emoji, name):
    """Lookup @name key in iterable @emoji and return value"""
    try:
        return list(filter(lambda x: x[0] == name, emoji))[0][1]
    except IndexError:
        return ''

def do_type(data, delay=None):
    """Type @data under cursor using xdotool
    Arguments:
        delay - delay between characters (ms)
    """
    if delay is None:
        delay = 50
    p = Popen(['xdotool', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
    p.stdin.write(("type --clearmodifiers --delay {} -- '{}'".format(delay, data)).encode('utf-8'))

def do_copy(data, clipboards=None):
    """Send @data to clipboards using xsel"""
    if clipboards is None:
        clipboards = XSEL_CLIPBOARDS
    for cb in clipboards:
        p = Popen(['xsel', '-'+cb, '-i'], stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        p.communicate(data.encode('utf-8'))

def main():
    # Parse arguments
    p = argparse.ArgumentParser(description='Select and type emoji with dmenu')
    p.add_argument("-c", "--cfg", metavar='PATH',
        help='Config and emoji file',
        default='$HOME/.config/emojimenu/emoji.cfg')
    p.add_argument("-t", "--type", action='store_true',
        help='Auto-type emoji using xdotool')
    p.add_argument("-d", "--delay", metavar='ms',
        help='Delay between typing each character (ms)',
        type=int, default=None)
    p.add_argument("-x", "--clipboards", nargs='+', choices=XSEL_CLIPBOARDS,
        help='List of xsel clipboards to copy to')
    args = p.parse_args()

    # Read config file
    cfg = parse_cfg(args.cfg)
    emoji_list = cfg.items('emoji') + IMP_EMOJI

    # Build input line
    line = dmenu_format(emoji_list)

    # Spawn process and get selection
    choice = dmenu_select(line)

    # Select emoji
    name = extract_name(choice)
    choice = get_emoji_by_name(emoji_list, name)

    # Type emoji under cursor or copy to clipboards
    if args.type:
        do_type(choice, args.delay)
    else:
        do_copy(choice, args.clipboards)

if __name__ == "__main__":
    main()

