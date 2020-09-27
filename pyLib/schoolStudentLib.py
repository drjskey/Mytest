
from cfg import HOST,my_vcode
import requests
from robot.libraries.BuiltIn import BuiltIn

class SchoolStudentLib:
    url = f"http://{HOST}/api/3school/students"
    header = {'Content-Type':'application/x-www-form-urlencoded'}

    def list_student(self):
        """列出学生"""
        payload = {"vcode":my_vcode,"action":"search_with_pagenation"}
        resp = requests.get(self.url,params=payload)
        print(f'列出学生结果为：{resp.json()}')
        return resp.json()

    def add_student(self,username,realname,gradeid,classid,phonenumber,idSaveName=None):
        """
        添加学生
        :param username: 注册名
        :param realname: 真实名
        :param gradeid: 年级号
        :param classid: 班级id
        :param phonenumber: 电话
        :return:
        """
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {"vcode":my_vcode,
                   "action":"add",
                   "username": username,
                   "realname": realname,
                   "gradeid": int(gradeid),
                   "classid": int(classid),
                   "phonenumber": int(phonenumber)
                    }
        resp = requests.post(self.url,headers=header,data=payload)
        print(f'请求body：{resp.request.body}')
        if idSaveName:
            BuiltIn().set_global_variable('${%s}'%idSaveName,resp.json()['id'])
        print(f'添加学生返回结果：{resp.json()}')
        return resp.json()

    def mod_student(self,studentid,realname=None,phonenumber=None):
        """
        修改学生生
        :param studentid: 学生编号
        :param realname: 真实姓名
        :param phonenumber: 电话
        :return:
        """
        mod_url = f'{self.url}/{studentid}'
        payload = {"vcode":my_vcode,"action":"modify"}
        if realname:
            payload["realname"]=realname
        if phonenumber:
            payload["phonenumber"] = phonenumber
        resp = requests.put(mod_url,data=payload)
        print(f'修改老师请求：{resp.request.body}')
        print(f'修改学生结果为：{resp.json()}')
        return resp.json()

    def del_student(self,studentid):
        """
        删除学生
        :param studentid: 学生id
        :return:
        """
        del_url = f'{self.url}/{studentid}'
        payload = {"vcode":my_vcode}
        resp = requests.delete(del_url,data=payload)
        print(f'学生{studentid}删除结果为：{resp.json()}')
        return resp.json()

    def del_all_student(self):
        """删除所有学生"""
        res = self.list_student()
        if res['retlist']==[]:
            pass
        for student in res['retlist']:
            self.del_student(student['id'])
        print('所有学生删除完成----------------')

    def studentlist_should_contain(self,studentlist,classid,realname,username,phonenumber,studentid,ExpTimes=1):
        """
        判断某个学生在列表里的次数
        :param studentlist: 列出学生的列表
        :param classid: 班级号
        :param realname: 真实姓名
        :param username: 注册名
        :param phonenumber: 电话
        :param studentid: 学生编号
        :param ExpTimes: 期望包含的次数
        :return:
        """
        item = {'classid': int(classid),
                'realname': realname,
                'username': username,
                'phonenumber': phonenumber,
                'id': int(studentid)}
        occurTimes = studentlist.count(item)
        print(f'列出学生列表：{studentlist}')
        print('=========================================')
        print(f'期望包含次数的学生：{item}')
        assert occurTimes==ExpTimes,f'包含{occurTimes}次，预计包含{ExpTimes}次'

if __name__ == '__main__':
    student = SchoolStudentLib()
    student.list_student()
    student.add_student("皮皮宝贝3","皮皮3",1,463504,19900002003)


    # student.mod_student(67329,"hahahah",19900005001)
    # student.del_student(67329)
    # student.del_all_student()
    # # 包含测试
    # studentlist = [{'classid': 459648, 'realname': '雪蹄', 'username': '小新宝贝', 'phonenumber': '19900001001', 'id': 67338},
    #                {'classid': 459648, 'realname': '雪蹄', 'username': '雪蹄宝贝', 'phonenumber': '19900001001', 'id': 67339},
    #                {'classid': 459648, 'realname': '雪蹄', 'username': '小新宝贝', 'phonenumber': '19900001001', 'id': 67338}]
    # student.studentlist_should_contain(studentlist,459648,'雪蹄','小新宝贝','19900001001',67338,2)