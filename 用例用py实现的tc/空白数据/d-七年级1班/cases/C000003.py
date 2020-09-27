# -*- coding: utf-8 -*-
# project : YJYX_pyCase
# time : 2020/8/11 17:14
from pyLib.schoolClassLib import SchoolClassLib
import pprint

sc = SchoolClassLib()

class C000003:             # 此用例，系统存在bug，返回的reason错误
    def setup(self):
        pass

    def teardown(self):
        pass

    def testCase(self):      # 此用例，系统存在bug，返回的reason错误
        print("***** step 1 ***** 先列出班级，为后面检查做准备 ******")
        listBefore = sc.list_school_class(1)
        print("***** step 2 ***** 添加一个班级（班级号和班级名称都已经存在 ******")
        addRes =  sc.add_school_class(1,'1班',60)
        print("***** step 3 ***** 检查响应数据 ******")
        assert  addRes['retcode']==1
        assert  addRes['reason']=="duplicated class name"
        print("***** step 4 ***** 检查列出班级结果不包含刚才添加的数据 ******")
        # 4.检查列出班级结果不包含刚才添加的数据
        listAfter = sc.list_school_class(1)
        assert listBefore == listAfter