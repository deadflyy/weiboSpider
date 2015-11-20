import urllib2
import cookielib
import WeiboEncode
import WeiboSearch
import WeiboLogin
if __name__ == '__main__':
    weiboLogin = WeiboLogin.WeiboLogin('deadflyy5280@dina.com', '882258')
    if weiboLogin.Login() == True:
        print "Login Successfully!"