*** Settings ***
Variables  cfg.py
Library  pyLib.schoolClassLib.SchoolClassLib
Suite Setup  add school class  ${g_grade_7_id}  1班  60  suite_g7c1_classid
Suite Teardown  del_school_class  ${suite_g7c1_classid}    # 按classid删除新增的班级


#*** Keywords ***
#suite初始化保存返回值
#    ${ret}  add school class  1  1班  60    #添加七年级1班且获得返回值
#    # 把返回数据里的classid保存到一个全局变量里，哪里都可以使用
#    set global variable  ${suite_g7c1_classid}  ${ret}[id]
#
#*** Settings ***
#Library  pyLib.schoolClassLib.SchoolClassLib
#Suite Setup  suite初始化保存返回值
#Suite Teardown  del_school_class  ${suite_g7c1_classid}    # 按classid删除新增的班级




