*** Settings ***
Library  pyLib.schoolTeacherLib.SchoolTeacherLib
Library  pyLib.schoolStudentLib.SchoolStudentLib
Library  pyLib.webTeacherLib.WebTeacherLib
Library  pyLib.webBaseLib.WebBaseLib
Library  pyLib.webStudentLib.WebStudentLib
Variables  cfg.py


*** Test Cases ***
老师登录1 - tc005001    # 有班级，没有学生的登录
    # 1.添加老师                  (登录名 真实名 教授学科ID 电话 邮箱 身份证号 所教班级id)
    ${addTeacher}  add teacher  小新老师  小新  ${middle_math_id}
                    ...  ${web_suite_g7c1_classid}
                    ...  13600001001  xiaoxin@123.com  3209251983090987899
    should be true  $addTeacher['retcode']==0
    # 2.登录
    user_login  小新老师  888888  ${False}
    # 3.获取主页信息并检查
    ${teacherinfo}  get teacher homepage info
    should be true  $teacherinfo==['松勤学院01084','小新','初中数学','0','0','0']
    # 4.获取班级学生信息并检查
    ${classStudent}  get_teacher_class_student_info
    log  ${classStudent}
    should be true  $classStudent=={'七年级1班':[]}
    # 5.数据恢复
    [Teardown]  del teacher  ${addTeacher}[id]

学生登录1 - tc005081   #有班级，没有老师，没有学生的学生登录
    # 1.创建学生
    ${addRes}=  add student  皮皮宝贝  皮皮   ${g_grade_7_id}
                ...  ${web_suite_g7c1_classid}  19900001001
    should be true  $addRes['retcode']==0
    # 2.学生登录
    user_login  皮皮宝贝  888888
    # 3.获取首页信息并检查
    ${studentinfo}  get student homepage info
    should be true  $studentinfo==['皮皮','松勤学院01084','0','0']
    # 4.获取错题库验证
    ${wrongquestings}  get_student_wrongquestions
    should be true  $wrongquestings=='您尚未有错题入库哦'
    # 5.数据恢复
    [Teardown]  del student  ${addRes}[id]