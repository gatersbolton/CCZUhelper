import base64
import datetime
import re
import time
import requests
import argparse
# usernames = ['20416323', '20440213', '20440216']
# passwords = ['Xf552200.', 'Chenxt1668zz', 'Pyw12345']

class libspider:
    session=requests.Session()
    seat_hash = [0, 12551,12552,12553,12554,12555,12556,13363,13364,12560,12561,12562,12563,12564,12565,13365,13366,12569,12570,12571,16751,12573,12574,13367,13368,13369,13370,12584,12623,12659,12695,12624,12660,12696,12627,12663,12699,13355,13356,13357,13358,13359,13360,12632,12668,12704,12635,12671,12707,12636,12672,12708,12639,16760,12711,12640,12676,16757,12643,12679,12715,12644,12680,12716,16756,12683,12719,12648,12684,12720,12615,12651,12687,12723,12759,12795,12616,12652,12688,12724,12760,12796,12848,12884,12849,12885,12852,12888,12853,12889,12856,12892,12857,12893,12860,12896,12861,12897,12990,13026,12991,13027,12994,13030,12995,13031,12998,13034,12999,13035,13002,13038,13003,13039,13006,13042,13007,13043,13393,13236,13394,13395,13396,13373,13397,13392,13398,13245,13399,13390,13400,13379,13401,13382,13402,13253,13403,13385,13404,13258,13405,13388,]
    usernames = ['20440225', '2100160322', '20440217']
    passwords = ['Amelia,520', '20030126Wxc', 'Scr1028scr']
    weekday_str = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def __init__(self,user=1,username='',password='',test=False):
        libspider.session=requests.Session()
        if user >= 0 :
            username=libspider.usernames[user]
            password=libspider.passwords[user]
        i1 = libspider.session.get(
            url='https://zmvpn.cczu.edu.cn/http/webvpn4578b329feda6a5f6cc5a9222350e3b0/sso/login',
            headers={
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
            },
        )
        if test:
            print(i1.text)
        i1txt = i1.text

        reg = re.compile(r'name="lt" value=".*"')
        match = reg.search(i1txt)
        start = match.start();
        end = match.end();
        lt = i1txt[start + 17:end]
        lt = lt.strip('>');
        lt = lt.strip('/');
        lt = lt.strip('"');
        reg = re.compile(r'name="execution" value=".*"')
        match = reg.search(i1txt)
        execution = match[0][24:-1]
        # 获取jlibspider.sessionid
        ijsid = libspider.session.post(url='https://webvpn.cczu.edu.cn/webvpn/getcookie?domain=sso.cczu.edu.cn')
        jsidtxt = ijsid.text
        reg = re.compile(r'"Jlibspider.sessionID":"[a-zA-Z0-9]*"')
        match = reg.findall(jsidtxt)
        # jlibspider.sessionid = match[0][14:-1]
        b64password = base64.b64encode(password.encode()).decode()
        i2 = libspider.session.post(
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
        if test:
            print(i2.text)

        i3 = libspider.session.post(
            url="https://zmvpn.cczu.edu.cn/http/webvpn4578b329feda6a5f6cc5a9222350e3b0/sso/login?service=https://zmvpn.cczu.edu.cn/http/webvpnd56e8ad031c0cd86860fe6de4f1464605e734b8b4eef67fef791aba5330c6934/cas",
            headers={
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
            },
        )
        if test:
            print(i3.text)
        i4 = libspider.session.get(
            url="https://zmvpn.cczu.edu.cn/http/webvpnd56e8ad031c0cd86860fe6de4f1464605e734b8b4eef67fef791aba5330c6934/cas?ticket=" + lt,
            headers={
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
            },
        )
        if test:
            print(i4.text)
        i4txt = i4.text
        reg = re.compile(r'name="SYNCHRONIZER_TOKEN" value=".*?"')
        match = reg.search(i4txt)
        libspider.st = match[0][33:-1]
        # print(match[0])
        # print(st)

    def book(self,date='today',starttime=18.5,duration=4.0,seat=1,test=False):
        log='预约成功！'
        endtime=starttime+duration
        #判断周六
        today = datetime.date.today()
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        if date == 'today': whichday = today
        if date == 'tomorrow': whichday = tomorrow
        weekday = whichday.today().weekday()
        if libspider.weekday_str[weekday] == 'Saturday' and endtime == 17.0:
            endtime = 16.5
            if not test:
                print(">>>>由于今天周六，下午四点半需要打扫，请注意哦！<<<<")

        i5 = libspider.session.post(
            url="https://zmvpn.cczu.edu.cn/http/webvpnd56e8ad031c0cd86860fe6de4f1464605e734b8b4eef67fef791aba5330c6934/selfRes",
            data={
                'SYNCHRONIZER_TOKEN': libspider.st,
                'SYNCHRONIZER_URI': '/',
                'date': str(whichday),
                'seat': libspider.seat_hash[seat],
                'start': str(int(starttime * 60)),
                'end': str(int(endtime * 60)),
                'authid': '-1'
            }
        )
        # print(i5.text)
        if test:
            print(i5.text)


        match = re.search(r"预约失败，请尽快选择其他时段或座位", i5.text)
        while match:
            seat=seat+1
            i4 = libspider.session.get(
                url="https://zmvpn.cczu.edu.cn/http/webvpnd56e8ad031c0cd86860fe6de4f1464605e734b8b4eef67fef791aba5330c6934/cas?ticket=" + libspider.st,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
                },
            )
            # print(i4.text)
            if test:
                print(i4.text)

            i4txt = i4.text
            reg = re.compile(r'name="SYNCHRONIZER_TOKEN" value=".*?"')
            match = reg.search(i4txt)
            st = match[0][33:-1]
            # print(seat)
            i5 = libspider.session.post(
                url="https://zmvpn.cczu.edu.cn/http/webvpnd56e8ad031c0cd86860fe6de4f1464605e734b8b4eef67fef791aba5330c6934/selfRes",
                data={
                    'SYNCHRONIZER_TOKEN': st,
                    'SYNCHRONIZER_URI': '/',
                    'date': str(whichday),
                    'seat': libspider.seat_hash[seat],
                    'start': str(int(starttime * 60)),
                    'end': str(int(endtime * 60)),
                    'authid': '-1'
                }
            )
            if test:
                print(i5.text)
            match = re.search(r"预约失败，请尽快选择其他时段或座位", i5.text)
            if match is None:
                if not test:
                    log=log+'座位已被预约，自动修改为  ' + str(seat) + '  号位置。\n'
                break
        return log
    def ChangeSeat(self,user):
        log, date, starttime, duration, seat, cancelable = self.Cancel(True)
        newspider=libspider(user)
        newspider.book(date,starttime,duration,seat)
    def Cancel(self,realcancel=True,test=False):
        log=""
        i6 = libspider.session.get(
            url="https://zmvpn.cczu.edu.cn/http/webvpnd56e8ad031c0cd86860fe6de4f1464605e734b8b4eef67fef791aba5330c6934/history?type=SEAT",
            headers={
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
            },
        )
        if test:
            print(i6.text)

        pattern = r'/reservation/cancel/(\d+)'
        result = re.findall(pattern, i6.text)
        pattern2 = r'style="font-weight: bold">(.*?)</dt>'
        result2 = re.findall(pattern2, i6.text)
        pattern3 = r'区三楼阅读空间(\d+)'
        result3 = re.findall(pattern3, i6.text)
        # result = str(result)
        if test:
            if result:print(result[0])
            if result2:print(result2[0])
            if result3:print(result3[0])
        if not result:
            log=log+"没有预约，无法取消！\n"
        date="today"
        if "明" in result2[0]: date="tomorrow"
        match = re.search(r"(\d+):(\d+)", result2[0])
        if match:
            start_hour = int(match.group(1))
            start_min = int(match.group(2))
            start_time = start_hour + start_min / 60.0
        match = re.search(r"-- (\d+):(\d+)", result2[0])
        if match:
            end_hour = int(match.group(1))
            end_min = int(match.group(2))
            duration = (end_hour + end_min / 60.0) - start_time
        seat=int(result3[0])
        if result and realcancel:
            url='https://zmvpn.cczu.edu.cn/http/webvpnd56e8ad031c0cd86860fe6de4f1464605e734b8b4eef67fef791aba5330c6934/reservation/cancel/'+str(result[0])
            if test:
                print(url)
            # "https://zmvpn.cczu.edu.cn/http/webvpnd56e8ad031c0cd86860fe6de4f1464605e734b8b4eef67fef791aba5330c6934/reservation/cancel/1665014"
            i7 = libspider.session.get(
                url=url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36',
                },
            )
            if test:
                print(i7.text)
        cancelable=True
        if (result and realcancel) or (not result): cancelable=False
        if cancelable: log="取消成功！"
        return log, date, start_time, duration,seat,cancelable

# library.py -t 18.5 -d 0 -s 2 -a 0

if __name__ == "__main__":
    s=libspider(user=0)
    # log=s.book(date='tomorrow',starttime=18.5,duration=4.0,seat=66,test=False)
    s.ChangeSeat(user=1)
    # print(log,date,starttime,duration,seat)


    # parser = argparse.ArgumentParser(description='图书馆预约程序')
    # parser.add_argument('-t', '--time', help='预约开始时间，接受小数，24小时制', required=False)
    # parser.add_argument('-e', '--endtime', help='预约结束时间，接受小数，24小时制', required=False)
    # parser.add_argument('-d', '--date', help='日期，0今天，1明天', required=False)
    # parser.add_argument('-s', '--seat', help='座位号，只支持3楼', required=False)
    # parser.add_argument('-a', '--account', help='使用系统中的哪个帐号，123表示', required=False)
    # parser.add_argument('-c', '--cancel', help='取消预约', required=False)
    # parser.add_argument('-u', '--use', help='转移到大号使用', required=False)
    # args = vars(parser.parse_args())
    # arg_t = args['time']
    # arg_d = args['date']
    # arg_s = args['seat']
    # arg_a = args['account']
    # arg_c = args['cancel']
    # date = 'today';
    # i = int(arg_a)
    # if arg_c is None:
    #     if arg_d=='1': date='tomorrow'
    #     libspider(mode='book',date=date,starttime=float(arg_t),endtime=float(arg_t)+4,username=usernames[i],password=passwords[i],index=i,seat=seat_index.index(int(arg_s)))
    # else:
    #     libspider("cancel", username=usernames[i], password=passwords[i], index=i)


