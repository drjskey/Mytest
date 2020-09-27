*** Settings ***
Variables  cfg.py
Library  pyLib.schoolTeacherLib.SchoolTeacherLib

Suite Setup  add_teacher  小新老师  小新  ${middle_math_id}  # 学科id
            ...  ${web_suite_g7c1_classid}   # 新增老师的班级id
            ...  13600001001  xiaoxin@123.com  3209251983090987899
            ...  web_suite_xx_teacherid                 # 需要得到增加老师返回的id号保存名称
Suite Teardown  del_teacher  ${web_suite_xx_teacherid}