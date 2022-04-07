import argparse
from Report import Report

want_report = True  # 是否每日打卡
want_cross_campus = True  # 是否跨校区报备
want_out_school = True  # 是否申请出校
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
cross_campus_data = [
    ("return_college[]", "东校区"),
    ("return_college[]", "西校区"),
    ("return_college[]", "南校区"),
    ("return_college[]", "北校区"),
    ("return_college[]", "中校区"),
    ("reason", "上课"),
    ("t", "3"),
]
out_school_data = [
    ("return_college[]", "蜀山区"),
    ("return_college[]", "包河区"),
    ("reason", "取快递"),
    ("t", "2"),
]
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="URC nCov auto report script.")
    parser.add_argument("stuid", help="your student number", type=str)
    parser.add_argument("password", help="your CAS password", type=str)
    args = parser.parse_args()
    autorepoter = Report(stuid=args.stuid, password=args.password)
    count = 5
    while count != 0:
        ret = True
        if want_report:
            ret = ret & autorepoter.report(report_data)
        if want_cross_campus:
            ret = ret & autorepoter.cross_campus(cross_campus_data)
        if want_out_school:
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
