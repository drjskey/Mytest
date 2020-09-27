*** Settings ***
Library  pyLib.schoolStudentLib.SchoolStudentLib
Variables  cfg.py

*** Test Cases ***
添加学生1 - tc002001
    # 1.添加学生
    ${addRes}=  add student  叶子学生  叶子   ${g_grade_7_id}
                             ...  ${suite_g7c1_classid}  19900001001
    should be true  $addRes['retcode']==0
    # 2.列出学生
    ${listRes}=  list_student
    ${retlist}=  evaluate  $listRes['retlist']
    # 3.判断新增成功
    studentlist should contain  ${retlist}  ${suite_g7c1_classid}  叶子  叶子学生  19900001001  ${addRes}[id]
#    sleep  1d
    # 4.数据恢复
    [Teardown]  del student  ${addRes}[id]