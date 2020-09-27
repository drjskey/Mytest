*** Settings ***
Library  pyLib.schoolTeacherLib.SchoolTeacherLib
Variables  cfg.py
Library  pyLib.webTeacherLib.WebTeacherLib
Library  pyLib.webBaseLib.WebBaseLib


*** Test Cases ***
老师登录2 - tc005002     # 已经有班级 有学生的老师登录
    # 1.添加老师                  (登录名 真实名 教授学科ID 电话 邮箱 身份证号 所教班级id)
    ${addTeacher}  add teacher  小新老师  小新  ${middle_math_id}
                    ...  ${web_suite_g7c1_classid}
                    ...  13600001001  xiaoxin@123.com  3209251983090987899
    should be true  $addTeacher['retcode']==0
    # 2.登录
    user_login  小新老师  888888   ${False}
    # 3.获取主页信息并检查
    ${teacherinfo}  get teacher homepage info
    should be true  $teacherinfo==['松勤学院01084','小新','初中数学','0','0','0']
    # 4.获取班级学生信息并检查
    ${classStudent}  get_teacher_class_student_info
    log  ${classStudent}
    should be true  $classStudent=={'七年级1班':['皮皮']}
    # 5.数据恢复
    [Teardown]  del teacher  ${addTeacher}[id]