

import requests,pprint
from cfg import HOST,my_vcode
from robot.api.logger import console
from robot.libraries.BuiltIn import BuiltIn

class SchoolClassLib:
    url = f'http://{HOST}/api/3school/school_classes'
    header = {'Content-Type':'application/x-www-form-urlencoded'}
    def list_school_class(self, gradeid=None):
        """
        列出班级
        :param gradeid: 班级编号
        :return:
        """
        if gradeid != None:
            payload = {"vcode":my_vcode,
                       "action":"list_classes_by_schoolgrade",
                       "gradeid":int(gradeid)}
        else:
            payload = {"vcode": my_vcode,
                       "action": "list_classes_by_schoolgrade"}
        resp = requests.get(url=self.url,params=payload)
        pprint.pprint(f'列出班级返回结果：{resp.json()}')   # 会打印详细内容到log日志，方便调试
        return resp.json()

    def add_school_class(self, grade, name, studentlimit,
                         idSavedName=None):     # 设置一个用来保存返回id的变量名称(不传递表示不需要这个变量)
        """
        添加班级
        :param grade: 班级编号（七年级1，八年级2，九年级3，高一4，高二5，高三6）
        :param name: 班级名称
        :param studentlimit: 班级最多人数
        :param idSavedName:传入需要保存id的变量名
        :return:
        """
        payload = {"vcode":my_vcode,
                   "action":"add",
                   "grade":int(grade),
                   "name":name,
                   "studentlimit":int(studentlimit)}
        resp = requests.post(url=self.url,headers = self.header,data = payload)                         # 会打印到控制台
        pprint.pprint(f'新增班级返回结果：{resp.json()}')  # 会打印详细内容到log日志，方便调试

        if idSavedName:      # 如果idSavedName不为空，表是调用方法是传递了参数，需要返回数据
            """1.传递两个参数（接收的全局变量的名称,需要保存的数据
               2.这里必须要封装为‘${变量名}’格式，因为rf的变量是这种格式，否则出错"""
            BuiltIn().set_global_variable('${%s}'%idSavedName,resp.json()['id'])

        return resp.json()

    def del_school_class(self, classid):
        """
        删除班级
        :param classid: 班级编号
        :return:
        """
        # 不管classid传入的是int还是str，f''字符串拼接都会把classid当做字符串类型来拼接
        del_url = f'{self.url}/{classid}'
        print(del_url)
        payload = {"vcode":my_vcode}
        resp = requests.delete(url=del_url,headers=self.header,data=payload)
        pprint.pprint(f'删除班级返回结果：{resp.json()}')    # 会打印到控制台，方便调试
        return resp.json()

    def del_all_school_classes(self):
        """
        删除所有的班级
        :return:
        """
        # 1- 列出所有班级
        listClasses = self.list_school_class()['retlist']
        print(listClasses)
        # 2- 循环删除所有班级
        for one  in listClasses:
            res = self.del_school_class(one['id'])
            console(f'id为{one["id"]}的班级删除结果：{res}')
        # 3- 再次列出班级，检查是否为空
        listClass = self.list_school_class()
        # print(f'之后的列表：{listClass}')
        assert listClass['retcode'] == 0    # 检查列出班级正常
        assert listClass['retlist'] == []   # 检查列表为空
        print('删除所有班级成功----------------')
        console('删除所有班级成功----------------')

    def classlist_should_contain(self,classlist,classname,gradename,invitecode,
                                 studentlimit,studentnumber,id,exptimes=1):
        """
        判断一个班级(字典)是否在列出班级的列表里,新增修改班级的用例都可以用
        :param classlist: 给出的列表
        :param classname: 班级名称
        :param gradename: 年级
        :param invitecode: 班级邀请码（新增时后台自动生成的）
        :param studentlimit: 班级最多人数
        :param studentnumber: 班级当前人数
        :param id: 班级id号（添加时生成的）
        :return:
        """
        item = {'name':classname,
                'grade__name':gradename,
                'invitecode':invitecode,
                'studentlimit':int(studentlimit),
                'studentnumber':int(studentnumber),
                'id':id,
                'teacherlist':[]}           # 在用例000002里检查老师都为空，所以这里不用检查
        pprint.pprint(f'列出班级：{classlist}')
        pprint.pprint('======================================')
        pprint.pprint(f'预期存在次数的班级：{item}')

        occurTimes = classlist.count(item)              # classlist里包含item的次数
        assert occurTimes == exptimes,f'班级包含了{occurTimes}次指定信息，期望包含{exptimes}次'  # 期望次数缺省1
        # # 也可以用抛出异常的方式
        # if occurTimes !=exptimes:
        #     raise Exception(f'班级包含了{occurTimes}次指定信息，期望包含{exptimes}次')

    def update_school_class(self,classid,classname,studentlimit):
        update_url = f'{self.url}/{classid}'
        payload = {"vcode":my_vcode,
                   "action":"modify",
                   "name":classname,
                   "studentlimit":int(studentlimit)
                    }
        resp = requests.put(update_url,data=payload,headers=self.header)
        print(f'修改班级返回结果：{resp.json()}')
        return resp.json()


if __name__ == '__main__':
    obj = SchoolClassLib()

    #--列出班级
    obj.list_school_class()

    # --添加某个班级
    # res = obj.add_school_class(1,"1班",30)

    # --循环添加班级
    # for i in range(1,5):
    #     obj.add_school_class(i,f"实验{i}班",80)

    # --根据id删除班级
    # obj.del_school_class('452043')

    # --删除所有班级
    # obj.del_all_school_classes()

    # --根据id修改班级
    # obj.update_school_class(453079,'2班',40)


