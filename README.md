# USTC健康打卡平台自动打卡脚本

![Auto-report action](https://github.com/cyzkrau/AutoDailyReport-For-USTC/workflows/Auto-report%20action/badge.svg?branch=master)
![Language](https://img.shields.io/badge/language-Python3-yellow.svg)
![GitHub stars](https://img.shields.io/github/stars/cyzkrau/AutoDailyReport-For-USTC)
![GitHub forks](https://img.shields.io/github/forks/cyzkrau/AutoDailyReport-For-USTC)

## 说明

**本打卡脚本仅供学习交流使用，请勿过分依赖。开发者对使用或不使用本脚本造成的问题不负任何责任，不对脚本执行效果做出任何担保，原则上不提供任何形式的技术支持。**

本仓库基于[原版](https://github.com/xbb1973/USTC-ncov-AutoReport)，参考[修改版](https://github.com/Kobe972/USTC-ncov-AutoReport)并进行修改。目前正持续更新以尽量使得每一天都可以自动打卡，愿完全放开的日子早日到来。

## 更新记录

- 20220407：本人基于之前的脚本，并进行修改以适应现在的打卡版本

## 使用方法

0. **写在前面：请在自己fork的仓库中修改，并push到自己的仓库，不要直接修改本仓库，也不要将您的修改pull request到本仓库（对本仓库的改进除外）！如果尚不了解github的基本使用方法，请参阅[使用议题和拉取请求进行协作/使用复刻](https://docs.github.com/cn/github/collaborating-with-issues-and-pull-requests/working-with-forks)和[使用议题和拉取请求进行协作/通过拉取请求提议工作更改](https://docs.github.com/cn/github/collaborating-with-issues-and-pull-requests/proposing-changes-to-your-work-with-pull-requests)。**

1. 将本代码仓库fork到自己的github。

2. 根据自己的实际情况修改`report.py`中39行以前的数据，默认的数据为本人报备数据。

3. 将修改好的代码提交到自己的仓库。如果不需要修改 `report.py`，请在 `README.md` 里添加一个空格并push，否则不会触发之后的步骤。

4. 点击Actions选项卡，点击`I understand my workflows, go ahead and enable them`.

5. 点击Settings选项卡，点击左侧Secrets，点击New secret，创建名为`STUID`，值为自己学号的secret。用同样方法，创建名为`PASSWORD`，值为自己统一身份认证密码的secret。这两个值不会被公开。

   ![secrets](imgs/image-20200826215037042.png)

6. 默认的打卡时间是每天的上午0:50，可能会有（延后）几十分钟的浮动。如需选择其它时间，可以修改`.github/workflows/report.yml`中的`cron`，详细说明参见[安排的事件](https://docs.github.com/cn/actions/reference/events-that-trigger-workflows#scheduled-events)，请注意这里使用的是**国际标准时间UTC**，北京时间的数值比它大8个小时。建议修改默认时间，避开打卡高峰期以提高成功率。

7. 在Actions选项卡可以确认打卡情况。如果打卡失败（可能是临时网络问题等原因），脚本会自动重试，五次尝试后如果依然失败，将返回非零值提示构建失败。

8. 在Github个人设置页面的Notifications下可以设置Github Actions的通知，建议打开Email通知，并勾选"Send notifications for failed workflows only"。请及时查看邮件，如果失败会进行通知。

## 在本地运行测试

要在本地运行测试，需要安装python 3。我们假设您已经安装了python 3和pip 3，并已将其路径添加到环境变量。

### 安装依赖

```shell
pip install -r requirements.txt
```

### 运行打卡程序

```shell
python report.py [STUID] [PASSWORD]
```
其中，`[STUID]`是学号，`[PASSWORD]`是统一身份认证的密码明文，如
```shell
python report.py "PB19890604" "FREEDOM"
```

## 打卡数据获取方法

使用 F12 开发者工具抓包之后得到数据，仿照给定格式写入 `report.py` 中。

1. 登录进入 `https://weixine.歪比巴卜.edu.cn/2020/`，打开开发者工具（Chrome 可以使用 F12 快捷键），选中 Network 窗口：

![](./imgs/1.png)

2. 点击确认上报，点击抓到的 `daliy_report` 请求，在 `Headers` 下面找到 `Form Data` 这就是每次上报提交的信息参数。

![](./imgs/2.png)

3. 将找到的 Data 除 `_token` （每次都会改变，所以不需要复制，脚本中会每次获取新的 token 并添加到要提交的数据中）外都复制下来，存放在 `report.py` 的对应位置中。

4. 通过push操作触发构建任务，检查上报数据是否正确。
