#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 申請書情報の取得

import requests
import json
import os


class Jobcan:
    """
    Jobcan API wrapper
    """

    def __init__(self):
        work_dir = os.path.dirname(__file__)
        config_path = f"{work_dir}/config.json"

        with open(config_path) as f:
            config = json.load(f)
            api_token = config["api_token"]
            self.headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json",
            }
            self.base_url = config["base_url"]

    def get(self, url):
        response = requests.get(url, headers=self.headers)
        return response

    def abort(self, url, response):
        print(url)
        print(response.json())
        exit(1)

    def request(self, request_id):
        """
        request_id で指定した申請の情報を取得する。
        """

        url = f"{self.base_url}/v1/requests/{request_id}/"
        response = self.get(url)
        data = response.json()

        if response.status_code == 200:
            return data
        elif response.status_code == 404:
            self.abort(url, response)
        elif response.status_code == 500:
            self.abort(url, response)
        else:
            print("仕様外の応答")
            exit(1)

    def requests(self, form_id, status):
        """
        form_id, status で指定した条件にマッチする申請のリストを取得する。
        """

        args = f"?status={status}&form_id={form_id}"
        url = f"{self.base_url}/v2/requests/" + args
        result = []

        req_list = self.__get_requests_seq(url)

        for i in req_list:
            r = self.request(i["id"])
            result.append(r)

        return result

    def __get_requests_seq(self, url):
        """
        requests の下請けメソッド。requestsの回答が複数ページに分かれる際の取りまとめを行う。
        """
        results = []

        while True:
            response = self.get(url)
            print(response)

            if response.status_code == 200:
                body = response.json()
                results += body["results"]
                if body["next"] == None:
                    break
                else:
                    url = body["next"]
            elif response.status_code == 400:
                self.abort(url, response)
            elif response.status_code == 404:
                self.abort(url, response)
            elif response.status_code == 500:
                self.abort(url, response)
            else:
                print("仕様外の応答: {response.status_code}")
                exit(1)

        return results

    def test(self):
        """
        接続テスト。APIトークンの設定値が正しいかどうかのテスト等
        """
        response = self.get(f"{self.base_url}/test/")
        return int(response.status_code)

    def forms(self):
        url = f"{self.base_url}/v1/forms/"
        results = []

        while True:
            response = self.get(url)

            if response.status_code == 200:
                body = response.json()
                results += body["results"]
                if body["next"] == None:
                    break
                else:
                    url = body["next"]
            elif response.status_code == 400:
                print(response.json())
                exit(1)
            elif response.status_code == 500:
                print(response.json())
                exit(1)
            else:
                print(f"仕様外の応答: {response.status_code}")
                exit(1)

        return results


def parse_customized_items(customized_items, title, target):
    """
    customized_items から、title を持つ content を取り出す。

    Args:
        customized_items: APIで取り出した request の JSON
        title: 検索キーとなる文字列
        target: 取り出す項目の種類
    """
    for i in customized_items:
        if i["title"] == title:
            return i[target]
    return None


def filter_waiting_at(req_list, name):
    result = []

    for req in req_list:
        steps = req["detail"]["approval_process"]["steps"]
        step_found = None
        for step in steps:
            if step["status"] == "承認待ち":
                step_found = step
                break
        if step_found == None:
            continue

        for approver in step_found["approvers"]:
            if approver["approver_name"] == name:
                result.append(req)
                continue
    return result
