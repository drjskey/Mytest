*** Settings ***
Variables  cfg.py
Library  pyLib.schoolClassLib.SchoolClassLib
Suite Setup  add school class  ${g_grade_7_id}  1班  60  web_suite_g7c1_classid
Suite Teardown  del_school_class  ${web_suite_g7c1_classid}    # 按classid删除新增的班级







