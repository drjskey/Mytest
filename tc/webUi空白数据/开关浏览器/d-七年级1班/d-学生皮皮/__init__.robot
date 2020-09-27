*** Settings ***
Variables  cfg.py
Library  pyLib.schoolStudentLib.SchoolStudentLib
Suite Setup   add student  皮皮学生  皮皮   ${g_grade_7_id}
              ...  ${web_suite_g7c1_classid}  15500001001
              ...  web_suite_pp_studentid     # 要保存的学生id名称
Suite Teardown  del student  ${web_suite_pp_studentid}