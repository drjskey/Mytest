*** Settings ***
Variables  cfg.py
Library  pyLib.schoolStudentLib.SchoolStudentLib
Suite Setup   add student  叶子学生  叶子   ${g_grade_7_id}
              ...  ${suite_g7c1_classid}  19900001001
              ...  suite_yz_studentid     # 要保存的学生id名称
Suite Teardown  del student  ${suite_yz_studentid}

