#!/usr/bin/python3
# -*- coding:utf-8 -*-

import argparse
import json
import os

import jsondb
import writer


def print_row(row):
    print("=" * 30 + " " + str(row[0]) + " " + "=" * 30)
    jsondata = json.loads(row[1])
    writer.console(jsondata)


def command_dump(args):
    for row in args.db.fetch("select * from requests;"):
        print_row(row)


def command_find(args):
    query = f"select * from requests where id={args.jobcan_id};"
    for row in args.db.fetch(query):
        print_row(row)


def main():
    parser = argparse.ArgumentParser(description="note management")
    subparsers = parser.add_subparsers()

    parser_dump = subparsers.add_parser("dump", help="dump the cache file.")
    parser_dump.set_defaults(handler=command_dump)

    parser_find = subparsers.add_parser("find", help="find a request by Jobcan ID.")
    parser_find.add_argument("jobcan_id", type=int, help="Jobcan ID")
    parser_find.set_defaults(handler=command_find)

    work_dir = os.path.dirname(__file__)
    config_path = f"{work_dir}/config.json"

    with open(config_path) as f:
        config = json.load(f)

        cache_file = config["cache_file"]

        with jsondb.DB(cache_file) as db:
            parser_dump.add_argument("--db", default=db)
            parser_find.add_argument("--db", default=db)

            args = parser.parse_args()
            if hasattr(args, "handler"):
                args.handler(args)
            else:
                parser.print_help()


if __name__ == "__main__":
    main()
