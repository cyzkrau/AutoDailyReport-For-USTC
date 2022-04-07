import argparse
from Report import Report

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
    ("return_college[]", "南校区"),  # 往返校区
    ("return_college[]", "北校区"),  # 往返校区
    ("return_college[]", "中校区"),  # 往返校区
    ("reason", "上课"),  # 原因
]
out_school_data = [
    ("return_college[]", "蜀山区"),  # 去往的区
    ("return_college[]", "包河区"),  # 去往的区
    ("reason", "取快递"),  # 原因
]
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="URC nCov auto report script.")
    parser.add_argument("stuid", help="your student number", type=str)
    parser.add_argument("password", help="your CAS password", type=str)
    parser.add_argument("--out", help="out school or not", type=int, default=0)
    parser.add_argument("--cross", help="cross campus or not", type=int, default=1)
    parser.add_argument("--report", help="report or not", type=int, default=1)
    args = parser.parse_args()
    autorepoter = Report(stuid=args.stuid, password=args.password)
    count = 5
    while count != 0:
        ret = True
        if args.report:
            ret = ret & autorepoter.report(report_data)
        if args.cross:
            ret = ret & autorepoter.cross_campus(cross_campus_data)
        if args.out:
            ret = ret & autorepoter.out_school(out_school_data)
        if ret:
            print("ENJOY YOUR FREEDOM! ")
            break
        print("Retry...")
        count = count - 1
    if count != 0:
        exit(0)
    else:
        exit(-1)
