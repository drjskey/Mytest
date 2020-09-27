# -*- coding: utf-8 -*-
# project : YJYX_pyCase
# time : 2020/8/11 17:14
from pyLib.schoolClassLib import SchoolClassLib
import pprint

sc = SchoolClassLib()

class C000002:
    def setup(self):
        pass

    def teardown(self):
        sc.del_school_class(self.addRes['id'])

    def testCase(self):
        print("***** step 1 ***** 添加7年级2班(年级与初始化已有年级相同，但班级不同) ******")
        self.addRes = sc.add_school_class(1,'2班',60)
        assert self.addRes['retcode']==0,'返回值不为0'   # 断言返回码为0
        print("\n\n***** step 2 ***** 列出班级，检查一下 ******\n")
        listRes = sc.list_school_class(1)
        classlist = listRes['retlist']                # 列出班级列表
        item = {'name': '2班',
                'grade__name': '七年级',
                'invitecode': self.addRes['invitecode'],
                'studentlimit': 60,
                'studentnumber': 0,
                'id': self.addRes['id'],
                'teacherlist': []}  # 在用例000002里检查老师都为空，所以这里不用检查
        pprint.pprint(f'列出班级：{classlist}')
        pprint.pprint('======================================')
        pprint.pprint(f'预期存在的班级：{item}')

        occurTimes = classlist.count(item)  # classlist里包含item的次数
        assert item in classlist, '班级列表里没有该班级'  # 断言包含关系
        assert occurTimes == 1, f'班级包含了{occurTimes}次指定信息，期望包含1次'


if __name__ == '__main__':
    # obj = C000002()
    # obj.testCase()
    sc.add_school_class(1, '2班', 60)