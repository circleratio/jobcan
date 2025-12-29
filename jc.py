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


def command_requests(args):
    req_arg = {}

    if args.form_id:
        req_arg["form_id"] = args.form_id
    if args.status:
        req_arg["status"] = args.status.replace("'", "")
    if args.completed_before:
        req_arg["completed_before"] = args.completed_before.replace("'", "")
    if args.completed_after:
        req_arg["completed_after"] = args.completed_after.replace("'", "")

    jc = jobcan.Jobcan()
    if args.details:
        if args.form_id is None:
            print('Query for detailed information is allowed only for a single form. Aborted.')
            exit(1)
            
        res = jc.requests_details(**req_arg)
    else:
        res = jc.requests(**req_arg)
    print(json.dumps(res, indent=2, ensure_ascii=False))


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

    parser_requests = subparsers.add_parser("requests", help="see `requests -h`")
    parser_requests.add_argument("-i", "--form_id", type=int, help="form ID")
    parser_requests.add_argument("-s", "--status", type=ascii, help="status")
    parser_requests.add_argument(
        "-t",
        "--completed_before",
        type=ascii,
        help="finally approved before the specified date",
    )
    parser_requests.add_argument(
        "-f",
        "--completed_after",
        type=ascii,
        help="finally approved after the specified date",
    )
    parser_requests.add_argument(
        "-d", "--details", action="store_true", help="get details of requests"
    )
    parser_requests.set_defaults(handler=command_requests)

    parser_test = subparsers.add_parser("test", help="see `test -h`")
    parser_test.set_defaults(handler=command_test)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
