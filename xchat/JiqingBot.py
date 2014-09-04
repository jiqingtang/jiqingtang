__module_name__ = 'JiqingBot'
__module_version__ = '1.0'
__module_description__ = 'Jiqing\'s Bot'


import os
import sys
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
  sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import xchat
import datetime
import re
import FacebookMenu
import GoogleTranslate


OP_CHANNEL_2_NICK_RE = {
    '#jjyy': None,
    '#ods': re.compile(r'''^(?:peter|
                               hlouie|
                               cvakili|
                               ctice|
                               jmooser|
                               ostap|
                               jgabbard|
                               jiqingt|
                               vinodv|
                               ljin)
                            (?:[_\d].*)?$''', re.X)
}

SHOW_MENU_CHANNELS = ('#jjyy',)

SHOW_ZH_MENU_CHANNELS = ('#jjyy',)


def onJoin(word, word_eol, userdata_op_channel_2_nick_re):

  def shouldGrantOp(channel_2_nick_re, channel, nick):
    if not channel_2_nick_re:
      return True
    if channel not in channel_2_nick_re:
      return False
    nick_re = channel_2_nick_re[channel]
    if not nick_re or nick_re.match(nick):
      return True
    return False

  nick = word[0].split('!')[0][1:]
  channel = word[2][1:]
  if shouldGrantOp(userdata_op_channel_2_nick_re, channel, nick):
    context = xchat.find_context(channel=channel)
    if context:
      me = context.get_info('nick')
      for user in context.get_list('users'):
        if user.nick == me:
          if '@' in user.prefix:
            context.command('op %s' % nick)
          break


def sayOnChannels(channels, message):
  lines = None
  for channel in channels:
    context = xchat.find_context(channel=channel)
    if context:
      if lines is None:
        lines = [line.encode('utf-8') for line in message.split('\n')]
      for line in lines:
        context.command('say %s' % line)


def showMenus(show_menu_channels=(),
              show_zh_menu_channels=(),
              meal_types=(),
              when=None):

  if isinstance(show_menu_channels, basestring):
    show_menu_channels = (show_menu_channels,)
  if isinstance(show_zh_menu_channels, basestring):
    show_zh_menu_channels = (show_zh_menu_channels,)
  if isinstance(meal_types, basestring):
    meal_types = (meal_types,)
  meal_types = meal_types and [meal_type.title() for meal_type in meal_types]

  meal_type = FacebookMenu.getMealType(when)
  if meal_type and (not meal_types or
                    meal_type in meal_types):
    menus = FacebookMenu.getMenus(when)
    if menus:
      if ' ' not in meal_type:
        meal_type += ' time'
      message = '%s\n%s' % (meal_type, '\n'.join(menus))
      sayOnChannels(show_menu_channels, message)
      zh_message = GoogleTranslate.translate(message)
      sayOnChannels(show_zh_menu_channels, zh_message)


def onTimer(userdata):
  showMenus(*userdata)
  hookShowMenus(*userdata)
  return True


def secondsToTime(hour, minute=0, second=0):
  today = datetime.datetime.today()
  seconds = (((hour - today.hour) * 60 + minute - today.minute) * 60 +
             second - today.second)
  if seconds <= 0:
    seconds += 24 * 60 * 60
  return seconds


def hookShowMenus(*args):
  if hasattr(hookShowMenus, 'handler'):
    xchat.unhook(hookShowMenus.handler)
  next, meal_type = min((secondsToTime(hour, minute), meal_type)
                        for hour, minute, meal_type in ((8, 0, 'Breakfast'),
                                                        (11, 45, 'Lunch'),
                                                        (17, 0, 'Happy Hour'),
                                                        (17, 45, 'Dinner')))
  hookShowMenus.handler = xchat.hook_timer(
      next * 1000, onTimer, args[:2] + (meal_type,))


if __name__ == '__main__':
  xchat.hook_server('Join', onJoin, OP_CHANNEL_2_NICK_RE)
  hookShowMenus(SHOW_MENU_CHANNELS, SHOW_ZH_MENU_CHANNELS)
  print '\0034%s %s has been loaded\003' % (__module_name__, __module_version__)
