#!/usr/bin/python3
import os
import time
import logging
import toml
import subprocess
import qbittorrentapi

config = toml.load(os.path.join(os.path.dirname(__file__), 'config.toml'))

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), 'qbit_cookie_feeder.log'), format="%(asctime)s - %(levelname)-10s - %(name)-10s - %(funcName)-20s - %(message)s", level=logging.INFO)


def add_torrent_link(_url, _cookie):
    client = qbittorrentapi.Client(host=config['host'], username=config['username'], password=config['password'])
    if client.torrents_add(urls=_url, cookie=_cookie, is_paused=True) == 'Ok.':
        return logging.info('Successfully added link to client')
    else:
        logging.info('Failed to add link to client')

def detect_text_within_line(target_text, line):
    if target_text in line:
        return True

def watch_logs(filename):
    logging.info('Starting log watcher')
    f = subprocess.Popen(['tail', '-F', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time_added = 0
    while True:
        line = f.stdout.readline()
        if detect_text_within_line(b'Web UI: Now listening on IP', line) and (time.time() - time_added) > 10:
            logging.info('Detected qbittorrent start - adding torrent link')
            add_torrent_link(config['torrentLink'], config['cookie'])
            time_added = time.time()

watch_logs(config['qbitLogFile'])
