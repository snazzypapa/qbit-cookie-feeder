import os
import time
import toml
import logging
import subprocess
from queue import Queue
from threading import Thread
import qbittorrentapi

config = toml.load(os.path.join(os.path.dirname(__file__), "config.toml"))

logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), "qbitcookiefeeder.log"),
    format="%(asctime)s - %(levelname)-10s - %(name)-10s - %(funcName)-20s - %(message)s",
    level=logging.INFO,
)


def add_cookies():
    """adds link with cookies to qbittorrent client from each tracker in config"""
    client = qbittorrentapi.Client(
        host=config["host"], username=config["username"], password=config["password"]
    )
    for tracker in config["trackers"].values():
        if (
            client.torrents_add(
                urls=tracker["downloadLink"], cookie=tracker["cookie"], is_paused=True
            )
            == "Ok."
        ):
            logging.info(
                f"Successfully added link to client for tracker: {tracker['name']}"
            )
        else:
            logging.info("Failed to add link to client for tracker: {tracker['name']}")


def read_logs(filename, out_q):
    logging.info("Starting log watcher")
    f = subprocess.Popen(
        ["tail", "-F", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    while True:
        line = f.stdout.readline()
        out_q.put(line)


def log_parser(in_q):
    logging.info("Starting log parser")
    time_added = 0
    while True:
        line = in_q.get()
        if b"Web UI: Now listening on IP" in line and time.time() - time_added > 10:
            logging.info("Detected qbittorrent start - adding cookies")
            add_cookies()
            time_added = time.time()


def main():
    q = Queue()
    t1 = Thread(target=read_logs, args=(config["qbitLogFile"], q))
    t2 = Thread(target=log_parser, args=(q,))
    t1.start()
    t2.start()


if __name__ == "__main__":
    main()

