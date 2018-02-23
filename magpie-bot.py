from __future__ import unicode_literals
import urllib2
from bs4 import BeautifulSoup
from lxml import html
import requests
import os
import sys
import scrape
from argparse import ArgumentParser
from flask import Flask, request, abort
from linebot import (
	LineBotApi, WebhookParser
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, VideoSendMessage
)
from googletrans import Translator


translator = Translator()
app = Flask(__name__)

channel_secret = "839a8b09678bdd07e57cffcd1330ffce"
channel_access_token = "buEqUNcckJXdu1EuTp2I+YJJeBR2WiEeFYDJHCtENPag2glrCdchIllLI2Vnb2yekKDLRUEujPlsSZyt6JgraWGEOLMqSkfhv7F14J+tzoa5y0hSLhvVwpyX6R2xn0VeY8WIMSSm3hZX/9DfS1kb+QdB04t89/1O/w1cDnyilFU="
if channel_secret is None:
	print('Specify LINE_CHANNEL_SECRET as environment variable.')
	sys.exit(1)
if channel_access_token is None:
	print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
	sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
	signature = request.headers['X-Line-Signature']
	# get request body as text
	body = request.get_data(as_text=True)
	print body
	app.logger.info("Request body: " + body)

	# parse webhook body
	try:
		events = parser.parse(body, signature)
	except InvalidSignatureError:
		abort(400)

	# if event is MessageEvent and message is TextMessage, then echo text
	for event in events:
		if not isinstance(event, MessageEvent):
			continue
		if not isinstance(event.message, TextMessage):
			continue

		text = event.message.text.lower().split(' ')
		if text[0]=="!tiketka":
			try:
				reply_text =""
				if text[1]=="info":
					reply_text = "List code :\nid = Indonesia\nko = Korea\nja = Japan\nzh-CN = Mandarin"
				else:
					origin_st = text[1]
					dest_st = text[2]
					departure_time = text[3]
					dept = departure_time.split('-')
					URL ="https://www.tiket.com/kereta-api/cari?d="+origin_st+"&a="+dest_st+"&date="+departure_time+"&adult=1&infant=0"
					schedules = scrape.online_schedule(URL)
					reply_text += "Jadwal Kereta dari "+origin_st.upper()+" ke "+dest_st.upper() + " pada tanggal " + dept[2] + "-" + dept[1] + "-" + dept[0] + "\n\n"
					idx = 0
					for schedule in schedules:
						idx += 1
						reply_text += str(idx)+". "
						keyorder = ['name', 'dept_time', 'arr_time', 'price', 'class']
						schedule = sorted(schedule.items(), key=lambda i:keyorder.index(i[0]))
						reply_text += ' - '.join(str(x[1]) for x in schedule)
						reply_text += "\n"
			except:
				reply_text = "Command : !translate <origin> <destination> <YYYY-MM-DD> Ex: !translate GMR BD 2018-02-26"
			command = TextSendMessage(reply_text)
		else:
			return 'OK'
		line_bot_api.reply_message(
			event.reply_token,
			command
		)

	return 'OK'


if __name__ == "__main__":
	arg_parser = ArgumentParser(
		usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
	)
	arg_parser.add_argument('-p', '--port', default=8000, help='port')
	arg_parser.add_argument('-d', '--debug', default=False, help='debug')
	options = arg_parser.parse_args()

	app.run(debug=options.debug, port=options.port, host='localhost')
