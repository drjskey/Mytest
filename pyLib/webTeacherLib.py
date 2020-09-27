
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
# from pyLib.WebBaseLib import WebBaseLib
from pprint import pprint
from pyLib.webBaseLib import WebBaseLib
class WebTeacherLib:
    """==========================================老师相关=========================================="""
    def get_teacher_homepage_info(self):
        # 点击“主页”
        WebBaseLib.driver.find_element_by_css_selector('a[href="#/home"]>li').click()
        WebBaseLib.driver.find_element_by_css_selector(".img-responsive")
        sleep(1)
        # 返回需要检查的几个数据
        eles = WebBaseLib.driver.find_elements_by_css_selector(".ng-binding")[1:]  # 不要第一个（是主页的元素）
        print([ele.text for ele in eles])
        return [ele.text for ele in eles]

    def get_teacher_class_student_info(self):
        """获取老师页面基本信息"""
        # 鼠标悬停在“班级情况”（这里也可以通过点击）
        ele = WebBaseLib.driver.find_element_by_css_selector(".main-menu li:nth-of-type(4)")
        ActionChains(WebBaseLib.driver).move_to_element(ele).perform()
        # 点击"班级学生"
        WebBaseLib.driver.find_element_by_css_selector(".fa-sitemap + span").click()
        sleep(1)
        """
        # 获取每个班级的学生信息,组合称面的格式
        {
        "x1班":["学生名1","学生名2","学生名3"]
        "x2班":["学生名1","学生名2","学生名3"]
        }
        """
        classStudentTable = {}
        # 找到所有的班级
        classes = WebBaseLib.driver.find_elements_by_css_selector(".panel-green")
        for classinfo in classes:
            print(f'班级名称:{classinfo.text}')
            # 取出班级名称
            className = classinfo.text.replace(" ","")
            # 把【"班级名称":[]】格式添加到字典classStudentTable
            classStudentTable[className] = []
            # 点击这个班级的标签（才会出现学生信息）
            classinfo.click()
            sleep(1)  # 等待信息加载
            # 获得当前班级的所有学生真实名字（在当前班级classinfo里找）
            eles = classinfo.find_elements_by_css_selector("tbody .ng-scope td:nth-child(2)>span")
            # 循环获取学生名字并按要求格式添加
            for name in eles:
                print(f'学生真实名字:{name.text}')
                studentName = name.text.strip()
                #在当前班级的值里添加学生名字
                classStudentTable[className].append(studentName)
        pprint(classStudentTable)
        return classStudentTable

    def teacher_assign_homework(self,workname):
        """老师下发作业"""
        # 鼠标悬停在“作业”（也可以点击）
        ele = WebBaseLib.driver.find_element_by_css_selector('.main-menu>ul>li:nth-of-type(2)>a')
        ActionChains(WebBaseLib.driver).move_to_element(ele).perform()
        # 点击“+创建作业”
        WebBaseLib.driver.find_element_by_css_selector('a[ng-click="show_page_addexam()"] span').click()
        sleep(1)
        # 作业名称框输入作业名称
        WebBaseLib.driver.find_element_by_css_selector('#tbody_question_body input').send_keys(workname)
        # 点击“从题库选择题目”('[ng-click="gotoPickQuestion()"]')
        sleep(1)
        WebBaseLib.driver.find_element_by_id('btn_pick_question').click()
        sleep(1)
        # 切换到找到iframe
        iframeEle = WebBaseLib.driver.find_element_by_id('pick_questions_frame')
        WebBaseLib.driver.switch_to.frame(iframeEle)
        # 找到当前页面的多个“加入试题篮”按钮
        """这里直接选择出来多个，点击一次加入，后可能页面重新加载，所以可能出错，每次点击后都重新获取一次元素"""
        # for i in range(3):
        #     eles = WebBaseLib.driver.find_elements_by_class_name('btn_pick_question')
        #     eles[i].click()
        eles = WebBaseLib.driver.find_elements_by_class_name('btn_pick_question')[:3]
        for ele in eles:
            ele.click()

        sleep(0.5)
        # 点击“确定”
        WebBaseLib.driver.find_element_by_css_selector('.btn-blue').click()
        sleep(0.5)
        # 从frame中跳回默认的地方
        WebBaseLib.driver.switch_to.default_content()
        # 点击“确定添加”
        WebBaseLib.driver.find_element_by_id('btn_submit').click()

        """下发作业"""
        # 点击“发布给学生”
        WebBaseLib.driver.find_element_by_css_selector('.bootstrap-dialog-footer-buttons button:nth-child(2)').click()
        sleep(2)
        # 找到所有的标签页句柄，并切换到对应的标签页
        all_handle = WebBaseLib.driver.window_handles
        WebBaseLib.driver.switch_to.window(all_handle[1])
        # 找到所有的学生并勾选
        WebBaseLib.driver.implicitly_wait(1)
        studenteles = WebBaseLib.driver.find_elements_by_css_selector('.myCheckbox')
        for ele in studenteles:
            ele.click()
        WebBaseLib.driver.implicitly_wait(5)
        # 点击“确定发布”
        WebBaseLib.driver.find_element_by_css_selector('[ng-click*="openDispatchDlg"]').click()
        sleep(1)
        # 再点击“确定”
        WebBaseLib.driver.find_element_by_css_selector('[ng-click="dispatchIt()"]').click()
        # 还要点击一个弹框的“确定”
        WebBaseLib.driver.find_element_by_css_selector('.bootstrap-dialog-footer-buttons button').click()
        sleep(1)
        WebBaseLib.driver.switch_to.window(all_handle[0])

    def teacher_check_homework(self):
        # 鼠标悬停在“作业”
        ele = WebBaseLib.driver.find_element_by_css_selector('.main-menu>ul>li:nth-of-type(2)>a')
        ActionChains(WebBaseLib.driver).move_to_element(ele).perform()
        # 点击”已发布的作业“
        WebBaseLib.driver.find_element_by_css_selector('.main-menu li:nth-of-type(2) .fa-bell-o+span').click()
        sleep(2)
        # 找到完成情况的图标
        eles = WebBaseLib.driver.find_elements_by_css_selector('tbody td:nth-of-type(5) .fa-search')
        # 如果存在就点击第一个
        if eles:
            eles[0].click()
        # 找到有“查看”状态的元素（“查看代表已完成”）
        eles = WebBaseLib.driver.find_elements_by_css_selector('[ng-click*="viewTaskTrack"]')
        if eles:
            eles[0].click()   # 点击第一个“查看”
        # 切换句柄
        all_handles = WebBaseLib.driver.window_handles
        WebBaseLib.driver.switch_to.window(all_handles[1])
        sleep(1)
        """=======获取这几道题的答案，返回列表======="""
        # 获得每一道题答案行的大元素
        eles = WebBaseLib.driver.find_elements_by_css_selector('[ng-if="examSubmitted"]')
        choices = []
        for ele in eles:
            # 找到当前题目的勾选选项（直接查看元素没有区别，这里用js实现，有'.myCheckbox input:checked'这个修饰）
            checkbox = ele.find_elements_by_css_selector('.myCheckbox input:checked')
            str = ''
            for i in checkbox:
                # 找到i的父元素，得到文本信息（这里定位到的是<span>,文本信息在父元素里）
                temp = i.find_element_by_xpath('./..').text.strip()
                str = str+','+temp      # 多个答案拼接起来，逗号隔开
            choices.append(str.strip(','))  # 去掉前后的逗号后再添加到列表
        print(f'得到的答案：{choices}')
        WebBaseLib.driver.switch_to.window(all_handles[0])
        return choices

if __name__ == '__main__':
    obj=WebTeacherLib()
    obj.open_browser()

    """=======老师相关====="""
    obj.user_login('小新老师','888888',False)
    # obj.get_teacher_homepage_info()
    # # # # # obj.get_teacher_class_student_info()
    obj.teacher_assign_homework('第一次作业')
    # obj.teacher_check_homework()
    """=======学生相关======"""
