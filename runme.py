import argparse
import random
from Report import *

report_data = [
    ("juzhudi", "中校区"),  # 居住地
    ("dorm_building", "z2"),  # 宿舍楼
    ("dorm", "414"),  # 宿舍号
    ("body_condition", "1"),  # 身体状况 1为正常
    ("body_condition_detail", ""),  # 身体状况详细 正常无需
    ("now_status", "1"),  # 当前状态 1为正常在校园内
    ("now_status_detail", ""),  # 当前状态详细 正常无需
    ("has_fever", "0"),  # 目前有无发热等疑似症状 0为无
    ("last_touch_sars", "0"),  # 是否接触过确诊或疑似病例的患者 0为无
    ("last_touch_sars_date", ""),  # 最近一次接触日期
    ("last_touch_sars_detail", ""),  # 具体情况
    ("is_danger", "0"),  # 当前居住地是否为疫情中高风险地区 0为否
    ("is_goto_danger", "0"),  # 14天内是否有疫情中高风险地区旅居史 0为否
    ("jinji_lxr", "cyzkrau"),  # 紧急联系人
    ("jinji_guanxi", "self"),  # 与本人关系
    ("jiji_mobile", "18701375065"),  # 紧急联系人电话
    ("other_detail", ""),  # 其他情况说明
]
cross_campus_data = [
    ("return_college[]", "东校区"),  # 往返校区
    ("return_college[]", "西校区"),  # 往返校区
    ("return_college[]", "中校区"),  # 往返校区
    ("reason", "上课"),  # 原因
]
out_school_data = [
    ("return_college[]", "蜀山区"),  # 目的地
    ("return_college[]", "包河区"),  # 目的地
    ("return_college[]", "瑶海区"),  # 目的地
    ("return_college[]", "庐阳区"),  # 目的地
    ("reason", "玩"),  # 原因
]
number = "187****5065"
course = ["泛函分析", "组合", "拓扑"]
croos_campus_dates = [] # 申请跨校区的日期

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="URC nCov auto report script.")
    parser.add_argument("stuid", help="your student number", type=str)
    parser.add_argument("password", help="your CAS password", type=str)
    args = parser.parse_args()
    autorepoter = Report(stuid=args.stuid, password=args.password)
    count = 5
    while count != 0:
        state = autorepoter.getstate()
        if '在校' != state[:2]:
            print("NOW STATE " + state)
            exit(0)
        work = autorepoter.report(report_data) & autorepoter.upload_code(number)

        try:
            # work = work & autorepoter.cross_campus(cross_campus_data)
            work = autorepoter.out_school(out_school_data)
        except Exception:
            if today % 7 + 1 in croos_campus_dates:
                cross_campus_data[-1] = ("reason", "上" + random.sample(course, 1)[0] + "课")
                print(cross_campus_data)
                work = autorepoter.apply_cross_campus(cross_campus_data)
            
        if work:
            print("ENJOY YOUR FREEDOM! ")
            break
        print("Retry...")
        count = count - 1
    if count != 0:
        exit(0)
    else:
        exit(-1)
