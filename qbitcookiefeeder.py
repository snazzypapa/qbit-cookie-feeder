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
            logging.info(f"Failed to add link to client for tracker: {tracker['name']}")


def output_new_lines(filename, out_q):
    """ Outputs new lines of text file to queue
        Args:
             filename: path to text file to watch
             out_q: queue from threading to post new lines
    """
    logging.info("Starting log watcher")
    f = subprocess.Popen(
        ["tail", "-F", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    while True:
        line = f.stdout.readline()
        out_q.put(line)


def parse_new_lines(match_string, in_q):
    """ Reads lines from queue and run add_cookies() if text is found
        Args:
            match_string: string to match in lines
            in_q: queue from threading to watch
    """
    logging.info("Starting log parser")
    time_added = 0
    while True:
        line = in_q.get()
        if match_string.encode('UTF-8') in line and time.time() - time_added > 10:
            logging.info("Detected qbittorrent start - adding cookies")
            add_cookies()
            time_added = time.time()


def main():
    q = Queue()
    t1 = Thread(target=output_new_lines, args=(config["qbitLogFile"], q))
    t2 = Thread(target=parse_new_lines, args=("Web UI: Now listening on IP", q))
    t1.start()
    t2.start()


if __name__ == "__main__":
    main()

