import re
import uuid
from datetime import datetime, time, timedelta


class Calendar:
    """ics文件格式:
    https://cloud.tencent.com/developer/article/1655829
    https://datatracker.ietf.org/doc/html/rfc5545"""
    HEADER = """BEGIN:VCALENDAR
        PRODID:https://github.com/barryZZJ/ucas_course_to_calendar
        VERSION:2.0
        CALSCALE:GREGORIAN
        METHOD:PUBLISH
        CLASS:PUBLIC
        BEGIN:VTIMEZONE
        TZID:Asia/Shanghai
        TZURL:http://tzurl.org/zoneinfo-outlook/Asia/Shanghai
        X-LIC-LOCATION:Asia/Shanghai
        BEGIN:STANDARD
        TZOFFSETFROM:+0800
        TZOFFSETTO:+0800
        TZNAME:CST
        DTSTART:19700101T000000
        END:STANDARD
        END:VTIMEZONE""".replace(" ", "")  # 日历头，replace 用来去掉对齐用的缩进
    TAIL = "END:VCALENDAR"
    TIMETABLE_ST = [
        '_',
        time(8, 30), time(9, 20), time(10, 30), time(11, 20),
        time(13, 30), time(14, 20), time(15, 30), time(16, 20),
        time(18, 10), time(19, 0), time(20, 10), time(21, 0),
    ]
    TIMETABLE_ED = [
        '_',
        time(9, 20), time(10, 10), time(11, 20), time(12, 10),
        time(14, 20), time(15, 10), time(16, 20), time(17, 10),
        time(19, 0), time(19, 50), time(21, 0), time(21, 50)
    ]
    char2int = { "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "日": 7, "天": 7 }
    def __init__(self, first_day_of_term):
        self._events = []
        self.first_day = first_day_of_term
        self.events = []
        self.pat = re.compile("星期(\S)： 第((?:\d+、?)+)节。")

    def appendCourse(self, id, name, time, place, week, teacher):
        """示例
        time: 星期二： 第1、2节。
        place: 教一楼404
        week: 2、3、4、5、6、8、9、10、11、12
        """
        weekday, numbers = self.pat.match(time).groups()  # weekday: 一, numbers: 1、2
        day = self.char2int[weekday]  # 星期几，int型
        numbers = [*map(int, numbers.split('、'))]  # 节次，int列表
        startTime = self.TIMETABLE_ST[numbers[0]]  # 起始时间 (xx:xx)
        endTime = self.TIMETABLE_ED[numbers[-1]]  # 结束时间 (xx:xx)
        weeks = [*map(int, week.split('、'))]  # 上课周次，int列表
        for w in weeks:
            st_delt = timedelta(weeks=w-1, days=day-1, hours=startTime.hour, minutes=startTime.minute)
            ed_delt = timedelta(weeks=w-1, days=day-1, hours=endTime.hour, minutes=endTime.minute)
            start = self.first_day + st_delt  # 起始日期时间 datetime对象
            end = self.first_day + ed_delt  # 结束日期时间 datetime对象
            self._events.append(self._toEvent(id, name, start, end, place, teacher))

    def _toEvent(self, id, name, start: datetime, end: datetime, location, teacher):
        """
        事件格式：https://datatracker.ietf.org/doc/html/rfc5545#section-3.6.1

        example:
            BEGIN:VEVENT
            DTSTAMP:20210830T121455Z  # 创建时间
            DTSTART;TZID=Asia/Shanghai:20211110T142500 # 开始时间
            DTEND;TZID=Asia/Shanghai:20211110T180500  # 结束时间
            SUMMARY:课程名
            LOCATION:教室
            DESCRIPTION:课程编码：xxx\n主讲教师:xxx
            TRANSP:OPAQUE
            ORGANIZER:UCAS
            UID:3ad5a81a-0f59-469c-bb37-e07fed6f9d9e
            END:VEVENT
        """

        time_format = "{date.year}{date.month:0>2d}{date.day:0>2d}T{date.hour:0>2d}{date.minute:0>2d}{date.second:0>2d}"
        res = []
        res += ['BEGIN:VEVENT']
        res += ['DTSTAMP:' + datetime.today().strftime("%Y%m%dT%H%M%SZ")]
        res += ['DTSTART;TZID=Asia/Shanghai:' + time_format.format(date=start)]
        res += ['DTEND;TZID=Asia/Shanghai:' + time_format.format(date=end)]
        res += ['SUMMARY:' + name]
        res += ['LOCATION:' + location]
        res += ['DESCRIPTION:' + '课程编码: ' + id + r'\n' + '主讲教师: ' + teacher]
        res += ['TRANSP:OPAQUE']
        res += ['ORGANIZER:UCAS']
        res += ['UID:' + str(uuid.uuid4())]
        res += ['END:VEVENT']
        return '\n'.join(res)

    def to_ics(self, filename):
        eventsStr = '\n'.join(self._events)
        icsStr = '\n'.join([self.HEADER, eventsStr, self.TAIL])
        with open(filename, "w", encoding="utf8") as f:
            f.write(icsStr)