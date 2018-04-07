#!/usr/bin/env python

# ################################################################################
#
# Steam Headers Downloader
# A script to download Steam header images
#
# ################################################################################
#
# v0.1: 	2015-04-29
# v0.1.1: 	2015-04-30
# v0.1.2:   2018-03-06
#
# ################################################################################
#
# The MIT License (MIT)
#
# Copyright (c) 2015-2018 Dinos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ################################################################################

import os
import sys
import urllib
import xml.etree.ElementTree as ET

from retries import retries, retry_exc_handler


def get_valid_filename(name):
    valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-+!.,\'_()[] '
    filename = name + '.jpg'

    return ''.join(c for c in filename if c in valid_chars)


def get_steam_xml(username):
    xml_url = 'http://steamcommunity.com/id/{0}/games?tab=all&xml=1'.format(username)
    return urllib.urlopen(xml_url)


@retries(4, exceptions=(IOError,), hook=retry_exc_handler)
def save_image(img_url, path_to_save, filename):
    urllib.urlretrieve(img_url, path_to_save + '/' + filename)


def get_images(username, status_output_enabled, path_to_save):
    tree = ET.parse(get_steam_xml(username))
    root = tree.getroot()

    if root.find('error') is not None:
        print root.find('error').text
        sys.exit(0)

    for game in root.iter('game'):
        name = game.find('name').text
        app_id = game.find('appID').text

        img_url = 'http://cdn.akamai.steamstatic.com/steam/apps/{0}/header.jpg'.format(app_id)

        if urllib.urlopen(img_url).getcode() == 200:
            filename = get_valid_filename(name)

            if status_output_enabled == 'Y':
                print 'Downloading \'' + filename + '\' image...'

            save_image(img_url, path_to_save, filename)

    print 'Download complete'


def main():
    print ('   _____ __                          _______ __         \n'
           '  / ___// /____  ____ _____ ___     /_  __(_) /__  _____\n'
           '  \__ \/ __/ _ \/ __ `/ __ `__ \     / / / / / _ \/ ___/\n'
           ' ___/ / /_/  __/ /_/ / / / / / /    / / / / /  __(__  ) \n'
           '/____/\__/\___/\__,_/_/ /_/ /_/    /_/ /_/_/\___/____/ \n')

    username = raw_input('Steam username: ')

    status_output_enabled = ''
    while status_output_enabled != 'Y' and status_output_enabled != 'N':
        status_output_enabled = raw_input('Status output (y/n): ').upper()
        if status_output_enabled != 'Y' and status_output_enabled != 'N':
            print 'Invalid input'

    path_to_save = raw_input('Path to save (leave blank for current directory): ')
    if path_to_save == '':
        path_to_save = '.'
    else:
        path_to_save = path_to_save.replace('\\', '/')
        if path_to_save[-1:] == '/':
            path_to_save = path_to_save[:-1]
    if not os.path.isdir(path_to_save):
        print 'Directory does not exist'
        sys.exit(0)

    get_images(username, status_output_enabled, path_to_save)


if __name__ == '__main__':
    main()
