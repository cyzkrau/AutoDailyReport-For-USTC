from bs4 import BeautifulSoup
from ustclogin import Login
import time

start_date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()+8*3600))
end_date = time.strftime("%Y-%m-%d 23:59:59",time.localtime(time.time()+32*3600))

class Report(object):

    def __init__(self, stuid, password):
        self.stuid = stuid
        self.password = password
        self.login = Login(self.stuid, self.password,
                           "https://weixine.ustc.edu.cn/2020/caslogin")

    def getstate(self):
        if self.login.login():
            data = self.login.result.text
            soup = BeautifulSoup(data, "html.parser")
            return soup.find("p", {"style":"margin: 5px -10px 0;"}).contents[1].contents[0]
        print("login failed")
        return False

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
            post_data = cross_campus_data + [
                ("_token", token),
                ("start_date", start_date),
                ("end_date", end_date),
                ("t", "3"),
            ]
            post = self.login.session.post(
                "https://weixine.ustc.edu.cn/2020/apply/daliy/ipost",
                data=post_data)
            if "?t=d" in post.url:
                print("cross campus successful!")
                return True
            else:
                print("cross campus failed")
                print(data)
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
            post_data = out_school_data + [
                ("_token", token),
                ("start_date", start_date),
                ("end_date", end_date),
                ("t", "2"),
            ]
            post = self.login.session.post(
                "https://weixine.ustc.edu.cn/2020/apply/daliy/ipost",
                data=post_data)
            if "?t=d" in post.url:
                print("out school successful!")
                return True
            else:
                print("out school failed")
                print(data)
                return False
        print("login failed")
        return False

    def upload_code(self):
        if self.login.login():
            data = self.login.session.get(
                "https://weixine.ustc.edu.cn/2020/upload/xcm").text
            if '关闭相关功能' in data:
                print("bad upload code time")
                return False
            data = data.encode("ascii", "ignore").decode("utf-8", "ignore")
            token = data.split("_token")[-1].split("'")[1]
            sign = data.split("sign")[-1].split("'")[2]
            gid = data.split("gid")[-1].split("'")[2]
            import newtime

            def run_update(fnm, t):
                data = [
                    ("_token", token),
                    ("gid", gid),
                    ("t", t),
                    ("id", "WU_FILE_0"),
                    ("sign", sign),
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
                    "https://weixine.ustc.edu.cn/2020img/api/upload_for_student",
                    data=data,
                    files=files,
                )
                if "true" not in post.text:
                    print("update failed")
                    return False
                return True

            # if run_update("xcm.jpg", 1) & run_update("akm.jpg", 2):
            if run_update("xcm.jpg", 1):
                print("update successful")
                return True
        print("login failed")
        return False
