*** Settings ***
Library  pyLib.schoolTeacherLib.SchoolTeacherLib
Variables  cfg.py

*** Test Cases ***
添加老师1 - tc001001
    # 1.添加老师                  (登录名 真实名 教授学科ID 电话 邮箱 身份证号 所教班级id)
    ${addTeacher}  add teacher  小新老师  小新  ${middle_math_id}
                    ...  ${suite_g7c1_classid}
                    ...  13600001001  xiaoxin@123.com  3209251983090987899
    should be true  $addTeacher['retcode']==0
    # 2.列出老师
    ${listTeacher}  list teacher  ${middle_math_id}
    ${listRes}  evaluate  $listTeacher['retlist']
    # 3.检查所添加的老师是否在列表里
    #(老师列表,老师注册名,真实姓名,所教授的课程,老师id,电话号码,邮箱,身份证号,期望包含次数(缺省1))
    teacherlist_should_contain  ${listRes}  小新老师  小新  ${suite_g7c1_classid}
    ...  ${addTeacher}[id]  13600001001  xiaoxin@123.com  3209251983090987899
    # 4.删除增加的班级
    [Teardown]  del_teacher  ${addTeacher}[id]

