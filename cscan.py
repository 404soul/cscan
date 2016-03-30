#coding:gb2312
import os
import re
import Queue
import threading

q=Queue.Queue()

class getCSgement:
    #��ʼ��
    def __init__(self,url):
        if "http" in url:
            pattern = re.compile(r'(?<=//).+(?<!/)')
            match = pattern.search(url)
            try:
                url = match.group()
            except:
                print "����error"
            self.url = url
        else:
            self.url = url
        
    def cSgment(self):
        lookStr = self.nsLookUp(self.url)
        listIp = self.fetIp(lookStr)
        
        if len(listIp)==0:
            return "networkbad"      

        if self.checkCdn(listIp):
            strIp = ""
            for i in listIp:
                strIp = strIp + i + ","
            return strIp[:-1] + " (����ʹ����cdn)"
        
        return self.makeCSeg(listIp)
    
    
    #ʹ��nslookup������в�ѯ
    def nsLookUp(self,url): 
        cmd = 'nslookup %s 8.8.8.8' % url
        handle = os.popen(cmd , 'r')
        result = handle.read()
        return result
    
    #��ȡnslookup�����ѯ�Ľ�������ip
    def fetIp(self,result):
        ips =  re.findall(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])', result)
        if '8.8.8.8' in ips:
            ips.remove('8.8.8.8')
        return ips
        
    #����Ƿ�ʹ��cdn
    def checkCdn(self,ips):
        if len(ips)>1:
            return True
        return False
    
    #����c��
    def makeCSeg(self,ips):
        if not self.checkCdn(ips):
            ipStr = "".join(ips)
            end = ipStr.rfind(".") 
            return ipStr[0:end+1] + "1-" + ipStr[0:end+1] + "254"

#��ʼɨ��        
def scaner():
    while not q.empty():
        url=q.get()
        t = getCSgement(url)
        result = t.cSgment()
        
        if not "networkbad" in result:
            print url + ":" + result
            if not "cdn" in result:
                writeFile("result.txt", result + "\n")
        else:
            t = getCSgement(url)
            result2 = t.cSgment()
            if not "networkbad" in result2:
                print url + ":" + result2
                if not "cdn" in result2:
                    writeFile("result.txt", result2 + "\n")
            else:
                print url + ":���ܷ��� ���� ���粻�ȶ�"
                
    if q.empty():
        delRep()
                
#�����¼
def writeFile(filename,context):
    f= file(filename,"a+")
    f.write(context)
    f.close()

#ȥ�ظ�
def delRep():
    buff = []
    for ln in open('result.txt'):
        if ln in buff:
            continue
        buff.append(ln)
    with open('result2.txt', 'w') as handle:
        handle.writelines(buff)
        
        
#�ж��ļ��Ƿ񴴽�
def isExist():
    if not os.path.exists(r'result.txt'):
        f = open('result.txt', 'w')
        f.close()
    else:
        os.remove('result.txt')
        
    if os.path.exists(r'result2.txt'):
        os.remove('result2.txt')    

if __name__=="__main__":
    isExist()
    
    #��ȡ��ַ
    lines = open("domains.txt","r")
    for line in lines:
        line=line.rstrip()
        q.put(line)
        
    #�����߳�
    for i in range(3): 
        t = threading.Thread(target=scaner)
        t.start()
        
        
    


