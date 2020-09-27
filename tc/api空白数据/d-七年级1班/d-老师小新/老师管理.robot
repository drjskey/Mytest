*** Settings ***
Library  pyLib.schoolTeacherLib.SchoolTeacherLib
Library  pyLib.schoolClassLib.SchoolClassLib
Variables  cfg.py

*** Test Cases ***
添加老师2 - tc001002
    # 1.增加老师雪蹄(注册名、所教学科id、手机号都与已存在的不相同)
    ${addTeacher}  add teacher  雪蹄老师  雪蹄  ${middle_science_id}   #学科id
                    ...  ${suite_g7c1_classid}  # 班级id
                    ...  13600001002  xueti@123.com  3209251983090987802
    should be true  $addTeacher['retcode']==0
    # 2.列出老师
    ${listTeacher}  list teacher  ${middle_science_id}          # 也可以不要学科id，直接列出全部
    ${listRes}  evaluate  $listTeacher['retlist']
    # 3.检查所添加的老师是否在列表里
    #(老师列表,老师注册名,真实姓名,所教授的课程,老师id,电话号码,邮箱,身份证号,期望包含次数(缺省1))
    teacherlist_should_contain  ${listRes}  雪蹄老师  雪蹄  ${suite_g7c1_classid}
    ...  ${addTeacher}[id]  13600001002  xueti@123.com  3209251983090987802
    # 4.删除增加的班级
    [Teardown]  del_teacher  ${addTeacher}[id]

添加老师3 - tc001003    # 登录名已存在
    # 1.列出老师，方便之后对比
    ${listBefor}  list teacher
    # 2.增加老师雪蹄(注册名、所教学科id、手机号都与已存在的不相同)
    ${addTeacher}  add teacher  小新老师  小新  ${middle_English_id}   #学科id
                    ...  ${suite_g7c1_classid}  # 班级id
                    ...  13600001003  xiaox@123.com  3209251983090987803
    should be true  $addTeacher['retcode']==1
    should be true  $addTeacher['reason']=="登录名 小新老师 已经存在"
    # 3.再次列出老师，断言列表没有任何改变
    ${listAfter}  list teacher
    should be true  $listBefor['retlist']==$listAfter['retlist']

修改老师1 - tc001051     # id不存在
    # 1.修改老师
    ${modRes}=  mod_teacher  999999  皮皮老师
    should be true  $modRes['retcode']==1
    should be true  $modRes['reason']=="id 为`999999`的老师不存在"

修改老师2 - tc001052     # 修改真实名和授课班级，班级由原来的1个改为2个(缺省参数怎么传递？)
    # 1.添加一个班级，七年级2班（要用到两个，但环境只有一个）
    ${addRes}=  add school class  ${g_grade_7_id}  2班  60
    ${classid}=  evaluate  $addRes['id']
    should be true  $addRes['retcode']==0
    # 2.添加一个有一个班级的老师（提供修改，不改变环境数据）
    ${addTeacher}  add teacher  雪蹄老师  雪蹄  ${middle_science_id}   #学科id
                    ...  ${suite_g7c1_classid}  # 班级id
                    ...  13600001002  xueti@123.com  3209251983090987802
    ${teacherid}=  evaluate  $addTeacher['id']
    should be true  $addTeacher['retcode']==0
    # 3.修改老师（# 缺省参数可以直接指定，但这里系统存在bug，所以必须挨个填写）
    ${modRes}=  mod_teacher  ${addTeacher}[id]  皮皮  ${middle_science_id}
                 ...  classids=${suite_g7c1_classid},${classid}    # 缺省参数可以指定填写
    should be true  $modRes['retcode']==0
    # 4.列出老师，验证修改前数据不在列表中，修改后的数据在列表中
    ${listTeacher}  list teacher
    teacherlist_should_contain  ${listTeacher}[retlist]  雪蹄老师  雪蹄  ${suite_g7c1_classid}
    ...  ${teacherid}  13600001002  xueti@123.com  3209251983090987802  0      # 原来数据包含0次
    teacherlist_should_contain  ${listTeacher}[retlist]  雪蹄老师  皮皮  ${suite_g7c1_classid},${classid}
    ...  ${teacherid}  13600001002  xueti@123.com  3209251983090987802  1      # 修改够的数据数据包含1次
    # 4.数据恢复
    [Teardown]  run keywords  del teacher  ${teacherid}
    ...  AND  del school class  ${classid}

#修改老师2 - tc001052     # 修改真实名和授课班级，班级由原来的1个改为2个(缺省参数挨着传值的)
#    # 1.添加一个班级，七年级2班（要用到两个，但环境只有一个）
#    ${addRes}=  add school class  ${g_grade_7_id}  2班  60
#    ${classid}=  evaluate  $addRes['id']
#    should be true  $addRes['retcode']==0
#    # 2.添加一个有一个班级的老师（提供修改，不改变环境数据）
#    ${addTeacher}  add teacher  雪蹄老师  雪蹄  ${middle_science_id}   #学科id
#                    ...  ${suite_g7c1_classid}  # 班级id
#                    ...  13600001002  xueti@123.com  3209251983090987802
#    ${teacherid}=  evaluate  $addTeacher['id']
#    should be true  $addTeacher['retcode']==0
#    # 3.修改老师
#    ${modRes}=  mod_teacher  ${addTeacher}[id]  皮皮  ${middle_science_id}  ${suite_g7c1_classid},${classid}
#    should be true  $modRes['retcode']==0
#    # 4.列出老师，验证修改前数据不在列表中，修改后的数据在列表中
#    ${listTeacher}  list teacher
#    teacherlist_should_contain  ${listTeacher}[retlist]  雪蹄老师  雪蹄  ${suite_g7c1_classid}
#    ...  ${teacherid}  13600001002  xueti@123.com  3209251983090987802  0      # 原来数据包含0次
#    teacherlist_should_contain  ${listTeacher}[retlist]  雪蹄老师  皮皮  ${suite_g7c1_classid},${classid}
#    ...  ${teacherid}  13600001002  xueti@123.com  3209251983090987802  1      # 修改够的数据数据包含1次
#    # 4.数据恢复
#    [Teardown]  run keywords  del teacher  ${teacherid}
#    ...  AND  del school class  ${classid}

删除老师1 - tc001081
    ${delRes}  del teacher  999999
    should be true  $delRes['retcode']==404
    should be true  $delRes['reason']=="id 为`999999`的老师不存在"

删除老师2 - tc001082
    # 1.新增老师（避免删除环境的数据）
    ${addTeacher}  add teacher  雪蹄老师  雪蹄  ${middle_science_id}   #学科id
                    ...  ${suite_g7c1_classid}  # 班级id
                    ...  13600001002  xueti@123.com  3209251983090987802
    should be true  $addTeacher['retcode']==0
    # 2.列出老师并检查添加的老师在列表里
    ${listTeacher}  list teacher           # 也可以不要学科id，直接列出全部
    teacherlist_should_contain  ${listTeacher}[retlist]  雪蹄老师  雪蹄  ${suite_g7c1_classid}
    ...  ${addTeacher}[id]  13600001002  xueti@123.com  3209251983090987802
    # 3.删除该老师
    ${delRes}  del teacher  ${addTeacher}[id]
    should be true  $delRes['retcode']==0
    # 4.再次列出老师并检查刚删除的老师已经不在列表中
    ${listAfter}  list teacher
    teacherlist_should_contain  ${listAfter}[retlist]  雪蹄老师  雪蹄  ${suite_g7c1_classid}
    ...  ${addTeacher}[id]  13600001002  xueti@123.com  3209251983090987802  0   #包含0次
