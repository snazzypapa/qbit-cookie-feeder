# qbit-cookie-feeder
Add private tracker cookies to qbittorrent in docker to enable auto downloading via RSS feeds.

Supports qBittorrent v4.1.0+ (i.e. Web API v2.0+). Currently supports up to qBittorrent [v4.3.8](https://github.com/qbittorrent/qBittorrent/releases/tag/release-4.3.8) (Web API v2.8.2) released on Aug 28, 2021.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-blue.svg?style=flat-square)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%203-blue.svg?style=flat-square)](https://github.com/snazzypapa/qbitmgr/blob/master/LICENSE.md)

---



# Introduction

qBittorrent in docker does not save private tracker cookies to disk so RSS automatic downloads fail after reboots and program restarts.

This simple script detects program starts via the qbittorrent logs and immediately adds torrent download links that contain the cookies to the client.

qBittorrent will save the cookies in memory even if the provided link does not download a torrent file. I recommend using a generic torrent download link without a torrent ID so you do not have to download a new file at every reboot. For example, use "https://linux-iso-tracker.com/download.php?" instad of "https://linux-iso-tracker.com/download.php?id=123456."  


# Requirements

1. Unix-based operating system (Ubuntu/Debian, MacOs, BSD). Only tested on Ubuntu.

2. Qbittorrent with WebUI accessible on localhost


# Installation

1. Clone the repo.

   ```
   sudo git clone https://github.com/snazzypapa/qbit-cookie-feeder /opt/qbitcookiefeeder
   ```

1. Fix permissions of the folder and make executable (replace `user`/`group` with your info; run `id` to check).

   ```
   sudo chown -R user:group /opt/qbitcookiefeeder
   chmod +x /opt/qbitcookiefeeder/qbitcookiefeeder.py
   ```

1. Go into the qbit-cookie-feeder folder.

   ```
   cd /opt/qbitcookiefeeder
   ```

1. Install Python PIP.

   ```
   sudo apt-get install python3-pip
   ```

1. Install the required python modules.

   ```
   sudo python3 -m pip install -r requirements.txt
   ```

1. Rename the example config file and edit it. You may include as many trackers as you wish.

   ```
   mv config.toml.example config.toml && nano config.toml
   ```

1. Run script using crontab.

   ```
   crontab -e
   @reboot /usr/bin/python3 /opt/qbitcookiefeeder/qbitcookiefeeder.py
   ```
