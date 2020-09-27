*** Settings ***
Variables  cfg.py
Library  pyLib.schoolStudentLib.SchoolStudentLib
Library  pyLib.webTeacherLib.WebTeacherLib
Library  pyLib.webBaseLib.WebBaseLib
Library  pyLib.webStudentLib.WebStudentLib

*** Test Cases ***
老师发布作业1 - tc005101
    # 1.老师登录
    user login  小新老师  888888  ${False}
    # 2.老师布置作业
    teacher assign homework  第一次作业
    # 3.学生登录
    user login  叶子学生  888888
    # 4.学生完成作业
    student do homework
    # 5.老师登录
    user login  小新老师  888888  ${False}
    # 6.老师打开页面，检查作业勾选的选项是否与学生做题勾选的一致
    ${answers}  teacher check homework
    should be true  $answers==['B','B','B']