#coding=utf-8
import pytest
from youdanweb import YoudanWeb
youdan = YoudanWeb()
'''
class TestProduct:
    def setup_class(self):
        youdan.initialize()
    def teardown_class(self):
        youdan.quit()
    def test_get_zgdetails(self):
        youdan.get_product_details(2,3)
    def test_get_xtdetails(self):
        youdan.get_product_details(1,2)
    def test_get_zqdetails(self):
        youdan.get_product_details(3,1)
'''
'''
class TestLogin:
    def setup_class(self):
        youdan.initialize()
    def teardown_class(self):
        youdan.quit()
    def test_login_success(self):
        youdan.login('15914145610','123456')
    def test_login_pwd_error(self):
        youdan.login('15914145610','456789')
'''
'''
class TestUpload:
    def setup_class(self):
        youdan.initialize()
    def teardown_class(self):
        youdan.quit()
    def test_click_upload(self):
        youdan.upload_click()
    def test_set_rakeback1(self):
        youdan.upload_click()
        youdan.set_product_name(u'测试12323432')
        assert u'投资范围1' in youdan.set_rake_back(1)
    def test_set_rakeback2(self):
        youdan.upload_click()
        youdan.set_product_name(u'测试12323432')
        assert u'投资范围1' in youdan.set_rake_back(2)
'''
class TestLogin:
    def setup_class(self):
        youdan.initialize()
    def teardown_method(self):
        youdan.clean_cooike()
    def teardown_class(self):
        youdan.quit()
    '''
    #不输入
    def test_input_null(self):
        youdan.open_homepage()
        youdan.login('','')
        assert youdan.checklogin_button() == 1,u'登录按钮亮显'
    #仅输入用户名
    def test_onlyuser(self):
        youdan.open_homepage()
        youdan.login('123456','')
        assert youdan.checklogin_button() == 1,u'登录按钮亮显'
    #仅输入密码
    def test_onlypwd(self):
        youdan.open_homepage()
        youdan.login('','123456111')
        assert youdan.checklogin_button() == 1,u'登录按钮亮显'
    #密码不足6位
    def test_pwd_not_six(self):
        youdan.open_homepage()
        youdan.login('15914145610','12345')
        assert youdan.checklogin_button() == 1,u'登录按钮亮显'
    '''
    #号码未注册
    def test_no_regist(self):
        youdan.open_homepage()
        youdan.login('1810000119711111','123456')
        assert youdan.checklogin_button() == 2
        assert youdan.checklogin() == 1
    #密码错误
    def test_pwd_wrong(self):
        youdan.open_homepage()
        youdan.login('18507097209','456789')
        assert youdan.checklogin_button() == 2
        assert youdan.checklogin() == 2






if __name__ == '__main__':
    #pytest.main("-q test_youdanweb.py --html=./report.html")
    pytest.main("-q test_youdanweb.py")
    #pytest.main(["--html=./report.html"])
