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
    def __init__(self, stuid, password):
        self.stuid = stuid
        self.password = password
        self.login = Login(
            self.stuid, self.password, "https://weixine.ustc.edu.cn/2020/caslogin"
        )

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
            data = self.login.session.get("https://weixine.ustc.edu.cn/2020").text
            soup = BeautifulSoup(data, "html.parser")
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39"
            }
            data = self.login.session.get(
                "https://weixine.ustc.edu.cn/2020/apply/daliy", headers=headers
            ).text
            data = data.encode("ascii", "ignore").decode("utf-8", "ignore")
            soup = BeautifulSoup(data, "html.parser")
            token = soup.find("input", {"name": "_token"})["value"]
            data = self.login.session.get(
                "https://weixine.ustc.edu.cn/2020/apply/daliy/i?t=3", headers=headers
            ).text
            data = data.encode("ascii", "ignore").decode("utf-8", "ignore")
            soup = BeautifulSoup(data, "html.parser")
            start_date = soup.find("input", {"id": "start_date"})["value"]
            end_date = soup.find("input", {"id": "end_date"})["value"]
            data = cross_campus_data + [
                ("_token", token),
                ("start_date", start_date),
                ("end_date", end_date),
                ("t", "3"),
            ]
            post = self.login.session.post(
                "https://weixine.ustc.edu.cn/2020/apply/daliy/post", data=data
            )
            if "?t=d" in post.url:
                print("cross school successful!")
                return True
            else:
                print("cross school failed")
                return False
        print("login failed")
        return False

    def out_school(self, out_school_data):
        if self.login.login():
            data = self.login.session.get("https://weixine.ustc.edu.cn/2020").text
            soup = BeautifulSoup(data, "html.parser")
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39"
            }
            data = self.login.session.get(
                "https://weixine.ustc.edu.cn/2020/apply/daliy", headers=headers
            ).text
            data = data.encode("ascii", "ignore").decode("utf-8", "ignore")
            soup = BeautifulSoup(data, "html.parser")
            token = soup.find("input", {"name": "_token"})["value"]
            data = self.login.session.get(
                "https://weixine.ustc.edu.cn/2020/stayinout_apply?t=2", headers=headers
            ).text
            data = data.encode("ascii", "ignore").decode("utf-8", "ignore")
            soup = BeautifulSoup(data, "html.parser")

            choose_ds = soup.find("select", {"id": "choose_ds"})
            choose_ds = str(choose_ds.contents[1]).split('"')[1]
            end_date = soup.find("input", {"id": "end_date"})["value"]
            start_date = soup.find("input", {"id": "start_date"})["value"]
            data = out_school_data + [
                ("choose_ds", choose_ds),
                ("_token", token),
                ("start_date", start_date),
                ("end_date", end_date),
                ("t", "2"),
            ]
            post = self.login.session.post(
                "https://weixine.ustc.edu.cn/2020/stayinout_apply", data=data
            )
            if "?t=t" in post.url:
                print("out school successful!")
                return True
            else:
                print("out school failed")
                return False
        print("login failed")
        return False
