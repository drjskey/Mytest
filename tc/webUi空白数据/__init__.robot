*** Settings ***
Library  pyLib.schoolClassLib.SchoolClassLib
Library  pyLib.schoolTeacherLib.SchoolTeacherLib
Library  pyLib.schoolStudentLib.SchoolStudentLib
Suite Setup  run keywords   del_all_teachers
             ...  AND  del_all_student
             ...  AND  del_all_school_classes
