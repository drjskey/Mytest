
from cfg import HOST,my_vcode
import requests,json,pprint
from robot.api.logger import console
from robot.libraries.BuiltIn import BuiltIn

class SchoolTeacherLib:
    url = f"http://{HOST}/api/3school/teachers"
    header = {'Content-Type':'application/x-www-form-urlencoded'}
    def add_teacher(self,username,realname,subjectid,classids,phone,email,idcar,
                    idSavedName=None):           # 用来保存返回id的变量名
        """
        添加老师，
        :param username: 登录名，不能重复
        :param realname: 真实姓名
        :param subjectid: 所教学科id，(初中数学1,初中科学5,初中英语11,初中体育12,高中语文13,高中数学14)
        :param classids:所教班级id，可填多个（多个班级中间用‘,’隔开）
        :param phone:电话，不能重复
        :param email:邮箱
        :param idcar:身份证号
        :param idSavedName:需要获得返回id时保存id的名称
        :return:
        """
        templist = str(classids).split(',')
        classlist = [{"id":id.strip()} for id in templist if id != '']   # 用户多输入逗号后面没跟另外参数时，会出现空的值
        payload = {"vcode":my_vcode,
                   "action":"add",
                   "username":username,
                   "realname":realname,
                   "subjectid":int(subjectid),
                   "classlist":json.dumps(classlist),
                   "phonenumber":int(phone),
                   "email":email,
                   "idcardnumber":int(idcar)}
        resp = requests.post(self.url,data=payload)
        print(f'增加老师返回结果：{resp.json()}')
        if idSavedName:
            BuiltIn().set_global_variable('${%s}'%idSavedName,resp.json()['id'])
        return resp.json()

    def list_teacher(self,subjectid=None):
        payload = {"vcode":my_vcode,
                   "action":"search_with_pagenation"}
        if subjectid !=None:          # 如果subjectid不为空，把这个键值对加入字典payload
            payload["subjectid"]=subjectid
        resp = requests.get(self.url,params=payload,headers=self.header)
        print(f'列出老师返回结果：{resp.json()}')
        return resp.json()

    def del_teacher(self,teacherid):
        """按id删除老师"""
        del_url= f'{self.url}/{teacherid}'
        payload={"vcode":my_vcode}
        resp = requests.delete(del_url,data=payload)
        print(f'删除老师返回结果：{resp.json()}')
        return resp.json()

    def del_all_teachers(self):
        retlist = self.list_teacher()['retlist']
        for teacher in retlist:
            self.del_teacher(teacher['id'])
        retlistRes = self.list_teacher()
        assert retlistRes['retcode']==0
        assert retlistRes['retlist']==[]
        print(f'删除所有老师完成-----------------------')
        console(f'删除所有老师完成-----------------------')

    def mod_teacher(self,teacherid,realname=None,subjectid=None,classids=None,
                    phonenumber=None,email=None,idcardnumber=None):
        mod_url = f'{self.url}/{teacherid}'
        payload = {"vcode":my_vcode,"action":"modify"}
        if realname !=None:
            payload["realname"]=realname
        if subjectid !=None:
            payload["subjectid"]=subjectid
        if phonenumber !=None:
            payload["phonenumber"]=phonenumber
        if email !=None:
            payload["email"]=email
        if idcardnumber !=None:
            payload["idcardnumber"]=idcardnumber
        if classids != None:
            templist = str(classids).split(',')
            classlist = [{'id':id.strip()} for id in templist if id!='']
            payload["classlist"]=json.dumps(classlist)

        resp = requests.put(mod_url,data=payload)
        print(f'修改老师的返回结果：{resp.json()}')
        return resp.json()

    def teacherlist_should_contain(self,listteacher,teachername,realname,teachclassids,
                                   teacherid,phonenumber,email,idcardnumber,expTimes=1):
        """
        验证老师在列表里的次数
        :param listteacher: 列出老师的列表
        :param teachername: 老师注册名
        :param realname: 真实姓名
        :param teachclasslist: 所教授的班级id列表
        :param id: 老师id
        :param phonenumber: 电话号码
        :param email: 邮箱
        :param idcardnumber: 身份证号
        :param expTimes: 期望包含的次数
        :return:
        """
        # 把传入的‘230,231’格式转为‘[230,231]’这种列表格式
        teachclassids=str(teachclassids)
        templist = teachclassids.split(',')
        teachclasslist = [int(id.strip()) for id in templist if id!='']
        item = {'username': teachername,
                'teachclasslist': teachclasslist,   # 转为json格式
                'realname': realname,
                'id': int(teacherid),
                'phonenumber': str(phonenumber),
                'email':email,
                'idcardnumber': str(idcardnumber)}
        pprint.pprint(f'列出老师：{listteacher}')
        pprint.pprint('======================================')
        pprint.pprint(f'预期存在次数的老师：{item}')

        occureTimes = listteacher.count(item)
        assert occureTimes == expTimes,f'老师包含{occureTimes}次，期望包含{expTimes}次'
        print(f'老师包含{occureTimes}次，期望包含{expTimes}次')


if __name__ == '__main__':
    teacher = SchoolTeacherLib()
    # res = teacher.add_teacher("小新老师","小新",1,463171,13600001004,"jcysdf@123.com",3209251983090987892)
    # teacher.mod_teacher(139202,realname='提提zi',email='1234567@qq.com')
    teacher.list_teacher()
    # list = teacher.list_teacher()['retlist']
    # teacher.del_teacher(455616)
    # teacher.del_all_teachers()
    # teacher.teacherlist_should_contain(list,"xueti3","xueti",458299,138909,'13600001003',
    #                                    "jcysdf@123.com",'3209251983090987899')




