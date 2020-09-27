

from time import sleep
from pyLib.webBaseLib import WebBaseLib
class WebStudentLib:
    """=====================================学生相关=============================================="""
    def get_student_homepage_info(self):
        """获取学生主页信息"""
        # 点击“主页”
        WebBaseLib.driver.find_element_by_css_selector('a[href="#/home"]>li').click()
        WebBaseLib.driver.find_element_by_css_selector(".img-responsive")
        sleep(1)
        # 返回需要检查的几个数据
        eles = WebBaseLib.driver.find_elements_by_css_selector(".row .ng-binding")
        studentinfo = [ele.text for ele in eles]
        studentinfo.pop(2)        # 把注册码去掉（不验证）
        print(f'获得的老师主页信息：{studentinfo}')
        return studentinfo

    def get_student_wrongquestions(self):
        WebBaseLib.driver.find_element_by_css_selector('a[href="#/yj_wrong_questions"]>li').click()
        sleep(2)
        ele = WebBaseLib.driver.find_element_by_css_selector('#page-wrapper')
        print(ele.text)
        return ele.text

    def student_do_homework(self):
        """学生完成作业"""
        # 点击通知图标
        WebBaseLib.driver.find_element_by_class_name('fa-tasks').click()
        # 找出通知
        eles = WebBaseLib.driver.find_elements_by_css_selector('[ng-click*="checkOneNotifiedTask"]')
        # 如果存在，就点击第一个，否则就退出
        if eles:
            eles[0].click()
        else:
            print('当前没有需要完成的作业')
            return
        sleep(0.2)
        # 点击”去做“按钮
        WebBaseLib.driver.find_element_by_css_selector('[ng-click*="viewTask"]').click()
        # 找出对应的三道题
        eles = WebBaseLib.driver.find_elements_by_css_selector('.btn-group')
        for ele in eles:
            # 找到ABCD四个答案
            answers = ele.find_elements_by_tag_name('button')
            # 都选择B答案
            answers[1].click()

        # 点击”提交“按钮
        WebBaseLib.driver.find_element_by_css_selector('[ng-click*="saveMyResult"]').click()
        sleep(0.5)
        # 点击”确定“
        WebBaseLib.driver.find_element_by_css_selector('.bootstrap-dialog-footer-buttons button:nth-child(2)').click()


if __name__ == '__main__':
    obj=WebStudentLib()
    """=======学生相关======"""
    obj.student_do_homework()
    #
    obj.user_login('小新老师', '888888', False)
    obj.teacher_check_homework()
    sleep(5)
    obj.close_browser()


    obj.user_login('小新老师','888888',False)
    obj.teacher_assign_homework('第一次作业')
    obj.user_login('叶子学生','888888')
    obj.student_do_homework()
    obj.user_login('小新老师', '888888', False)
    obj.teacher_check_homework()