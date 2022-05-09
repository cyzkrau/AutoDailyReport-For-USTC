import time
import re
from bs4 import BeautifulSoup
import json
import pytz
from ustclogin import Login
from datetime import datetime
from datetime import timedelta
from datetime import timezone

SHA_TZ = timezone(  # 北京时间
    timedelta(hours=8),
    name="Asia/Shanghai",
)


class Report(object):

    def __init__(self, stuid, password, gid):
        self.stuid = stuid
        self.password = password
        self.gid = gid
        self.login = Login(self.stuid, self.password,
                           "https://weixine.ustc.edu.cn/2020/caslogin")

    def report(self, report_data):
        if self.login.login():
            data = self.login.result.text
            data = data.encode("ascii", "ignore").decode("utf-8", "ignore")
            soup = BeautifulSoup(data, "html.parser")
            token = soup.find("input", {"name": "_token"})["value"]

            data = [("_token", token)] + report_data
            url = "https://weixine.ustc.edu.cn/2020/daliy_report"
            resp = self.login.session.post(url, data=data)
            if "上报成功" in resp.text:
                print("daily report successful!")
                return True
            else:
                print("daily report failed")
                return False
        print("login failed")
        return False

    def cross_campus(self, cross_campus_data):
        if self.login.login():
            data = self.login.session.get(
                "https://weixine.ustc.edu.cn/2020").text
            soup = BeautifulSoup(data, "html.parser")
            headers = {
                "user-agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39"
            }
            data = self.login.session.get(
                "https://weixine.ustc.edu.cn/2020/apply/daliy/i?t=3",
                headers=headers).text
            data = data.encode("ascii", "ignore").decode("utf-8", "ignore")
            soup = BeautifulSoup(data, "html.parser")
            token = soup.find("input", {"name": "_token"})["value"]
            start_date = soup.find("input", {"id": "start_date"})["value"]
            end_date = soup.find("input", {"id": "end_date"})["value"]
            data = cross_campus_data + [
                ("_token", token),
                ("start_date", start_date),
                ("end_date", end_date),
                ("t", "3"),
            ]
            post = self.login.session.post(
                "https://weixine.ustc.edu.cn/2020/apply/daliy/ipost",
                data=data)
            if "?t=d" in post.url:
                print("cross campus successful!")
                return True
            else:
                print("cross campus failed")
                return False
        print("login failed")
        return False

    def out_school(self, out_school_data):
        if self.login.login():
            data = self.login.session.get(
                "https://weixine.ustc.edu.cn/2020").text
            soup = BeautifulSoup(data, "html.parser")
            headers = {
                "user-agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39"
            }
            data = self.login.session.get(
                "https://weixine.ustc.edu.cn/2020/apply/daliy/i?t=2",
                headers=headers).text
            data = data.encode("ascii", "ignore").decode("utf-8", "ignore")
            soup = BeautifulSoup(data, "html.parser")
            token = soup.find("input", {"name": "_token"})["value"]
            start_date = soup.find("input", {"id": "start_date"})["value"]
            end_date = soup.find("input", {"id": "end_date"})["value"]
            data = out_school_data + [
                ("_token", token),
                ("start_date", start_date),
                ("end_date", end_date),
                ("t", "2"),
            ]
            post = self.login.session.post(
                "https://weixine.ustc.edu.cn/2020/apply/daliy/ipost",
                data=data)
            if "?t=d" in post.url:
                print("out school successful!")
                return True
            else:
                print("out school failed")
                return False
        print("login failed")
        return False

    def upload_code(self):
        if self.login.login():
            data = self.login.session.get(
                "https://weixine.ustc.edu.cn/2020/upload/xcm").text
            data = data.encode("ascii", "ignore").decode("utf-8", "ignore")
            soup = BeautifulSoup(data, "html.parser")
            token = soup.find("input", {"name": "_token"})["value"]
            import newtime

            def run_update(fnm, n):
                data = [
                    ("_token", token),
                    ("gid", self.gid),
                    ("id", "WU_FILE_0"),
                ]
                files = {
                    "file": (
                        fnm,
                        open(fnm, "rb"),
                        "image/jpeg",
                        {},
                    )
                }
                post = self.login.session.post(
                    "https://weixine.ustc.edu.cn/2020/upload/" + str(n) +
                    "/healthimg",
                    data=data,
                    files=files,
                )
                if "true" not in post.text:
                    print("update failed")
                    return False
                return True

            if run_update("xcm.jpg", 1) & run_update("akm.jpg", 2):
                print("update successful")
                return True
        print("login failed")
        return False
