*** Settings ***
Library  pyLib.schoolClassLib.SchoolClassLib
Suite Setup  add school class  1  1班  60        # 添加七年级一班
#上一层是空环境，这一层用例执行完，就恢复到空环境状态，否则先执行这里的用例，环境没恢复，在执行空环境用例时环境并不为空
Suite Teardown  del_all_school_classes