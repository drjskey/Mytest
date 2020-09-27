*** Settings ***
Library  pyLib.schoolStudentLib.SchoolStudentLib
Variables  cfg.py

*** Test Cases ***
添加学生2 - tc002002   #存在班级老师和学生，添加一个没有重复注册名的学生
    # 1.添加学生
    ${addRes}=  add_student  樊樊学生  樊樊   ${g_grade_7_id}  ${suite_g7c1_classid}  19900001001
    should be true  $addRes['retcode']==0
    # 2.列出学生
    ${listRes}=  list_student
    ${retlist}=  evaluate  $listRes['retlist']
    # 3.判断新增成功
    studentlist should contain  ${retlist}  ${suite_g7c1_classid}
                                ...  樊樊  樊樊学生  19900001001  ${addRes}[id]
    # 4.数据恢复
    [Teardown]  del student  ${addRes}[id]

添加学生3 - tc002003   #存在班级老师和学生，添加一个重复注册名的学生
    # 1.列出学生，与之后对比
    ${listBefor}  list student
    # 2.添加学生
    ${addRes}=  add_student  叶子学生  樊樊   ${g_grade_8_id}  ${suite_g7c1_classid}  19900001002
    should be true  $addRes['retcode']==1
    should be true  $addRes['reason']=="登录名`叶子学生`已经存在，请换一个登录名"
    # 3.再次列出学生
    ${listAfter}  list student
    # 4.判断数据没有改变（没添加成功）
    should be true  $listBefor['retlist'] == $listAfter['retlist']

修改学生1 - tc002051    # 修改一个id不存在的学生数据
    # 1.列出学生，与之后对比
    ${listBefor}  list student
    # 2.修改学生
    ${modRes}  mod student  999999
    should be true  $modRes['retcode']==404
    should be true  $modRes['reason']=="id 为`999999`的学生不存在"
    # 3.再次列出学生
    ${listAfter}  list student
    # 4.判断数据没有改变（数据没任何改变成功）
    should be true  $listBefor['retlist'] == $listAfter['retlist']

修改学生2 - tc002052     # 修改学生数据成功
    # 1.添加学生（不去修改环境数据）
    ${addRes}=  add_student  樊樊学生  樊樊   ${g_grade_7_id}  ${suite_g7c1_classid}  19900001001
    should be true  $addRes['retcode']==0
    # 2.修改学生
    ${modRes}  mod student  ${addRes}[id]  樊二
    # 3.列出学生列表
    ${listRes}  list student
    ${retlist}  evaluate  $listRes['retlist']
    # 4.检查原数据不在列表里，新数据在列表里
    studentlist should contain  ${retlist}  ${suite_g7c1_classid}
                                ...  樊樊  樊樊学生  19900001001  ${addRes}[id]  0
    studentlist should contain  ${retlist}  ${suite_g7c1_classid}
                                ...  樊二  樊樊学生  19900001001  ${addRes}[id]
    # 5.数据恢复
    [Teardown]  del student  ${addRes}[id]

删除学生1 - tc002081   # 删除存在的学生
    # 1.添加学生（不去修改环境数据）
    ${addRes}=  add_student  樊樊学生  樊樊   ${g_grade_7_id}  ${suite_g7c1_classid}  19900001001
    should be true  $addRes['retcode']==0
    # 2.列出学生，检查存在列表中
    ${listBefor}  list student
    studentlist should contain  ${listBefor}[retlist]  ${suite_g7c1_classid}
                                ...  樊樊  樊樊学生  19900001001  ${addRes}[id]
    # 3.删除学生
    ${delRes}  del student  ${addRes}[id]
    should be true  $delRes['retcode']==0
    # 4.再次列出学生，检查刚新增的数据已经不存在
    ${listAfter}  list student
    studentlist should contain  ${listAfter}[retlist]  ${suite_g7c1_classid}
                                ...  樊樊  樊樊学生  19900001001  ${addRes}[id]  0

删除学生2 - tc002082    # 删除不存在的学生
    # 1.列出学生
    ${listBefor}  list student
    # 2.删除学生
    ${delRes}  del student  999999
    # 3.再次列出学生，对比前后两次没变化
    ${listAfter}  list student
    should be true  $listBefor['retlist']==$listAfter['retlist']