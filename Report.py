from bs4 import BeautifulSoup
from ustclogin import Login
import time
from newtime import create

start_date = time.strftime("%Y-%m-%d 00:00:00",time.localtime(time.time()+8*3600))
end_date = time.strftime("%Y-%m-%d 23:59:59",time.localtime(time.time()+8*3600))
nowday = time.mktime(time.strptime(end_date, "%Y-%m-%d %H:%M:%S"))
monday = time.mktime(time.strptime("2017-01-01 23:59:59", "%Y-%m-%d %H:%M:%S"))
today = int(nowday - monday) // (24 * 3600) % 7

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
            if "关闭进出校报备" in data:
                raise ValueError("change method")
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

    def apply_cross_campus(self, cross_campus_data):
        if self.login.login():
            data = self.login.session.get(
                "https://weixine.ustc.edu.cn/2020").text
            soup = BeautifulSoup(data, "html.parser")
            headers = {
                "user-agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39"
            }
            data = self.login.session.get(
                "https://weixine.ustc.edu.cn/2020/stayinout_apply?t=3",
                headers=headers).text
            soup = BeautifulSoup(data, "html.parser")
            xck = soup.find("input", {"name": "files_xck"})["value"]
            akm = soup.find("input", {"name": "files_akm"})["value"]
            hs = soup.find("input", {"name": "files_hs"})["value"]
            hs2 = soup.find("input", {"name": "files_hs2"})["value"]
            token = soup.find("input", {"name": "_token"})["value"]
            choose_ds = data.split('<option value="')[1].split('"')[0]
            sd = time.strftime("%Y-%m-%d 06:00:00",time.localtime(time.time()+32*3600))
            ed = time.strftime("%Y-%m-%d 23:59:59",time.localtime(time.time()+32*3600))
            post_data = cross_campus_data + [
                ("_token", token),
                ("start_date", sd),
                ("end_date", ed),
                ("choose_ds", choose_ds),
                ("t", "3"),
                ("files_xck", xck),
                ("files_akm", akm),
                ("files_hs", hs),
                ("files_hs2", hs2),
                ("start_day", "2"), 
            ]
            post = self.login.session.post(
                "https://weixine.ustc.edu.cn/2020/stayinout_apply",
                data=post_data)
            if post.url[-3:] == 't=t':
                print("cross campus successful!")
                return True
            else:
                print("cross campus failed")
                f = open("./log.html", 'w')
                f.write(data)
                f.close()
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
            morehs = ("未检测到昨日核酸检测结果，请自行上传" in data)
            soup = BeautifulSoup(data, "html.parser")
            token = soup.find("input", {"name": "_token"})["value"]
            post_data = out_school_data + [
                ("_token", token),
                ("start_date", start_date),
                ("end_date", end_date),
                ("t", "2"),
            ]
            if morehs:
                gid = data.split("gid")[-1].split("'")[2]
                sign = data.split("sign")[-1].split("'")[2]
                p = self.login.session.post(
                    "https://weixine.ustc.edu.cn/2020img/api/upload", 
                    data=[
                        ("_token", token),
                        ("gid", gid),
                        ("sign", sign),
                        ("id", "WU_FILE_0"),
                        ("name", "xcm.jpg"),
                    ],
                    files={
                        "file": (
                            "xcm.jpg",
                            open("xcm.jpg", "rb"),
                            "image/jpeg",
                            {},
                        )
                    }
                )
                print('upload hesuannnn')
                post_data.append(("files_hs3", "".join(p.text.split('"id":"')[-1].split('"')[0].split('\\'))))
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

    def upload_code(self, number):
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
            create(number)

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

if __name__ == '__main__':
    print(end_date)
    print(today)