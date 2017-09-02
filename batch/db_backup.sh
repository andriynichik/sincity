#!/usr/bin/env bash

dt=$(date '+%Y%m%d%H%M%S');

mongodump --host mongodb.example.net --port 27017 --out /data/backup/$dt