import cookielib
import urllib2
import re
import json
import WeiboEncode
import WeiboSearch
class WeiboLogin:
    
    def __init__(self, user, pwd, enableProxy = False):
        
        print "Initializing WeiboLogin..."
        self.userName = user
        self.passWord = pwd
        self.enableProxy = enableProxy

        self.serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)&_=1379834957683"
        self.loginUrl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
        self.postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}
        
    def Login(self):
         
        self.EnableCookie(self.enableProxy)
        
        serverTime, nonce, pubkey, rsakv = self.GetServerTime()
        postData = WeiboEncode.PostEncode(self.userName, self.passWord, serverTime, nonce, pubkey, rsakv)
        print "Post data length:\n", len(postData)
        req = urllib2.Request(self.loginUrl, postData, self.postHeader)
        print "Posting request..."
        result = urllib2.urlopen(req)
        text = result.read()
        try:
            loginUrl = WeiboSearch.sRedirectData(text)
            urllib2.urlopen(loginUrl)
        except:
            print 'Login error!'
            return False
        
        print 'Login sucess!'
        return True 
    def EnableCookie(self, enableProxy):
        "Enable cookie & proxy (if needed)."
    
        cookiejar = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
        if enableProxy:
            proxy_support = urllib2.ProxyHandler({'http':'http://xxxxx.pac'})
            opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)
            print "Proxy enabled"
        else:
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
    
    def GetServerTime(self):
        "Get server time and nonce, which are used to encode the password"
        
        print "Getting server time and nonce..."
        serverData = urllib2.urlopen(self.serverUrl).read()
        print serverData
        try:
            serverTime, nonce, pubkey, rsakv = WeiboSearch.sServerData(serverData)
            return serverTime, nonce, pubkey, rsakv
        except:
            print 'Get server time & nonce error!'
            return None 
    def sServerData(self,serverData):
        "Search the server time & nonce from server data"
        
        p = re.compile('({[^{]+?})')
        jsonData = p.search(serverData).group(1)
        #jsonData = re.search(r'({[^{]+?})', serverData).group(1)
        print jsonData
        data = json.loads(jsonData)
            
        serverTime = str(data['servertime'])
        nonce = data['nonce']
        pubkey = data['pubkey']
        rsakv = data['rsakv']
        print "Server time is:", serverTime
        print "Nonce is:", nonce
        return serverTime, nonce, pubkey, rsakv
    def sRedirectData(self,text):
        p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
        loginUrl = p.search(text).group(1)
        print 'loginUrl:',loginUrl
        return loginUrl
    