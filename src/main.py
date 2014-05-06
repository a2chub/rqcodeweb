#!/usr/bin/env python
#coding:utf-8

import os
import time
import qrcode

from flask import Flask
from flask import request

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
  return "hello world"

@app.route('/input')
def input():
  src_html ='''
  <form action="/api/set" method="GET">
  <textarea name="src_text""></textarea>
  <input type="submit">
  </form>
  '''
  return src_html


@app.route('/api/set')
def api_set():
  _src = request.args.get('src_text')
  _saved_file = save_file( make_qr( _src ) )
  res_html = '''
  <p><a href='/input'>入力ページ</a></p>
  <img src="/static/qrimg/%s"><br/>
  '''%(_saved_file)

  return res_html

def make_qr(src_text):
  img = None
  if len(src_text) < 1024:
    img = qrcode.make( src_text )
  else:
    img = qrcode.make("too long keyword")
  return img


def save_file( tgt_file ):
  _base_path = os.path.dirname(os.path.abspath(__file__))
  _save_path = os.path.join('static', "qrimg")
  _file_name = str( int(time.time() * 1000) ) + ".png"
  _save_file_path_name = os.path.join( _save_path, _file_name)
  tgt_file.save( _save_file_path_name )
  return _file_name


if __name__ == '__main__':
  print os.path.dirname(os.path.abspath(__file__))
  app.run(host="0.0.0.0", port=9090)


