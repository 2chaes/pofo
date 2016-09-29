#!/usr/bin/python3
#-*- coding: utf-8 -*-
 
############Module import############
from __future__ import print_function
import json
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os
import datetime
import time
import subprocess
from selenium import webdriver

 
from urllib.parse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
############Module import############

'''
def DaumSpellCheck(msg):
	element = driver.find_element_by_id("tfSpelling")
	element.send_keys(msg)
	driver.find_element_by_id("btnCheck").click()
	soup = BeautifulSoup(driver.page_source,'html.parser')
	soup = soup.find(class_='cont_spell')
	err_texts = soup.find_all('a')
	ans = ""
	for i in err_texts:
		if i['data-error-type'] == "doubt":
			ans +="[" + i['data-error-input'] + " → 맞춤법 오류 의심]" + "\\n"
		else:
			ans +="[" + i['data-error-input'] + " → " + i['data-error-output'] + "]" + "\\n"
	
	# ans 수정 장소
	if ans.strip() == "":
		ans = "틀린 맞춤법을 찾지 못했습니다."
	else:
		ans = ans[:-2]
		ans = ans.replace('''"''','''\\"''')

	# ans.replace('\n','\\n')

	return ans
'''

def SpellCheck(msg):
	# 처리부분
	in_element.send_keys(msg)
	check_btn.click()

	## 갱신부분
	soup = BeautifulSoup(driver.page_source,'html.parser')
	soup = soup.find(class_='csu_rs').span

	# xlist는 틀린 단어들의 모음 # try 필요할듯
	xlist = soup.find_all('span')

	ans = ""
	for x in xlist:
		err_text = ""
		if x['class'][0] == 're_red':
			err_text = "맞춤법"
		elif x['class'][0] == 're_green':
			err_text = "띄어쓰기"
		elif x['class'][0] == 're_purple':
			err_text = "표준어 의심"
		else: # 틀린 부분 없음
			err_text = "correct"
			break

		ans +="[{0} : \"{1}\"]".format(err_text, x.text.strip()) + "\\n"

	# ans 수정 장소
	if err_text == "correct":
		ans = "교정할 내용이 없습니다."
	else:
		ans = ans[:-2]
		ans = ans.replace('''"''','''\\"''')

	# ans.replace('\n','\\n')

	return ans


def lyric_parse(lyric):
	lyrics=urllib.parse.quote(lyric)
	chtml=subprocess.check_output('curl -s \'http://www.melon.com/search/lyric/index.htm?q=' + lyrics + '\'', shell=True)
	soup = BeautifulSoup(chtml, 'html.parser')
	soup = soup.find(class_='list_lyric').li

	lylink = 'http://www.melon.com/song/detail.htm?songId='+soup.dt.a['data-song-no']
	title = soup.dt.a.text.strip()
	artist = soup.find(class_='atist').text.strip()

	#print(lylink,title,artist)

	return (artist + " - " + title,lylink)

app = Flask(__name__)

# 메시지는 최대 300자까지 받을수있음 
@app.route("/message", methods=['GET', 'POST'])
def message():
	# json must be str, not 'bytes' -> decode utf-8
	userMessage = json.loads(request.get_data().decode('utf-8'))
	userText=userMessage['content'].split()
	responseText = userMessage['content'] # 여기다가 기본 메시지
	if userText[0] == '가사':
		# " ".join(list) 이용해서 또는 그냥 가사를 저 함수에 넘기면 됨
		try:
			song_info = lyric_parse(" ".join(userText[1:]))

			return '''{ "message": { "text" : "''' + song_info[0] + '''" , "message_button" : { "label" : "곡정보 확인", "url": "'''+ song_info[1] + '''" }}}'''
		except Exception as e:
			return '''{ "message" : { "text" : "해당하는 가사가 없습니다."} }'''
	else:
		if len(userMessage['content']) >= 300:
			responseText = "300자 이상의 교정은 이곳에서!"
			return '''{ "message": { "text" : "''' + responseText + '''" , "message_button" : { "label" : "Naver 맞춤법 검사기", "url": "https://m.search.naver.com/search.naver?query=%EB%A7%9E%EC%B6%A4%EB%B2%95+%EA%B2%80%EC%82%AC%EA%B8%B0" }}}'''
		else:
			#driver.get("http://dic.daum.net/grammar_checker.do")
			in_element.clear()
			responseText = SpellCheck(userMessage['content'])

		return '''{ "message" : { "text" : "'''+responseText+'''" } }'''

	#print(userRequest['content'])
	#return '''{ "message" : { "text" : "good" } }'''
	#return '''{ "message": { "photo": { "url": "http://2chaes.xyz/bot/nal.jpg", "width": 640, "height": 480 }, "message_button" : { "label" : "반갑습니다", "url": "http://2chaes.xyz/bot/nal.jpg" }}}'''


@app.route("/keyboard", methods=['GET', 'POST'])
def keyboard():
	return """{ "type" : "text" }"""

if __name__ == "__main__":
	driver = webdriver.Firefox()
	url="https://m.search.naver.com/search.naver?query=%EB%A7%9E%EC%B6%A4%EB%B2%95+%EA%B2%80%EC%82%AC%EA%B8%B0"
	driver.get(url)
	driver.find_element_by_xpath("//*[@class='btn active']").click()
	in_element = driver.find_element_by_xpath("//*[@class='csu_ti']")
	in_element = in_element.find_element_by_tag_name("textarea")
	in_element.send_keys("맞춤법")
	check_btn=driver.find_element_by_class_name("chg_area")
	check_btn.click()
	in_element.clear()
	app.run(host="0.0.0.0", port=15000, threaded=True)
