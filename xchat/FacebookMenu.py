#!/usr/bin/env python


import datetime
if hasattr(datetime.datetime, 'strptime'):
  strptime = datetime.datetime.strptime
else:
  import time
  strptime = lambda s, f: datetime.datetime(*(time.strptime(s, f)[:6]))
import HTMLParser
try:
  import json
except ImportError:
  import simplejson as json
import re
import urllib
import urllib2


def getMealType(when=None):
  when = when or datetime.datetime.today()
  if 7 <= when.hour < 10:
    return 'Breakfast'
  elif 11 <= when.hour < 14:
    return 'Lunch'
  elif when.isoweekday() == 5 and 16 <= when.hour < 19:
    return 'Happy Hour'
  elif when.isoweekday() != 5 and 17 <= when.hour < 20:
    return 'Dinner'
  return None


class WeekMenu(object):

  def __init__(self):
    self.cafe = None
    self.date = None
    self.menu = []

  def get(self, when=None):
    when = when or datetime.datetime.today()
    start = strptime(self.date, '%B %d, %Y')
    days = (when - start).days
    if 0 <= days < len(self.menu):
      prefix = getMealType(when)
      if prefix:
        result = [' %s: %s' % (meal_type, meal)
                  for meal_type, meal in self.menu[days][1]
                  if meal_type.lower().startswith(prefix.lower()) or
                     (meal_type.lower().startswith('soup') and
                      prefix in ('Lunch', 'Dinner'))]
        if result:
          result[0:0] = ['%s %s' % (self.cafe, self.menu[days][0])]
        return result
    return None


class MenuHtmlParser(HTMLParser.HTMLParser):

  CAFE_DATE_RE = re.compile(
      '^(Cafe [^:]+): Menu for the week of: (\w+ \d+, \d{4})$',
      re.I)

  def __init__(self, *args, **dargs):
    self.tag_stack = []
    self.tr_data = None
    self.seen_tds = 0
    self.result = WeekMenu()
    HTMLParser.HTMLParser.__init__(self, *args, **dargs)

  def handle_starttag(self, tag, attrs):
    #print ' ' * len(self.tag_stack) + tag + ' %s' % len(self.tag_stack)
    self.tag_stack.append(tag)
    if tag == 'tr':
      self.tr_data = []
    elif tag == 'td':
      self.seen_tds += 1

  def handle_endtag(self, tag):
    while self.tag_stack:
      popped_tag = self.tag_stack.pop()
      if popped_tag == 'tr':
        if self.tr_data:
          self.result.menu[-1][1].append(
              (self.tr_data[0], ' '.join(self.tr_data[1:])))
        self.tr_data = None
      elif popped_tag == 'td':
        self.seen_tds -= 1
      if popped_tag == tag:
        break
    #print ' ' * len(self.tag_stack) + '/' + tag + ' %s' % len(self.tag_stack)

  def handle_data(self, data):
    if self.tag_stack:
      data = data.strip()
      if self.tag_stack[-1] == 'div':
        match = self.CAFE_DATE_RE.match(data)
        if match:
          self.result.cafe = match.group(1)
          self.result.date = match.group(2)
      elif self.tag_stack[-1] == 'h5':
        self.result.menu.append((data, []))
      elif self.tr_data is not None and self.seen_tds > 0 and data:
        self.tr_data.append(data)
    #print ' ' * len(self.tag_stack) + data[:10]


def getMenusForWeek():
  menus = []
  for cafe, app_id in (('Cafe X', 3078020178),
                       ('Cafe 6', 130162533670674)):
    response = urllib2.urlopen('http://www.facebook.com/ajax/profile/tab.php',
                               urllib.urlencode(dict(__a=1,
                                                     id=80518126820,
                                                     v='app_%d' % app_id)))
    encode = response.headers['content-type'].split('charset=')[-1]
    js = unicode(response.read(), encode)
    json_obj = json.loads(js[js.find('{'):])
    parser = MenuHtmlParser()
    parser.feed(json_obj['payload']['tab_content'])
    parser.close()
    menus.append((cafe, parser.result))
  return menus


def getMenus(when=None):
  when = when or datetime.datetime.today()
  week_menus = getMenusForWeek()
  menus = []
  for cafe, week_menu in week_menus:
    menu = week_menu.get(when)
    if menu:
      menus += menu
  return menus
