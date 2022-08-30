# USTC健康打卡平台自动打卡脚本

![Auto-report action](https://github.com/cyzkrau/AutoDailyReport-For-USTC/workflows/Auto-report%20action/badge.svg?branch=master)
![Language](https://img.shields.io/badge/language-Python3-yellow.svg)
![GitHub stars](https://img.shields.io/github/stars/cyzkrau/AutoDailyReport-For-USTC)
![GitHub forks](https://img.shields.io/github/forks/cyzkrau/AutoDailyReport-For-USTC)

## 说明

**本打卡脚本仅供学习交流使用，请勿过分依赖。开发者对使用或不使用本脚本造成的问题不负任何责任，不对脚本执行效果做出任何担保，原则上不提供任何形式的技术支持。**

本仓库基于[原版](https://github.com/xbb1973/USTC-ncov-AutoReport)，参考[修改版](https://github.com/Kobe972/USTC-ncov-AutoReport)并进行修改，增加对出校申请和跨校区报备的支持。目前正持续更新以尽量使得每一天都可以自动打卡，愿完全放开的日子早日到来。

## 更新记录

- 20220407: 本人基于之前的脚本，并进行修改以适应现在的打卡版本
- 20220408: 在SECRET中增加是否执行操作的选项，以适应更多需求
- 20220421: 增加每日上传两码功能
- 20220506: **恭喜解封**，源代码可用，但增加每日出校报备
- 20220509: 解决打卡系统post链接被修改，上传两码需要GID的问题
- 20220510: 解决上传两码需要sign的问题
- 20220513: **恭喜自动授权安康码**，不再需要自动上传安康码
- 20220706: 增加对于不在校等状态的支持，可能有bug
- 20220829: 风头较严，进出校需要人工审核，建议只进行报备和上传行程码
- 20220830: 增加每日对于申请审核跨校区的支持

## 使用方法

0. **写在前面：请在自己fork的仓库中修改，并push到自己的仓库，不要直接修改本仓库，也不要将您的修改pull request到本仓库（对本仓库的改进除外）！如果尚不了解github的基本使用方法，请参阅[使用议题和拉取请求进行协作/使用复刻](https://docs.github.com/cn/github/collaborating-with-issues-and-pull-requests/working-with-forks)和[使用议题和拉取请求进行协作/通过拉取请求提议工作更改](https://docs.github.com/cn/github/collaborating-with-issues-and-pull-requests/proposing-changes-to-your-work-with-pull-requests)。**

1. 将本代码仓库fork到自己的github，并授权打卡系统从权威机构获取安康码信息。

2. 根据自己的实际情况修改`runme.py`中的数据，修改`xcm.jpg`为自己的行程码，更改`newtime.py`中<code>bbox</code>数据使得更新的时间数据可以以假乱真。

3. 将修改好的代码提交到自己的仓库。

4. 点击Actions选项卡，点击`I understand my workflows, go ahead and enable them`.

5. 点击Settings选项卡，点击左侧Secrets，点击New secret，创建名为`STUID`，值为自己学号的secret。用同样方法，创建名为`PASSWORD`，值为自己统一身份认证密码的secret。以上数据不会被公开。

   ![secrets](imgs/image-20200826215037042.png)

6. 默认的打卡时间是每天的上午7:10(建议5点之后，因为5点才会同步安康码)，可能会有（延后）几十分钟的浮动。如需选择其它时间，可以修改`.github/workflows/report.yml`中的`cron`，详细说明参见[安排的事件](https://docs.github.com/cn/actions/reference/events-that-trigger-workflows#scheduled-events)，请注意这里使用的是**国际标准时间UTC**，北京时间的数值比它大8个小时。建议修改默认时间，避开打卡高峰期以提高成功率。

7. 在Actions选项卡可以确认打卡情况。如果打卡失败（可能是临时网络问题等原因），脚本会自动重试，五次尝试后如果依然失败，将返回非零值提示构建失败。

8. 在Github个人设置页面的Notifications下可以设置Github Actions的通知，建议打开Email通知，并勾选"Send notifications for failed workflows only"。请及时查看邮件，如果失败会进行通知。

9. 如果觉得这个仓库对你有用的话，给个星星✨吧～

## 在本地运行测试

要在本地运行测试，需要安装python 3。我们假设您已经安装了python 3和pip 3，并已将其路径添加到环境变量。

### 安装依赖

```shell
pip install -r requirements.txt
```

### 运行打卡程序

```shell
python runme.py [STUID] [PASSWORD]
```
其中，`[STUID]`是学号，`[PASSWORD]`是统一身份认证的密码明文，剩下三个参数为是否出校报备、是否跨校区报备、是否每日打卡，默认不出校，跨校区，打卡。如
```shell
python runme.py "PB19890604" "FREEDOM"
```
