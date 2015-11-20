import re
import json
def sServerData(serverData):
    "Search the server time & nonce from server data"
    #servData = 'sinaSSOController.preloginCallBack({"retcode":0,"servertime":1447997169,"pcid":"xd-8b927d64100e5ae13a5bc5a12902d7144824","nonce":"4GHP5K","pubkey":"EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443","rsakv":"1330428213","exectime":9})'
    p = re.compile('({[^{]+?})')
    jsonData = p.search(serverData).group(1)
    #jsonData = re.search(r'({[^{]+?})', servData).group(1)
    #print jsonData
    data = json.loads(jsonData)
    
    serverTime = str(data['servertime'])
    nonce = data['nonce']
    pubkey = data['pubkey']
    rsakv = data['rsakv']
    print "Server time is:", serverTime
    print "Nonce is:", nonce
    return serverTime, nonce, pubkey, rsakv
def sRedirectData(text):
    p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
    loginUrl = p.search(text).group(1)
    print 'loginUrl:',loginUrl
    return loginUrl
#serverTime, nonce, pubkey, rsakv = sServerData()
#print serverTime,nonce,pubkey,rsakv

