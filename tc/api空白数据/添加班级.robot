*** Settings ***
Library  pyLib.schoolClassLib.SchoolClassLib
Library  pyLib.varType
Variables  cfg.py

*** Test Cases ***
添加班级1-tc000001
    # 1.添加一个班级（班级号 班级名称 最多人数）
    ${addRes}  add school class  ${g_grade_7_id}  1班  60
    log to console  添加班级：${addRes}
    should be true  $addRes['retcode']==0         # python表达式里的0就是int型
    # 2.验证添加班级的数据
    ${listRes}  list school class  ${g_grade_7_id}
    log to console  列出班级：${listRes}
    ${fc}  evaluate  $listRes['retlist'][0]     # 获取该年级的班级的第一条数据（添加第一条，实际也只有这一条）
    should be true  $fc['grade__name'] == "七年级"
    should be true  $fc['name'] == "1班"
    should be true  $fc['studentlimit'] == 60
    should be true  $fc['invitecode'] == $addRes['invitecode']
    should be true  $fc['id'] == $addRes['id']

    # 3.数据清除：删除新增点的用例
    [Teardown]  del school class  ${addRes}[id]



