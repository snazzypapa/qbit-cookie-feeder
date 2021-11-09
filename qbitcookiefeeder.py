#!/usr/bin/python3
import os
import time
import logging
import toml
import subprocess
import qbittorrentapi

config = toml.load(os.path.join(os.path.dirname(__file__), 'config.toml'))

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), 'qbitcookiefeeder.log'), format="%(asctime)s - %(levelname)-10s - %(name)-10s - %(funcName)-20s - %(message)s", level=logging.INFO)


def add_cookies(tracker_dict):
    client = qbittorrentapi.Client(host=config['host'], username=config['username'], password=config['password'])
    for tracker in tracker_dict.values():
        if client.torrents_add(urls=tracker['downloadLink'], cookie=tracker['cookie'], is_paused=True) == 'Ok.':
            logging.info(f"Successfully added link to client for tracker: {tracker['name']}")
        else:
            logging.info("Failed to add link to client for tracker: {tracker['name']}")


def watch_logs(filename):
    logging.info('Starting log watcher')
    f = subprocess.Popen(['tail', '-F', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time_added = 0
    while True:
        line = f.stdout.readline()
        if b'Web UI: Now listening on IP' in line and time.time() - time_added > 10:
            logging.info('Detected qbittorrent start - adding cookies')
            add_cookies(config['trackers'])
            time_added = time.time()

watch_logs(config['qbitLogFile'])
