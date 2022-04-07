from bs4 import BeautifulSoup
import requests
from io import BytesIO
import pytesseract
from PIL import Image
import numpy as np
import cv2
from urllib.parse import unquote


class Login:
    def __init__(self, stuid, password, service):
        self.stuid = stuid
        self.password = password
        self.service = service
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
        }
        self.logined = False

    def get_LT(self):
        text = self.session.get(
            "https://passport.ustc.edu.cn/validatecode.jsp?type=login",
            stream=True,
            headers=self.headers,
        ).content
        image = Image.open(BytesIO(text))
        image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        kernel = np.ones((3, 3), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.erode(image, kernel, iterations=1)
        return pytesseract.image_to_string(Image.fromarray(image))[:4]

    def passport(self):
        data = self.session.get(
            "https://passport.ustc.edu.cn/login?service=" + self.service,
            headers=self.headers,
        )
        # self.headers = data.headers
        data = data.text
        data = data.encode("ascii", "ignore").decode("utf-8", "ignore")
        soup = BeautifulSoup(data, "html.parser")
        CAS_LT = soup.find("input", {"name": "CAS_LT"})["value"]
        LT = self.get_LT()
        data = {
            "model": "uplogin.jsp",
            "CAS_LT": CAS_LT,
            "service": unquote(self.service),
            "warn": "",
            "showCode": "1",
            "username": self.stuid,
            "password": str(self.password),
            "LT": LT,
            "button": "",
        }
        self.result = self.session.post(
            "https://passport.ustc.edu.cn/login", data=data, headers=self.headers
        )

    def login(self):
        if self.logined:
            return True
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        retrycount = 5
        while (not self.logined) and retrycount:
            self.passport()
            self.cookies = self.session.cookies
            retrycount = retrycount - 1
            if self.result.url == "https://passport.ustc.edu.cn/login":
                print("Login Failed! Retry...")
            else:
                print("Login Successful!")
                self.logined = True
                self.logined = True
        return self.logined
