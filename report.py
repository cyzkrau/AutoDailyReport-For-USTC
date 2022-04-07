import time
import re
import argparse
from bs4 import BeautifulSoup
import json
import pytz
from ustclogin import Login
from datetime import datetime
from datetime import timedelta
from datetime import timezone

report_data = [
    ("juzhudi", "中校区"),
    ("dorm_building", "z2"),
    ("dorm", "414"),
    ("body_condition", "1"),
    ("body_condition_detail", ""),
    ("now_status", "1"),
    ("now_status_detail", ""),
    ("has_fever", "0"),
    ("last_touch_sars", "0"),
    ("last_touch_sars_date", ""),
    ("last_touch_sars_detail", ""),
    ("is_danger", "0"),
    ("is_goto_danger", "0"),
    ("jinji_lxr", "cyzkrau"),
    ("jinji_guanxi", "self"),
    ("jiji_mobile", "18701375065"),
    ("other_detail", ""),
]
outschool_data = [
    ("return_college[]", "东校区"),
    ("return_college[]", "西校区"),
    ("return_college[]", "南校区"),
    ("return_college[]", "北校区"),
    ("return_college[]", "中校区"),
    ("reason", "*"),
    ("t", "3"),
]
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

    def report(self):
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

    def outschool(self):
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
            data = outschool_data + [
                ("_token", token),
                ("start_date", start_date),
                ("end_date", end_date),
            ]
            post = self.login.session.post(
                "https://weixine.ustc.edu.cn/2020/apply/daliy/post", data=data
            )
            if "?t=d" in post.url:
                print("out school successful!")
                return True
            else:
                print("out school failed")
                return False
        print("login failed")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="URC nCov auto report script.")
    parser.add_argument("stuid", help="your student number", type=str)
    parser.add_argument("password", help="your CAS password", type=str)
    args = parser.parse_args()
    autorepoter = Report(stuid=args.stuid, password=args.password)
    count = 5
    while count != 0:
        ret = autorepoter.report() & autorepoter.outschool()
        if ret:
            print("ENJOY YOUR FREEDOM! ")
            break
        print("Retry...")
        count = count - 1
    if count != 0:
        exit(0)
    else:
        exit(-1)
