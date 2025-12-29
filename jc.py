#!/usr/bin/python3
# -*- coding:utf-8 -*-

import argparse
import json
import jobcan


def command_forms(args):
    jc = jobcan.Jobcan()
    res = jc.forms()

    if args.long:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        for j in res:
            print("{}: {}".format(j["id"], j["name"]))


def command_request(args):
    jc = jobcan.Jobcan()
    res = jc.request(args.jobcan_id)
    print(json.dumps(res, indent=2, ensure_ascii=False))


def command_test(jc):
    jc = jobcan.Jobcan()
    res = jc.test()
    if res == 200:
        print("正常(200)")
    elif res == 401:
        print("問題あり(401)")
    else:
        print(f"仕様外の応答({res})")


def main():
    parser = argparse.ArgumentParser(description="CLI for Jobcan")
    subparsers = parser.add_subparsers()

    parser_forms = subparsers.add_parser("forms", help="see `forms -h`")
    parser_forms.add_argument(
        "-l", "--long", action="store_true", help="show all JSONs"
    )
    parser_forms.set_defaults(handler=command_forms)

    parser_request = subparsers.add_parser("request", help="see `request -h`")
    parser_request.add_argument(
        "jobcan_id", type=int, help="get a request with jobcan_id"
    )
    parser_request.set_defaults(handler=command_request)

    parser_test = subparsers.add_parser("test", help="see `test -h`")
    parser_test.set_defaults(handler=command_test)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
