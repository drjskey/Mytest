*** Settings ***
Library  pyLib.schoolClassLib.SchoolClassLib
Library  cases/C000002.py  WITH NAME  C2
Library  cases/C000003.py  WITH NAME  C3

*** Test Cases ***
添加班级2 - tc000002
    [Setup]  C2.setup
    [Teardown]  C2.teardown
    C2.testCase

添加班级3 - tc000003           # 此用例，系统存在bug，返回的reason错误
    [Setup]  C3.setup
    [Teardown]  C3.teardown
    C3.testCase




