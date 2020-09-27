*** Settings ***
Library  pyLib.schoolClassLib.SchoolClassLib
Library  pyLib.varType
Variables  cfg.py

*** Test Cases ***
添加班级2 - tc000002
    [Documentation]  添加一个班级（年级相同，但班级名不同）
    # 1.添加一个班级（年级相同，但班级不同）：rf框架1班与001用例相同，但年级不同
    ${addRes}  add school class  ${g_grade_7_id}  2班  60
    log to console  添加班级：${addRes}
    should be true  $addRes['retcode']==0         # python表达式里的0就是int型
    # 2.列出班级，检查一下
    ${listRes}  list school class  ${g_grade_7_id}
    ${retlist}  evaluate  $listRes['retlist']
    log to console  列出班级：${retlist}
    # rf里最好不要写这么复杂的表达式，我们可以放在py里写为关键字
    # should be true  {'name':'2班','grade__name':'七年级','invitecode':$addRes['invitecode'],'studentlimit':60,'studentnumber':0,'id':$addRes['id'],'teacherlist':[]} in $retlist
    # 关键字检查一个班级是否在列出班级的列表里（列出班级列表  班级名称 年级   班级代码     班级最多人数 班级当前人数 班级id）
    classlist should contain  ${retlist}  2班  七年级  ${addRes}[invitecode]  60  0  ${addRes}[id]
    # 3.数据清除：删除新增点的用例
    [Teardown]  del school class  ${addRes}[id]

添加班级3 - tc000003           # 此用例，系统存在bug，返回的reason错误
    [Documentation]  添加一个班级(班级号和班级名称都已经存在)，此用例，系统存在bug，返回的reason错误
    # 1.先列出班级，为后面检查做准备
    ${listBefore}  list school class  ${g_grade_7_id}
    # 2.添加一个班级（班级号和班级名称都已经存在，初始化环境存在七年级一班）
    ${addRes}  add school class  ${g_grade_7_id}  1班  60
    # 3.检查响应数据
    should be true  $addRes['retcode']==1
    should be true  $addRes['reason']=="duplicated class name"
    # 4.检查列出班级结果不包含刚才添加的数据
    ${listAfter}  list school class  ${g_grade_7_id}
    should be true  $listBefore  $listAfter

修改班级1 - tc000051    # 最好别修改初始化的数据，否则如果数据恢复没正确改回来会影响其他用例环境
    [Documentation]  修改班级名称(新名称改年级不存在)
    # 1.添加班级（七年级2班），返回id
    ${addRes}  add school class  ${g_grade_7_id}  2班  60
    should be true  $addRes['retcode']==0
    ${classid}  evaluate  $addRes['id']      #获取id值
    # 2.修改id存在的班级（修改班级名当前年级不存在）
    ${updclass}  update_school_class  ${classid}  3班  30   #数据环境知道现在有1班和2班
    should be true  $updclass['retcode']==0
    # 3.再次列出班级
    ${retlist}  list school class  ${g_grade_7_id}
    # 4.检查修改后的数据
    ${modlist}  evaluate  $retlist['retlist']
    classlist should contain  ${modlist}  3班  七年级  ${addRes}[invitecode]  30  0  ${classid}
    # 5.数据恢复，删除新建的班级
    [Teardown]  del school class  ${classid}

修改班级2 - tc000052
    [Documentation]  修改班级名为该年级已经存在的班级名，此用例系统存在bug
    # 1.添加班级（七年级2班），返回id
    ${addRes}  add school class  ${g_grade_7_id}  2班  60
    should be true  $addRes['retcode']==0
    ${classid}  evaluate  $addRes['id']      #获取id值
    # 2.列出原来数据，方便后面检查时候
    ${listbefore}  list school class  ${g_grade_7_id}
    # 3.修改id存在的班级（修改班级名为存在的）
    ${updclass}  update_school_class  ${classid}  1班  30
    should be true  $updclass['retcode']==1
    should be true  $updclass['reason']=="duplicated class name"
    # 4.列出班级
    ${listafter}  list school class  ${g_grade_7_id}
    # 5.检查没有刚修改后的数据存在
    should be equal  ${listbefore}  ${updclass}
    # 6.数据恢复，删除新建的班级
    [Teardown]  del school class  ${classid}

修改班级3 - tc000053
    [Documentation]  修改班级id为不存在的
    ${updclass}  update_school_class  999999  1班  60     # id写一个很大很少可能的（也可以去列出班级后取不存在的）
    should be true  $updclass['retcode']==404
    should be true  $updclass['reason']=="id 为`999999`的班级不存在"   # id后有个空格

删除班级1 - tc000081
    [Documentation]  用不存在的id号请求删除班级
    ${defRes}  del_school_class  999999
    should be true  $defRes['retcode']==404
    should be true  $defRes['reason']=='id 为`999999`的班级不存在'

#删除班级2 - tc000082      #没有用到自己定义包含关系
#    # 1.新增班级：七年级2班（为了不影响原来环境）
#    ${addRes}  add school class  ${g_grade_7_id}  2班  60
#    should be true  $addRes['retcode']==0
#    ${classid}  evaluate  $addRes['id']      #获取id值
#    # 2.列出班级，方便比较
#    ${listRes}  list school class  ${g_grade_7_id}
#    ${list}  evaluate   $listRes['retlist']
#    FOR  ${i}  IN  @{list}    # 遍历列表，这里一定要拆包
#        ${addclass}  set variable if  $classid==$i['id']  ${i}   #取出刚才新增的数据
#        END
#    # 3.删除该班级
#    ${delRes}  del_school_class  ${classid}
#    should be true  $delRes['retcode']==0
#    # 4.再次列出班级
#    ${listAfter}  list school class  ${g_grade_7_id}
#    ${After}  evaluate   $listAfter['retlist']
#    # 5.检查刚才新增的班级不再列表里
#    should not contain  ${After}  ${addclass}

删除班级2 - tc000082        # 用到自己定义的包含关系
    [Documentation]  正常删除班级
    # 1.新增班级：七年级2班（为了不影响原来环境）
    ${addRes}  add school class  ${g_grade_7_id}  2班  60
    should be true  $addRes['retcode']==0
    ${classid}  evaluate  $addRes['id']      #获取id值
    # 2.检查刚才新增的数据在列表里
    ${listBefore}  list school class  ${g_grade_7_id}
    classlist should contain  ${listBefore}[retlist]  2班  七年级  ${addRes}[invitecode]  60  0  ${classid}
    # 3.删除该班级
    ${delRes}  del_school_class  ${classid}
    should be true  $delRes['retcode']==0
    # 5.检查刚才新增的班级不再列表里（exptimes值默认1，这里我们需要检查为0次）
    ${listAfter}  list school class  ${g_grade_7_id}
    classlist should contain  ${listAfter}[retlist]  2班  七年级  ${addRes}[invitecode]  60  0  ${classid}  0
