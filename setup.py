#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import json
import jsondb

work_dir = os.path.dirname(__file__)
config_file = f"{work_dir}/config.json"


def setup_config():
    if os.path.isfile(config_file):
        print("Config file already exists. Skipped.")
    else:
        print("Not implemented yet.")


def setup_cache():
    with open(config_file) as f:
        config = json.load(f)
        cache_file = config["cache_file"]

    if os.path.isfile(cache_file):
        print("Cache file already exists. Skipped.")
    else:
        with jsondb.JsonDB(cache_file) as db:
            print("Creating a table for Jobkan requests.")
            db.create_table("requests")
            db.commit()


def main():
    setup_config()
    setup_cache()


if __name__ == "__main__":
    main()
