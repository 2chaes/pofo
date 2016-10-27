#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import time
import threading
import random
import re
import _thread

# 이미지 처리 영역. PIL
import io
from PIL import Image

# telepot에 필요한 영역. (설치)
# https://github.com/nickoala/telepot
import telepot
import pprint
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

# bs4 and urllib2 and lxml(설치)
from bs4 import BeautifulSoup
import urllib
import urllib.request

# selenium (selenium 설치)
from selenium import webdriver


# 리눅스에서 설치해야할 패키지 목록
# transmission-daemon
# curl



# thread 종료시점을 확인하기 위해 체크하는 변수
ttsnum=0

# 해당 텍스트를 음성으로 변환해주는 함수
def th_maketts(ttshtext, ttsstr, num):
    global ttsnum
    ttstext=urllib.parse.quote(ttsstr)
    if ttshtext == '/ttse':
        os.system('wget -O \'/tmp/tmptts'+str(num)+'.mp3\' \'http://responsivevoice.org/responsivevoice/getvoice.php?t=' + ttstext + '&tl=en-US\'')
    else:
        os.system('wget -O \'/tmp/tmptts'+str(num)+'.mp3\' \'http://responsivevoice.org/responsivevoice/getvoice.php?t=' + ttstext + '&tl=ko-KR\'')
    ttsnum+=1
    return



# 봇을 통해 이미지를 전송해주는 함수, 봇 api를 이용하여 전송하는 과정이 복잡해서
# 편하게 사용하기 위해서 정의함
def th_imgmsg(chat_id, templink, tempname, temptitle, i):
    try:
        try:
            bot.sendPhoto(chat_id, ('tempcal.gif', urllib.request.urlopen(templink[i])), caption="["+tempname[i]+"]\n"+temptitle[i])
        except:
            bot.sendPhoto(chat_id, ('tempcal.gif', urllib.request.urlopen("http:"+templink[i])), caption="["+tempname[i]+"]\n"+temptitle[i])
    except:
        try:
            bot.sendMessage(chat_id, "["+tempname[i]+"]\n" + temptitle[i])
        except:
            return

def div_sentence(words,lang):
    resstr=""
    while len(words) > 200:
        stat='\n'
        tempn=words[:200].find('\n')
        if tempn != -1 and words[tempn-1] in '.,?':
            stat = words[tempn-1]+'\n'

        if tempn == -1:
            tempn=words[:200].rfind('.')
            if words[tempn+1] == ' ':
                stat='. '
            else:
                stat='.'

        if tempn == -1:
            tempn=words[:200].rfind(',')
            if words[tempn+1] == ' ':
                stat='. '
            else:
                stat=', '

        if tempn == -1:
            tempn=words.find('.')
            stat='. '
            resstr+=words[:tempn+1].strip()
            words=words[tempn+1:]
        else:
            resstr+=Trans_lang(words[:tempn+1].strip(),lang)[:-1]+stat

            words=words[tempn+1:]

    resstr+=Trans_lang(words.strip(),lang)
    return resstr

# lang이 0이면 Kor2Eng, 1이면 Eng2Kor
def Trans_lang(msg, lang):
    global isE2K

    if len(msg.strip()) == 0:
        return ""

    # trans switch
    if isE2K != lang:
        isE2K=lang
        swit_btn.click()

    # input 전송
    in_element.send_keys(msg.strip())

    # 번역 버튼 검색, 클릭
    trans_btn.click()

    # 결과 기다렸다가 반환
    while not inout[1].text:
        pass
    trans_res = inout[1].text

    in_element.clear()
    return trans_res




#영타를 한글로 변환해주는 명령어에 필요한 함수

cho_index = []

cho_list = ["r","R","s","e","E","f","a","q","Q","t","T","d","w","W","c","z","x","v","g"]
cho_han_list=["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
jung_list = ["k","o","i","O","j","p","u","P","h","hk","ho","hl","y","n","nj","np","nl","b","m","ml","l"]
jung_han_list = ["ㅏ","ㅐ","ㅑ","ㅐ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"]
jong_list = ["", "r","R","rt","s","sw","sg","e","f","fr","fa","fq","ft","fx","fv","fg","a","q","qt","t","T","d","w","c","z","x","v","g"]
word_list = []

# 오타 출력
def OTAprint(i,endNum):
    global cho_index, cho_list, cho_han_list, jung_list, jung_han_list, word_list
    while (i != endNum):
        try:
            cho = cho_list.index(s[i])
            jung = 0
            jong = 0
            #print(cho_han_list[cho], end="")
            word_list.append(cho_han_list[cho])
            
        except:
            try:
                cho = 0
                jung = jung_list.index(s[i])
                jong = 0
                #print(jung_han_list[jung], end="")
                word_list.append(jung_han_list[jung])
                ##print(unichr(0xac00+((cho * 21) + jung) * 28 + jong), end="")
            except:
                if s[i] in [" ", "  "]:
                    #print(" ",end="")
                    word_list.append(" ")
                else:
                    #print(s[i],end="")
                    word_list.append(s[i])
                    
        i=i+1

# 영어를 한글로 변환해주는 함수이다.
def ETH(message):
    global s, cho_index, cho_list, cho_han_list, jung_list, jung_han_list, jong_list, word_list
    isJung = False
    isJJung = False
    s = message
    s = s + "rk"
    
    #print(len(cho_list),len(cho_han_list),len(jung_list),len(jung_han_list))
    

    #cho Index, jung_last_index
    for i , x in enumerate(s):
        # 모음이 두개짜리면 거른다.
        if isJJung == True:
            isJJung = False
            continue

        # 자음 뒤에 있는 모음인지 확인
        if i != 0:
            if s[i-1] in cho_list and s[i] in jung_list:
                isJung = True

        # 초성의 위치를 index 하고, 판별변수 초기화.
        if isJung:
            if s[i] != s[-1] and s[i]+s[i+1] in jung_list:
                cho_index.append([i-1, i+1])
                isJJung = True
            else :
                cho_index.append([i-1, i])
            isJung = False



    # 위에서 저장한 초성, 중성위치 리스트를 이용해서 한글의 종류를 판단한다.
    
    # 초성과 중성이 합쳐진 경우는 2 
    # 초성과 이중성이 합쳐진 경우는 3 
    # 초성과 중성과 종성이 합쳐진 경우는 4 
    # 초성과 이중성과 종성이 합쳐진 경우는 5
    # 끝에 공백인경우는 +10

    for i, x in enumerate(cho_index[:len(cho_index)-1]):
        num = 1 # 이게 나왔다면 오류일 확률이 높음.
        
        # 그냥 중성일 경우
        if x[1] - x[0] == 1:
            num = 2
        # 이중성일 경우 (ㅙ ㅚ)
        if x[1] - x[0] == 2:
            num = 3

        # 종성이 없는 경우. ("현재 중성의 위치"와 "다음 한글의 초성의 위치"를 비교해서 판별)
        if cho_index[i+1][0] - x[1] == 1: 
            pass
        # 종성이 있는 경우
        else: 
            # 종성이 맞는가? 아니면 공백인가?
            
            tempS = s[x[1]+1:cho_index[i+1][0]]
            #print("얍 : \""+tempS+"\"")

            # (앞대가리 두개가) 오른쪽 공백을 제외한 뒷 단어들이 null 이 아닌 종성인가?
            if tempS.rstrip() != "":
                if tempS[0] in jong_list: # 종성이 확인될때,
                    num = num + 2

                else: # 종성이 없을때
                    pass

            # 마지막 문자가 공백인가?
            if tempS[-1] in [" ", "  "]:
                num = num + 10
                #print("예스 공백요")


        cho_index[i].append(num)
        #print(num)

    #print(cho_index)


    # n는 현재 처리중인 단어의 위치를 가리킴
    n = 0

    # 0번째 부터 첫번째 한글의 초성까지 오타가 있다면 출력한다.
    OTAprint(n,cho_index[0][0])


    # cho_index에 저장한 정보를 이용해서 글자 만듬
    for i, x in enumerate(cho_index[:len(cho_index)-1]): # 젤 마지막에 rk 라는 단어를 넣어서 사용안함.
        cho = cho_list.index(s[x[0]])
        jong = 0
        n = x[0]
        
        if x[2] % 10 == 2: # 2, 12
            jung = jung_list.index(s[x[1]]) # 중성은 무조건 한개
            #print(unichr(0xac00+((cho * 21) + jung) * 28 + jong), end="")
            word_list.append(chr(0xac00+((cho * 21) + jung) * 28 + jong))
            n=n+2 # 사용한 초성 1개, 중성 1개
            ##print("\n숫자:",cho_index[i+1][0] - n) # 오타의 개수 확인
            # 공백이 있다면
            if x[2] == 12:
                #print(" ", end="")
                word_list.append(" ")
                n=n+1 # 공백 1개

        if x[2] % 10 == 3:
            jung = jung_list.index(s[x[1]-1:x[1]+1])
            #print(unichr(0xac00+((cho * 21) + jung) * 28 + jong), end="")
            word_list.append(chr(0xac00+((cho * 21) + jung) * 28 + jong))
            n=n+3 # 사용한 초성 1개, 중성 2개
            if x[2] == 13:
                #print(" ", end="")
                word_list.append(" ")
                n=n+1
        
        if x[2] % 10 == 4:
            jung = jung_list.index(s[x[1]])
            # 받침이 1개짜리면
            n = n+3
            try:
                # 받침이 1개임을 가정(n+3)했을때 처리하고 있는 위치가
                # 다음 단어의 초성의 위치라면
                # 오타가 나지 않은 이상 받침이 1개가 확실함.
                if n == cho_index[i+1][0]: 
                    raise Exception ("받침이 한개가 확실하니까 에러발생 시키고 넘어감")

                # 만약 받침이 2개짜리면 아래의 indexing은 성공하고,
                # indexing이 실패했다면 받침은 1개이고, '공백이거나, 오타가 났다'.
                jong = jong_list.index(s[x[1]+1:x[1]+3])
                n = n+1
            except Exception as e: # 여기로 왔으면 받침은 1개임.
                jong = jong_list.index(s[x[1]+1])
                # 받침이 2개짜리 검색 실패
                # print(e,"에러",s[x[1]+1:x[1]+3])
                
            #print(unichr(0xac00+((cho * 21) + jung) * 28 + jong), end="")
            word_list.append(chr(0xac00+((cho * 21) + jung) * 28 + jong))
            # 공백있으면 발생
            if x[2] == 14:
                #print(" ", end="")
                word_list.append(" ")
                n=n+1

        # 상동
        if x[2] % 10 == 5:
            jung = jung_list.index(s[x[1]-1:x[1]+1]) # 얘는 이중성
            n = n+4
            try:                
                if n == cho_index[i+1][0]:
                    raise Exception ("받침이 한개가 확실함.")

                jong = jong_list.index(s[x[1]+1:x[1]+3])
                n = n+1
            except Exception as e:
                jong = jong_list.index(s[x[1]+1])
                
            #print(unichr(0xac00+((cho * 21) + jung) * 28 + jong), end="")
            word_list.append(chr(0xac00+((cho * 21) + jung) * 28 + jong))

            if x[2] == 15:
                #print(" ", end="")
                word_list.append(" ")
                n=n+1

        OTAprint(n, cho_index[i+1][0])



# 날씨 예보 명령어에 사용되는 함수
# 지역이름을 받고 기상청에서 해당지역의 예보요약 주소를 반환.
def address_kma(addrlocal):
    if addrlocal == u'강원도':
        return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=105&x=28&y=16"
    elif addrlocal == u'서울' or addrlocal == u'인천' or addrlocal == u'경기도':
        return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=109&x=23&y=5"
    elif addrlocal == u'부산광역시' or addrlocal == u'울산광역시' or addrlocal == u'경상남도':
        return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=159&x=32&y=14"
    elif addrlocal == u'대구광역시' or addrlocal == u'경상북도':
        return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=143&x=15&y=16"
    elif addrlocal == u'광주광역시' or addrlocal == u'전라남도':
        return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=156&x=19&y=18"
    elif addrlocal == u'전라북도':
        return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=146&x=30&y=2"
    elif addrlocal == u'제주특별자치도':
        return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=184&x=27&y=10"
    elif addrlocal == u'대전광역시' or addrlocal == u'충청남도' or addrlocal == u'세종특별자치시':
        return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=133&x=31&y=16"
    elif addrlocal == u'충청북도':
        return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=131&x=36&y=9"
    else: # 전국
        return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=108&x=14&y=11"

        

message_with_inline_keyboard = None


# 메시지를 받아서 처리하는 함수
def on_chat_message(msg):
#    pprint.pprint(msg)
    content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True)
    
    # 메시지 시작이 /가 아니면 반환. API에 이 기능을 담당하는 부분이 있긴함.
    if msg['text'][0] != '/': return

    listtext = msg['text'].split() # msg['text']를 리스트로 저장.
    liststr  = " ".join(listtext[1:]) #list를 명령인자는 제외하고 string으로 변환.

# help 처리 영역 시작.    
    # 명령 판단 부분. /help, /cal, /tor, /torr, /tts, /미세먼지, /hash, /날씨
    if listtext[0] == '/help':
        if listtext[1:] == []:
            bot.sendMessage(chat_id, "***채승 하급봇 입니다.***\n1. <code>/cal expression|anything</code>\n2. <code>/hash md5|sha1|sha256|sha512 string</code>\n3. <code>/tor 검색어</code>\n4. <code>/torr 검색어</code> (whitelist_user만 사용 가능)\n5. <code>/날씨 위치 [-|0|1|2]</code>\n6.<code>/tts string(kor), /ttse string(eng)</code>\n7. <code>/미세먼지 [지역]</code>\n8. <code>/help [cal|hash|tor|torr|날씨]</code> 으로 명령어 확인이 가능합니다.\n", parse_mode='HTML', reply_to_message_id=msg_id)
        else: # /help 이후 명령어들
            if listtext[1] == 'cal':
                bot.sendMessage(chat_id, "cal 명령어는 울프람알파(http://m.wolframalpha.com)로 <code>수식이나 문자</code>를 넘겨서 결과를 가져옵니다.\n\n[SYNOPSIS]\n<code>/cal expression|anything</code>\n\n[EXAMPLE]\n<code>/cal 1+2+..+99+100</code>\n<code>/cal pikachu</code>\n<code>/cal H2O</code>", disable_web_page_preview=True, parse_mode='HTML', reply_to_message_id=msg_id)
            elif listtext[1] == 'hash':
                bot.sendMessage(chat_id, "hash 명령어는 해시함수를 이용하여 문자열의 해쉬값을 가져옵니다. *공백을 포함합니다*\n\n[SYNOPSIS]\n<code>/hash md5|sha1|sha256|sha512 string</code>\n\n[EXAMPLE]\n<code>/hash md5 2chaes</code>\n<code>/hash sha256 한글도 가능합니다. </code>\n<code>/hash sha512 apple banana coconut </code>", disable_web_page_preview=True, parse_mode='HTML', reply_to_message_id=msg_id)
            elif listtext[1] == 'tor':
                bot.sendMessage(chat_id, "tor 명령어는 토렌트사이트(https://torrentkim3.net/)에서 <code>검색어</code>로 검색 후 결과를 가져옵니다. 이후 원하는 파일의 <code>magnet</code>을 출력합니다.\n\n[SYNOPSIS]\n<code>/tor 검색어 </code>\n\n[EXAMPLE]\n<code>/tor 마이 리틀 텔레비전</code>\n<code>/tor 무한도전</code>\n<code>/tor 160522 1박 2일</code>\n<code>/tor 런닝맨</code>", disable_web_page_preview=True, parse_mode='HTML', reply_to_message_id=msg_id)
            elif listtext[1] == 'torr':
                bot.sendMessage(chat_id, "torr 명령어는 토렌트사이트(https://torrentkim3.net/)에서 <code>검색어</code>로 검색 후 서버에 다운로드 요청을 합니다. \n*whitelist에 등록된 사람만 이용 가능합니다.*\n\n[SYNOPSIS]\n<code>/tor 검색어</code>\n\n[EXAMPLE]\n<code>/tor 마이 리틀 텔레비전</code>\n<code>/tor 무한도전</code>\n<code>/tor 160522 1박 2일</code>\n<code>/tor 런닝맨</code>\n\nPS. 악용을 막기 위해 검색결과를 통해서만 다운 요청이 가능합니다. <code>야동 받지마라...</code>", disable_web_page_preview=True, parse_mode='HTML', reply_to_message_id=msg_id)
            elif listtext[1] == '날씨':
                bot.sendMessage(chat_id, "날씨 명령어는 기상청에서 제공하는 <code>(오늘,내일,모레)예보요약</code>과, 다음(http://www.daum.net/)으로 지역의 날씨를 검색하여 <code>날씨영역을 캡쳐</code>해서 제공합니다.\n*해외도 검색가능합니다. 예보요약 미제공*\n\n[SYNOPSIS]\n<code>/날씨 위치 [-|0|1|2]</code>\n\n[EXAMPLE]\n옵션인자에 따라서 예보요약 제공이 바뀝니다.\n오늘 예보요약 : <code>/날씨 진주</code>\n내일 예보요약 : <code>/날씨 창원 1 </code>\n전체 예보요약 : <code>/날씨 서울 0</code>\n예보요약 거절 : <code>/날씨 전국 -</code>\n", disable_web_page_preview=True, parse_mode='HTML', reply_to_message_id=msg_id)
            elif listtext[1] == '미세먼지':
                bot.sendMessage(chat_id, "미세먼지 명령어 다음(http://www.daum.net/)으로 지역의 미세먼지를 검색하여 <code>미세먼지 영역을 캡쳐</code>해서 제공합니다.\n\n[SYNOPSIS]\n<code>/미세먼지 [위치]</code>\n\n[EXAMPLE]\n<code>/미세먼지</code>\n<code>/날씨 창원 </code>\n<code>/날씨 서울</code>\n", disable_web_page_preview=True, parse_mode='HTML', reply_to_message_id=msg_id)
            elif listtext[1] == 'tts' or listtext[1] == 'ttse':
                bot.sendMessage(chat_id, "tts/ttse 명령어는 http://responsivevoice.org/ 에서 제공하는 <code>TTS(Text To Speech)</code>를 이용하여 문자열을 <code>음성메시지</code>로 변환해서 전송해줍니다.\n\n[SYNOPSIS]\n<code>/tts 문자열</code>\n<code>/ttse 문자열(eng)</code>\n\n[EXAMPLE]\n<code>/tts 안녕하세요?</code>\n<code>/ttse i'm a boy, you're a girl</code>", disable_web_page_preview=True, parse_mode='HTML', reply_to_message_id=msg_id)
            else:
                bot.sendMessage(chat_id, "***채승 하급봇 입니다.***\n1. <code>/cal expression|anything</code>\n2. <code>/hash md5|sha1|sha256|sha512 string</code>\n3. <code>/tor 검색어</code>\n4. <code>/torr 검색어</code> (whitelist_user만 사용 가능)\n5. <code>/날씨 위치 [-|0|1|2]</code>\n6.<code>/tts string(kor), /ttse string(eng)</code>\n7. <code>/미세먼지 [지역]</code>\n8. <code>/help [cal|hash|tor|torr|날씨]</code> 으로 명령어 확인이 가능합니다.\n", parse_mode='HTML', reply_to_message_id=msg_id)
# help 처리 영역 끝.


# /tor, /torr 처리 영역 시작.
    # tor와 torr 부분 / tor는 마그넷 검색해주고, torr(tor remote)는 검색한 프로그램을 트랜스미션으로 다운로드 받는다.
    elif listtext[0] == '/tor' or listtext[0] == '/torr':
        if msg['chat']['type'] != 'private': # 인라인 키보드는 개인채팅이 아닌곳에선 지원하지 않음.
            bot.sendMessage(chat_id, "그룹채팅에선 사용할 수 없습니다.", parse_mode='HTML', reply_to_message_id=msg_id)
            return

        if listtext[0] == '/tor':
            if len(listtext) < 2:
                bot.sendMessage(chat_id, "\"<code>/tor 검색어</code>\" 의 형태로 입력해주세요. 자세한 명령은 <code>/help tor</code>에서 확인가능합니다.", parse_mode='HTML', reply_to_message_id=msg_id)
                return
        else:
            if len(listtext) < 2:
                bot.sendMessage(chat_id, "\"<code>/torr 검색어</code>\" 의 형태로 입력해주세요. 자세한 명령은 <code>/help torr</code>에서 확인가능합니다.", parse_mode='HTML', reply_to_message_id=msg_id)
                return
        # if torr일때 사용 유저는 화이트 리스트에 있는가?
        if listtext[0] == '/torr' and msg['from']['username'] not in whitelist:
            bot.sendMessage(chat_id, "whitelist에 등록된 사람만 사용 가능합니다.", reply_to_message_id=msg_id)
            return
        
        # 검색중
        bot.sendMessage(chat_id, "<code>["+ liststr + "]</code> searching...", parse_mode='HTML', reply_to_message_id=msg_id)
        # subprocess를 이용해서 curl로 소스를 가져온다.
        # urllib을 이용하지 않고 굳이 이렇게 한 이유는 다양하게 연습해보고 싶어서이다.
        torhtml=subprocess.check_output('curl -s \'https://torrentkim3.net/bbs/rss.php?k=' + liststr + "\'", shell=True)

        # BeautifulSoup를 이용해서 원하는 부분을 가져온다.
        #soup = BeautifulSoup(torhtml, 'lxml')
        soup = BeautifulSoup(torhtml, 'html.parser')
        temptorname=soup.find_all('title')
        temptorlink=soup.find_all('guid')

        
        # 검색 성공시 검색결과 개수는 name은 n+1개 link는 name-1개, 실패시 0개.
        namesearch=len(temptorname)
        linksearch=len(temptorlink)

        if namesearch*linksearch == 0:
            bot.sendMessage(chat_id, "<code>[" + liststr + "]</code> Not Found.", parse_mode='HTML')
            return

        
        temptorlist=[] # InlineKeyboard 출력으로 활용될 배열이다. 형식에 맞게 append 작업을 한다.
        
        # callback_data type은 string형으로 보내야함.
        # /tor 이라면 마그넷만을 출력하기 위해 callback_data 앞에 magnet 을 붙여주고
        # /torr 이면 다운로드 명령을 하기 위해서 magdown을 붙여서 구분한다.
        if listtext[0] == '/tor':
            for i in range(linksearch):
                temptorlist.append([InlineKeyboardButton(text=temptorname[i+1].get_text(), callback_data="magnet " + temptorlink[i].get_text())])
        else:
            for i in range(linksearch):
                temptorlist.append([InlineKeyboardButton(text=temptorname[i+1].get_text(), callback_data="magdown " + temptorlink[i].get_text())])
        
        # 마지막은 닫기 버튼 callback_data는 close
        temptorlist.append([InlineKeyboardButton(text="닫기", callback_data="close")])
        
        # 인라인 키보드 함수에 위에서 저장한 리스트를 넣음.
        markup = InlineKeyboardMarkup(inline_keyboard=temptorlist)


        global message_with_inline_keyboard
        message_with_inline_keyboard = bot.sendMessage(chat_id, '총'+ str(linksearch) + '개의 검색결과가 존재 합니다.', reply_markup=markup)
# /tor, /torr 처리 영역 끝.



# /cal 처리 영역 시작.
    # selenium으로 처리하면 Full Page를 출력 할 수 있다.
    # urllib2 활용하기 샘플용. (빠르긴 빠름)
    # /cal은 모바일 울프람알파 페이지에서 검색하고 결과를 파싱해서 출력한다.
    elif listtext[0] == '/cal':
        # 인자가 없으면 반환
        if len(listtext) < 2:
            bot.sendMessage(chat_id, "\"<code>/cal expression|whatever</code>\" 의 형태로 입력해주세요. 자세한 명령은 <code>/help cal</code>에서 확인가능합니다.", parse_mode='HTML', reply_to_message_id=msg_id)
            return

            
        bot.sendMessage(chat_id, "searching...", reply_to_message_id=msg_id)

        # 파싱 및 분류
        searchlist = urllib.parse.quote(liststr)
        try:
            browser.get('http://m.wolframalpha.com/input/?i='+searchlist)
        except:
            bot.sendMessage(chat_id, "데이터를 받아오는 시간이 너무 오래 걸려 취소 했습니다.", reply_to_message_id=msg_id)
            return
        calhtml = browser.page_source

        # calhtml = urllib.request.urlopen('http://m.wolframalpha.com/input/?i='+searchlist) # urlopen을 이용한 검색임.
        # 이후 소스 페이지를 html로 받아오고 BeautifulSoup로 재가공한다.
        # soup = BeautifulSoup(calhtml, 'lxml')
        soup = BeautifulSoup(calhtml, 'html.parser')
        # solvelist = soup.body.find_all('div', { "class" : "pod " }) # div 중 "class" 이름이 "pod " 인것을 검색.


        tempname=[]
        templink=[]
        temptitle=[]
        calresultnum=0
        #solvelist = soup.body.find_all('div', { "class" : "pod " }) # div 중 "class" 이름이 "pod " 인것을 검색.
        solvelist = soup.find_all(class_=re.compile('(^pod|^pod )'))
        # 위에서 찾은 부분을 분리하고 리스트에 넣음.
        for sol in solvelist:
            tempname.append(sol.h2.get_text().strip().replace(":","")) # 콜론을 제거하고 공백 제거 후 h2영역의 text를 가져옴.
            templink.append(sol.img.get('src')) # 이미지 영역만 가져옴
            temptitle.append(sol.img.get('title'))
            calresultnum+=1

        for i in range(calresultnum):
            _thread.start_new_thread(th_imgmsg, (chat_id,templink,tempname,temptitle,i))
# /cal 처리 영역 끝.


# /hash 처리 영역 시작.
    # /hash 는 리눅스에서 기본적으로 제공하는 해쉬값 만들기를 이용해서 출력한다.
    # 문자열을 입력받으면 해당 문자열에 대해 해쉬값을 반환한다.
    elif listtext[0] == '/hash':
        if len(listtext) < 2:
            bot.sendMessage(chat_id, "\"<code>/hash md5|sha1|sha256|sha512 STRING</code>\" 의 형태로 입력해주세요. 자세한 명령은 <code>/help hash</code>에서 확인가능합니다.", parse_mode='HTML', reply_to_message_id=msg_id)
            return
        # md5 sha1 sha256 sha512
        if listtext[1] == 'md5':
            bot.sendMessage(chat_id, "<code>"+str(subprocess.check_output('echo '+liststr+' | md5sum', shell=True),'utf-8').split()[0]+"</code>", parse_mode='HTML', reply_to_message_id=msg_id)
        elif listtext[1] == 'sha1':
            bot.sendMessage(chat_id, "<code>"+str(subprocess.check_output('echo '+liststr+' | sha1sum', shell=True),'utf-8').split()[0]+"</code>", parse_mode='HTML', reply_to_message_id=msg_id)
        elif listtext[1] == 'sha256':
            bot.sendMessage(chat_id, "<code>"+str(subprocess.check_output('echo '+liststr+' | sha256sum', shell=True),'utf-8').split()[0]+"</code>", parse_mode='HTML', reply_to_message_id=msg_id)
        elif listtext[1] == 'sha512':
            bot.sendMessage(chat_id, "<code>"+str(subprocess.check_output('echo '+liststr+' | sha512sum', shell=True),'utf-8').split()[0]+"</code>", parse_mode='HTML', reply_to_message_id=msg_id)
        else:
            bot.sendMessage(chat_id, "\"<code>/hash md5|sha1|sha256|sha512 STRING</code>\" 의 형태로 입력해주세요. 자세한 명령은 <code>/help hash</code>에서 확인가능합니다.", parse_mode='HTML', reply_to_message_id=msg_id)
# /hash 처리 영역 끝.


# /날씨 처리 영역 시작.
    # 날씨는 daum에서 검색 결과를 가져와서 "시·도" 영역의 텍스트를 이용하여 기상청에서 요약예보를 받아온다.
    # 이후 daum의 검색 결과 중 weatherColl 영역의 크기를 구하여(selenium 활용) PIL을 이용해서 해당하는 크기만큼 crop 한다.
    # 기존의 이미지는 너무 작기 때문에 1.5배 사이즈로 resize 한 뒤 전송한다. (antialiasing 활용)
    # ps. selenium에서 zoom을 하고 이미지를 전송하는 방법도 시도 해보았지만 텍스트는 커지지 않아서 해결방법을 찾다가 포기함.

    # 오늘 내일 모레 까지의 날씨 및 텍스트 날씨를 요청할 수 있다.
    elif listtext[0] == u'/날씨':
        if len(listtext) < 2:
            bot.sendMessage(chat_id, "\"<code>/날씨 위치 [-|0|1|2]</code>\" 의 형태로 입력해주세요. 자세한 명령은 <code>/help 날씨</code>에서 확인가능합니다.", parse_mode='HTML', reply_to_message_id=msg_id)
            return

        # 옵션 인자를 결정하는 부분 tyebo가 0이면 전체, 1이면 내일, 2면 모레, -1은 출력하지 않음, 10은 오늘 이다.
        # 옵션 인자 부분은 재 가공해서 다시 liststr에 저장한다.
        if liststr[len(liststr)-1] == '0' or liststr[len(liststr)-1] == '3':
           tyebo=0
           liststr = liststr[:len(liststr)-1].rstrip()
        elif liststr[len(liststr)-1] == '1':
           tyebo=1
           liststr = liststr[:len(liststr)-1].rstrip()
           liststr = "내일 " + liststr
        elif liststr[len(liststr)-1] == '2':
           tyebo=2
           liststr = liststr[:len(liststr)-1].rstrip()
           liststr = "모레 " + liststr
        elif liststr[len(liststr)-1] == "-":
           tyebo=-1
           liststr = liststr[:len(liststr)-1].rstrip()
        else:
           tyebo=10

        
        # selenium (PhantomJS 브라우저)을 이용해서 해당 주소의 데이터를 로드한다.
        # unicode error 떄문에 이렇게 사용함. 추후 변경 해야함. ASCII 문자를 사용하기 때문에 발생하는 에러가 파이썬 2.x 버전에 있다.
        nalssi0=urllib.parse.quote(liststr)
        nalssi1=urllib.parse.quote(" 날씨")
        browser.get('http://search.daum.net/search?w=tot&q='+nalssi0+nalssi1)

        # 이후 소스 페이지를 html로 받아오고 BeautifulSoup로 재가공한다.
        daumhtml = browser.page_source
        #daumsoup = BeautifulSoup(daumhtml, 'lxml')
        daumsoup = BeautifulSoup(daumhtml, 'html.parser')

        # 이곳에서 예보 요약을 알려준다.
        try: # 해당 try는 아래의 try-except 영역에서 실패했을 경우 해외 주소입력으로 간주하고 해외 처리 부분으로 넘어간다.
            try: # 지역에 해당하는 영역으로 접근했을때 지명이 검색 되는가? 이후 address_kma 함수를 이용해서 해당 지명의 예보요약 주소를 받아와서 저장한다.
                localw=address_kma(daumsoup.find(class_="ico_weather txt_place").text)
            except: # 실패했다면 전국에 해당하는 영역으로 접근 했을때 지명이 검색 되는가? address_kma 함수를 이용해서 전국예보요약 주소를 받아와서 저장한다.
                localw=address_kma(daumsoup.find(id="ico_weather txt_place").text)

                
            # 위에서 저장된 주소를 이용해서 다시 주소를 로드한다.
            kmahtml = urllib.request.urlopen(localw)
            #kmasoup = BeautifulSoup(kmahtml, 'lxml')
            kmasoup = BeautifulSoup(kmahtml, 'html.parser')
            kmasummary = kmasoup.find_all(class_='table_announcementtime') # 예보요약 영역을 가져옴.
            
            # 문자열 위에서 가져와서 알맞게 분리
            wsummary=[]
            # 문자열을 알맞게 가공후 wsummary 리스트에 저장.
            for i in kmasummary:
                wsummary.append((i.text.replace(u"다.",u"다.\n").replace("\n\n\n\n\n\n","\n").rstrip())[9:])

            # 옵션 인자 처리 부분
            if tyebo == 0:
                wwsum=wsummary[0] + "\n==============================\n" + wsummary[1] + "\n==============================\n" + wsummary[2]
            elif tyebo == 1:
                wwsum=wsummary[1]
            elif tyebo == 2:
                wwsum=wsummary[2]
            else:
                wwsum=wsummary[0]

            if tyebo != -1:
                bot.sendMessage(chat_id, wwsum, reply_to_message_id=msg_id)
            
            # 날씨를 알려주는 div 영역을 element로 저장한다.
            element = browser.find_element_by_id('weatherColl')

        # 해외 및 검색 불가지역 처리 부분
        except:
            try: # 날씨를 알려주는 div 영역을 element로 저장한다.
                element = browser.find_element_by_id('worldWeatherColl')
            except: # 검색이 되지 않으면 알려주고 종료.
                bot.sendMessage(chat_id, "검색되지 않는 지역입니다. 시·도를 넣어 검색해보세요.", reply_to_message_id=msg_id)
                return

            # 옵션 인자 처리 부분.
            if tyebo != -1:
                bot.sendMessage(chat_id, "해외는 요약 날씨를 지원하지 않습니다.", parse_mode='HTML', reply_to_message_id=msg_id)


        # 해당하는 영역의 좌표를 구하는 부분.
        # selenium 내에서 자바스크립트를 활용하여 좌표를 가져온다
        crop_points = browser.execute_script("""
            var r = arguments[0].getBoundingClientRect();
            return [r.left, r.top, r.left + r.width, r.top + r.height];
            """, element)
        
        # 위에서 구한 영역으로 스크린샷을 crop 한다.
        with Image.open(io.BytesIO(browser.get_screenshot_as_png())) as img:
            with img.crop(crop_points) as imgsub :
                # 크기가 작아서 1.5배 크기만큼 resize 한다.
                imgsub = imgsub.resize([int((crop_points[2]-crop_points[0])*1.5),int((crop_points[3]-crop_points[1])*1.5)], Image.ANTIALIAS)
                # 이미지 생성 후 전송하고 삭제. 
                # imgsub를 바로 전송할 수는 없다. 지원하는 부분이 fopen을 이용한 전송과 urllib2을 통한 이미지 전송만 가능함.
                imgsub.save('/tmp/tmpweatherimg.png', 'PNG')
                result = bot.sendPhoto(chat_id, open('/tmp/tmpweatherimg.png','rb'), reply_to_message_id=msg_id)
                os.remove('/tmp/tmpweatherimg.png')
# /날씨 처리 영역 끝.



# /미세먼지 처리 영역 시작.
    # 미세먼지를 daum에서 검색 결과를 가져온다.
    # 이외에는 /날씨 부분의 crop 부분과 동일하다.
    elif listtext[0] == u'/미세먼지':
        if len(listtext) < 2:
            nalssi0=urllib.parse.quote("전국")

        # selenium (PhantomJS 브라우저)을 이용해서 해당 주소의 데이터를 로드한다.
        # unicode error 떄문에 이렇게 사용함. 추후 변경 해야함. ASCII 문자를 사용하기 때문에 발생하는 에러가 파이썬 2.x 버전에 있다.
        nalssi0=urllib.parse.quote(liststr)
        nalssi1=urllib.parse.quote(" 미세먼지")
        browser.get('http://search.daum.net/search?w=tot&q='+nalssi0+nalssi1)
        element = browser.find_element_by_id('airPollutionNColl')

        # 해당하는 영역의 좌표를 구하는 부분.
        crop_points = browser.execute_script("""
            var r = arguments[0].getBoundingClientRect();
            return [r.left, r.top, r.left + r.width, r.top + r.height];
            """, element)
        
        # 위에서 구한 영역으로 스크린샷을 crop 한다.
        with Image.open(io.BytesIO(browser.get_screenshot_as_png())) as img :
            with img.crop(crop_points) as imgsub :
                # 크기가 작아서 1.5배 크기만큼 resize 한다.
                imgsub = imgsub.resize([int((crop_points[2]-crop_points[0])*1.5),int((crop_points[3]-crop_points[1])*1.5)], Image.ANTIALIAS)
                # 이미지 생성 후 전송하고 삭제. 
                # imgsub를 바로 전송할 수는 없다. 지원하는 부분이 fopen을 이용한 전송과 urllib2을 통한 이미지 전송만 가능함.
                imgsub.save('/tmp/tmpmiseimg.png', 'PNG')
                result = bot.sendPhoto(chat_id, open('/tmp/tmpmiseimg.png','rb'), reply_to_message_id=msg_id)
                os.remove('/tmp/tmpmiseimg.png')


# /미세먼지 처리 영역 끝.



# /tts 처리 영역 시작.
    # 영어와 한국어를 읽을수 있다. 다른 언어도 지원하지만 큰 필요성을 느끼지 못함.
    # responsivevoice에서 제공하는건 한번에 300자까지만 지원된다.
    # responsivevoice는 비상업적 용도로 사용하는것은 괜찮다.
    elif listtext[0] == '/tts' or listtext[0] == '/ttse' or listtext[0] == 'ttsk':
        if len(listtext) < 2:
            bot.sendMessage(chat_id, "\"<code>/tts 문자열</code>\" 또는 \"<code>/ttse 문자열(eng)</code>\" 의 형태로 입력해주세요. 자세한 명령은 <code>/help tts</code>에서 확인가능합니다.", parse_mode='HTML', reply_to_message_id=msg_id)
            return
        # 글자수를 세기위해 포맷을 변경.
        # 한번에 최대 300자까지 지원된다.
        liststr=u'{0}'.format(liststr)
        if len(liststr) <= 300:
            ttstext=urllib.parse.quote(liststr)
            try:
                # /tts는 한글로 처리, /ttse는 영어로 처리.
                if listtext[0] == '/ttse':
                    os.system('wget -O \'/tmp/tmptts.mp3\' \'http://responsivevoice.org/responsivevoice/getvoice.php?t=' + ttstext + '&tl=en-US\'')
                else:
                    os.system('wget -O \'/tmp/tmptts.mp3\' \'http://responsivevoice.org/responsivevoice/getvoice.php?t=' + ttstext + '&tl=ko-KR\'')
                bot.sendVoice(chat_id, open('/tmp/tmptts.mp3','rb'), reply_to_message_id=msg_id)
                os.remove('/tmp/tmptts.mp3')
            except:
                 bot.sendMessage(chat_id, "알수없는 원인으로 실패했습니다.", reply_to_message_id=msg_id)
        
        # 300자가 넘으면 문자열을 나누어서 쓰레드로 처리한 뒤 합친후 전송한다.
        else:
            global ttsnum # 쓰레드 완료 확인 변수

            ttslist=[] # 문자열을 나누어서 저장할 배열
            # 300자로 잘랐을때 가장 가까운 공백에서 문자열을 나누어서 배열에 저장한다.
            while len(liststr)>250:
                div=liststr[:250].rfind(" ")
                if div==0:
                    bot.sendMessage(chat_id, "알수없는 원인으로 실패했습니다.", reply_to_message_id=msg_id)
                    return
                ttslist.append(liststr[:div].strip())
                liststr=liststr[div:].strip()

            for abcd in ttslist:
                print(len(abcd))

            ttsthreadnum=0 # 쓰레드 번호.
            # 쓰레드 실행
            for ttsn in ttslist:
                _thread.start_new_thread(th_maketts, (listtext[0], ttsn, ttsthreadnum))
                ttsthreadnum+=1

            # 쓰레드 대기. 함수
            while True:
                if ttsnum==len(ttslist):
                    break

            ttsnum=0 # 쓰레드 완료확인 변수 초기화

            # mp3 이어붙임. ls -v 로 정렬해서 안하면 1번다음 10번이 옴
            os.system('mp3wrap /tmp/tmp_tts.mp3 `ls -v /tmp/tmptts*.mp3`')
            bot.sendVoice(chat_id, open('/tmp/tmp_tts_MP3WRAP.mp3','rb'), reply_to_message_id=msg_id) # 보내고
            for i in range(len(ttslist)): # 삭제
                os.remove('/tmp/tmptts'+str(i)+'.mp3')
            os.remove('/tmp/tmp_tts_MP3WRAP.mp3')
# /tts 처리 영역 끝.


# /eh 처리 영역 시작.
    # 영타를 한글로 바꿔주는 명령어이다.
    elif listtext[0] == '/eh':
        global cho_index, word_list
        if len(listtext) < 2:
            bot.sendMessage(chat_id, "\"<code>/eh 영타</code>\" 의 형태로 입력해주세요. 자세한 명령은 <code>/help eh</code>에서 확인가능합니다.", parse_mode='HTML', reply_to_message_id=msg_id)
            #print(unichr(0xac00)
            return
        # 글자수를 세기위해 포맷을 변경.
        # 한번에 최대 300자까지 지원된다.
        liststr=u'{0}'.format(liststr)
        cho_index = []
        word_list = []
        eh_ans=""
        ETH(liststr)
        for x in word_list:
            eh_ans=eh_ans+x
        bot.sendMessage(chat_id, eh_ans, reply_to_message_id=msg_id)
        print(eh_ans) 

# /eh 처리 영역 끝

# 번역부분 시작
    elif listtext[0] == '/tr':
        if len(listtext) < 2 or len(liststr.strip()) == 0:
            bot.sendMessage(chat_id, "\"<code>/tr 번역할 내용</code>\" 의 형태로 입력해주세요. 자세한 명령은 <code>/help tr</code>에서 확인가능합니다.", parse_mode='HTML', reply_to_message_id=msg_id)
            return
        alpha_n=0                                                                                                                     for t in liststr:
            if t in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                alpha_n+=1

        print(alpha_n,len(liststr),alpha_n/len(liststr))

        if alpha_n/len(liststr) > 0.60:
            # 영->한 번역
            trans_res=div_sentence(liststr,1)
        else:
            trans_res=div_sentence(liststr,0)

        bot.sendMessage(chat_id, trans_res, reply_to_message_id=msg_id)
# 번역부분 끝

    else:
        return


# InlineKeyboard 를 이용해서 응답하면 callback_data가 넘어온다.
# callback_data를 처리하는 영역.
def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
#    print 'Callback query:', query_id, from_id, data
#    pprint.pprint(msg)

    # callback_data == data 이다. 이걸 재가공한다
    anslist = data.split()
    
    # anslist가 close라면 취소.
    if anslist[0] == 'close':
        bot.answerCallbackQuery(query_id, text='cancelled')
        bot.editMessageText((msg['message']['chat']['id'], msg['message']['message_id']), '요청 취소')
    
    # magnet 이라면 마그넷을 반환한다. 반환할때 인라인 키보드를 출력한 메시지id를 이용해서 수정하여 출력한다.
    elif anslist[0] == 'magnet':
        bot.editMessageText((msg['message']['chat']['id'], msg['message']['message_id']), anslist[1])
        return

    # magdown 이라면 transmission-remote를 이용하여 다운로드 후 메시지를 수정하여 출력한다.
    elif anslist[0] == 'magdown':
        # os.system은 명령의 성공 유무를 반환해 준다.
        if os.system('transmission-remote *트랜스미션 주소*:*포트* -n *트랜스미션아이디*:*암호* -a magnet:?xt=urn:btih:' + anslist[1]) == 0:
            bot.editMessageText((msg['message']['chat']['id'], msg['message']['message_id']), "다운로드 요청이 완료되었습니다.")
        else:
            bot.editMessageText((msg['message']['chat']['id'], msg['message']['message_id']), "알수없는 원인으로 실패하였습니다.")
        return

    # 다른게 넘어오면 그냥 리턴
    else:
        return



# 인라인 질의 처리 부분이다. 사용하지 않으므로 바로 return 처리함.
# 더 알아봐야할 영역.
def on_inline_query(msg):
    return
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('%s: Computing for: %s' % (threading.current_thread().name, query_string))

        articles = [InlineQueryResultArticle(
                        id='abcde', title='Telegram', input_message_content=InputTextMessageContent(message_text='Telegram is a messaging app')),
                    dict(type='article',
                        id='fghij', title='Google', input_message_content=dict(message_text='Google is a search engine'))]

        photo1_url = 'https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf'
        photo2_url = 'https://www.telegram.org/img/t_logo.png'
        photos = [InlineQueryResultPhoto(
                      id='12345', photo_url=photo1_url, thumb_url=photo1_url),
                  dict(type='photo',
                      id='67890', photo_url=photo2_url, thumb_url=photo2_url)]

        result_type = query_string[-1:].lower()

        if result_type == 'a':
            return articles
        elif result_type == 'p':
            return photos
        else:
            results = articles if random.randint(0,1) else photos
            if result_type == 'b':
                return dict(results=results, switch_pm_text='Back to Bot', switch_pm_parameter='Optional start parameter')
            else:
                return dict(results=results)

    answerer.answer(msg, compute)



# 마찬가지로 인라인 질의 처리 부분이다. 사용하지 않으므로 바로 return 처리함.
# 더 알아볼 영역.
def on_chosen_inline_result(msg):
    return
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)



# main 함수 시작.

# python 2.7의 경우 발생하는 에러들
# unicode error : ascii 사용 불가일때 아래와 같이 처리한다. 
# https://libsora.so/posts/python-hangul/ 이곳을 참조.
# 이후 문제가 발생하는 한글을 str(unicode("문제가 발생하는 한글")) 로 처리해서 재배정하면 발생하지 않음.


whitelist=["lcs901221"]

# selenium을 이용해서 PhantomJS 브라우저를 실행한다.
# 30초 이상 로드가 된다면 에러로 간주하고 timeout
browser = webdriver.PhantomJS()
browser.set_page_load_timeout(30)

# 번역기 부분
isE2K=0
trans_browser = webdriver.Firefox()
url="http://labspace.naver.com/nmt/"
trans_browser.get(url)

# input area
inout=trans_browser.find_elements_by_tag_name("app-text-input")
in_element = inout[0].find_element_by_tag_name("textarea")

# trans_btn
trans = trans_browser.find_element_by_xpath("//*[@class='menu-target']")
trans_btn=trans.find_element_by_tag_name("button")

# trans_switch
swit = trans_browser.find_element_by_xpath("//*[@class='menu-source']")
swit_btn=swit.find_element_by_tag_name("app-button-switch")


# telepot token 입력 부분.
bot = telepot.Bot(''' 봇파더에서 제공하는 토큰을 입력하세요 ''')

# 인라인 질의 관련 부분이다.
answerer = telepot.helper.Answerer(bot)

# 메시지의 형태에 따라서 함수 호출.
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query,
                  'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result})
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(1)
