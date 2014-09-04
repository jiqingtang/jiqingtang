#!/usr/bin/env python


try:
  import json
except ImportError:
  import simplejson as json
import urllib
import urllib2


def translate(q, langpair='|zh'):
  url = 'http://ajax.googleapis.com/ajax/services/language/translate'
  lines = q.split('\n')
  q = '<br>'.join(lines)
  request = urllib2.Request(url, None,
                            {'Referer': 'http://www.from-command-line.com'})
  response = urllib2.urlopen(request,
                             urllib.urlencode(dict(v='1.0',
                                                   q=q.encode('utf-8'),
                                                   langpair=langpair)))
  encode = response.headers['content-type'].split('charset=')[-1]
  json_obj = json.load(response, encode)
  if json_obj['responseStatus'] != 200:
    return 'Error %d: %s' % (json_obj['responseStatus'],
                             json_obj['responseDetails'])
  translated_lines = json_obj['responseData']['translatedText'].split('<br>')
  for i, line in enumerate(lines):
    leading_spaces = len(line) - len(line.lstrip())
    translated_lines[i] = ' ' * leading_spaces + translated_lines[i].strip()
  return '\n'.join(translated_lines)
