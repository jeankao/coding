# -*- coding: UTF-8 -*-
from account.models import Log
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import datetime
from django.utils import timezone
from itertools import groupby
import re

class VideoLogHelper:

    def _calculate(self, events):
        start_time = ''
        videos = []
        for event in events:
            # 查看課程內容<1> | 影片：為什麼要學程式設計 | PAUSE[00:07:56]
            action, time = re.search(
                "(PLAY|PAUSE|STOP)\[(.+)\]", event.event).groups()
            if action == 'PLAY':
                start_log_time = event.publish
                start_time = time
                searching = True
            if searching and (action in ['PAUSE', 'STOP']):
                    tmp = start_time.split(":")
                    tfrom = int(tmp[0]) * 3600 + int(tmp[1]) * 60 + int(tmp[2])
                    length = int(
                        (event.publish - start_log_time).total_seconds())
                    tto = tfrom + length
                    videos.append({'stamp': str(localtime(start_log_time).strftime(
                        "%Y-%m-%d %H:%M:%S")), 'from': tfrom, 'to': tto, 'length': length, 'duration': 300})
                    searching = False
        return videos

    def _collectTime(self, events):
        videos = list(map(lambda e: {'uid': e.user_id, 'start': int(e.event[-9:-7]) * 3600 + int(e.event[-6:-4]) * 60 + int(e.event[-3:-1]) }, events))
        return videos

    def getLogByUserid(self, user_id, youtube_id):
        event_list = ['PLAY', 'PAUSE', 'STOP']
        events = Log.objects.filter(user_id=user_id, youtube_id=youtube_id).order_by("id")
        return self._calculate(events)

    def getPlayLogByUserids(self, ids, lesson, tabName):
        events = Log.objects.filter(
                event__contains=u"查看課程內容<"+lesson+"> | "+tabName+" | PLAY",
                user_id__in=ids
            ).order_by('user_id', 'id')
        return self._collectTime(events)

    def getLogByUserid_Lesson_Tab(self, userid, lesson, tab):
        events = self.getLogByUserid(userid)
        try:
            return events[lesson, tab]
        except:
            return []