#!/bin/sh

# 사용법 (http://2chaes.xyz)
# crontab에 등록하여 사용하는것을 추천합니다.
# 실행 : /경로/tordown.sh 숫자 검색어
# 스크립트 뒤에 있는 *숫자*는 당일 다운로드 시작인 경우 0, 익일 다운로드 시작인 경우 1로 설정한다.
# 검색어는 띄워쓰기를 해도 상관 없다.
# ex) tordown.sh 0 1박 2일
# ex) tordown.sh 1 마이 리틀 텔레비전 

# .info 파일에서 라인별로 정보를 가져온다.
# SERVER='9091 --auth 트랜스미션ID:암호
# SITE='토렌트 사이트 rss'
# LOG='로그파일 경로'
SERVER=`sed -n 1p /Scripts/.info`
SITE=`sed -n 2p /Scripts/.info`
LOG=`sed -n 3p /Scripts/.info`
TVLOG=`sed -n 4p /Scripts/.info`
BUPUSH=`sed -n 5p /Scripts/.info`

# @반복 시도 횟수
MAXTRY=60
# @반복 간격 횟수!! / 단위:초 (60 = 1분)
ITV=300
YMD=`date +%y%m%d`
MD=`date +%m-%d`
CYMD=$YMD
YMDTS=`date +%m-%d\|%H:%M:%S`
YMDT=`date +%m-%d\|%H:%M`
TIME=`date +%H:%M:%S`
LTIME=`date +%H:%M`
BANMAGNET=""

if [ "$1" != "0" ] && [ "$1" != "1" ]; then
	echo "$YMD | $TIME | 첫번째 인자를 확인해주세요 (0 또는 1)" >> $LOG
	exit 0
fi
if [ -z "$2" ]; then
	echo "$YMD | $TIME | 다운로드 할 파일명을 입력해주세요" >> $LOG
	exit 0
fi

# 만약 $1가 1이라면(어제인 경우) CYMD=$YYMD로 바꾼다.
if [ "$1" = "1" ]; then
	YYMD=`date -d '1 day ago' +%y%m%d`
	CYMD=$YYMD
fi


# 검색 키워드를 가져옴
# 다음날 검색 되는 파일일 경우 $1의 위치에 1을 적어준다.
# 변수 $* 앞에서 부터 해당하는 문자열을 찾아 제거함
OPR=${*##"$1"}
PR=`echo $OPR | sed 's/\ /+/g'`

# $* 데이터를 정규표현식으로 변환한다.
# 추후 transmission에서 마그넷 체크를 하기 위함.
CHECKPR=`echo "$*" | awk '{printf("("); for (i=2;i<=NF-1;i++) printf(".*%s.*|",$i); printf(".*%s.*){%d}", $NF, NF-1)}'`

# @화질 설정 가능
PNAME="$CYMD+$PR+720p" 

# 사이트 존재 여부 테스트
EXTEST=`curl -s "$SITE"$PNAME`
if [ "$EXTEST" = "" ]; then
	curl -u "$BUPUSH": https://api.pushbullet.com/v2/pushes -d type=note -d title="에러" -d body="토렌트서버의 이전이 예상됩니다. 주소를 변경해주세요" --insecure 1> /dev/null 2>&1
fi

# 검색 시행
NUM=1
while [ "$NUM" -lt "$MAXTRY" ];
do

	YMD=`date +%y%m%d`
	TIME=`date +%H:%M:%S`
	LTIME=`date +%H:%M`

	if [ $NUM = 1 ]; then
		echo "$YMD | $TIME | $CYMD.$PR 다운 요청." >> $LOG
	fi

	# 파일 존재 여부 테스트
	EXFILE=`curl -s "$SITE""$PNAME" | cut -b-9`
	if [ "$EXFILE" = "no result" ]; then
		NUM=`expr $NUM + 1`

		# 5번째 마다 로그를 남김
		TNUM=`expr $NUM % 5`
		if [ $TNUM = 0 ]; then
			echo "$YMD | $TIME | $CYMD.$PR 다운 실패. $NUM번째 시도 준비." >> $LOG
		fi

			sleep $ITV

		if [ $NUM = $MAXTRY ]; then
			echo "$YMD | $TIME | $CYMD.$PR 다운 최종실패 ㅠㅠ" >> $LOG

			EXTEST=`curl -s "$SITE"$PNAME`
			if [ "$EXTEST" = "" ]; then
				curl -u "$BUPUSH": https://api.pushbullet.com/v2/pushes -d type=note -d title="$CYMD | $OPR 최종 다운 실패" -d body="토렌트서버의 이전이 예상됩니다. 주소를 변경해주세요" --insecure 1> /dev/null 2>&1
				echo "$MD|$LTIME|$CYMD.$OPR 다운 실패. 서버이전이 예상됩니다." >> $TVLOG
			else
				curl -u "$BUPUSH": https://api.pushbullet.com/v2/pushes -d type=note -d title="$YMD | $OPR 최종 다운 실패" -d body="프로그램 결방이 예상됩니다." --insecure 1> /dev/null 2>&1
				echo "$MD|$LTIME|$CYMD.$OPR 다운 실패. 결방이 예상됩니다." >> $TVLOG
			fi
		fi
	else
		# 검색 결과가 있는 경우
		MAG=`curl -s "$SITE""$PNAME" | sed "s/magnet/\nmagnet/" | sed -n '2p' | cut -d'&' -f1`
		# 광고 마그넷이 검출됐을 경우
		echo $BANMAGNET | fgrep -li $MAG > /dev/null
		if [ "$?" = "0" ]; then
                        sleep $ITV
                        continue
		fi

		# 마그넷 형식이 일치하지 않는 경우
		if [ "${#MAG}" != "60" ]; then
			curl -u "$BUPUSH": https://api.pushbullet.com/v2/pushes -d type=note -d title="오류 : $TR_TORRENT_NAME" -d body="$YMD | $TIME | $TR_TORRENT_NAME 서버이전이 예상됩니다." --insecure

			exit 0
		fi

		# 다운로드 요청 성공
		RUN=`transmission-remote $SERVER -a "$MAG"`

		echo "$YMD | $TIME | $CYMD.$PR 다운 시작!! ($NUM) :$MAG" >> $LOG

		#echo "$MD|$LTIME|$CYMD.$PR 다운 시작!! ($NUM)" >> $TVLOG

		TARGETID=`transmission-remote $SERVER -l | grep -P "$CHECKPR" | awk '{print $1}'`
		while [ "$TARGETID" = "" ];
		do
			sleep 15
			TARGETID=`transmission-remote $SERVER -l | grep -P "$CHECKPR" | awk '{print $1}'`
		done
		
		TARGETINFO=`transmission-remote $SERVER -t"$TARGETID" -i`
		PROGRAMNAME=`echo $TARGETINFO | grep -Po "Name: .*?(.avi|.mp4|.ts)" | awk '{for(i=2;i<=NF-1;i++) printf "%s ", $i; printf "%s", $NF;}'`
		TESTMAGNET=`echo $TARGETINFO | grep -Po "Hash: .*? " | awk '{print $2}'`
		PERCENT=`echo $TARGETINFO | grep -Po "Percent Done: .*?%" | awk '{print $3}'`
		LOCATION=`echo $TARGETINFO | grep -Po "Location:\ .*? " | awk '{print $2}'`
		
		PERN=`transmission-remote $SERVER -l | grep -P "$CHECKPR" | cut -b8-10`
		
		# 30프로보다 작아서 기다림
		while [ "$PERN" -lt "30" ];
		do
			sleep 30
			PERN=`transmission-remote $SERVER -l | grep -P "$CHECKPR" | cut -b8-10`
		done
		
		head -n1 "$LOCATION/$PROGRAMNAME.part" | fgrep -i 'H.264/MPEG-4 AVC codec - Copyleft 2003-2014 - http://www.videolan.org/x264.html' > /dev/null
		
		# 처리 완료하면 =을 !=로 바꿔줘야함
		if [ "$?" != "0" ]; then
			break
		else
			transmission-remote $SERVER -t"$TARGETID" --remove-and-delete > /dev/null
			BANMAGNET="magnet:?xt=urn:btih:$TESTMAGNET""$BANMAGNET"
			echo "$YMD | $TIME | $CYMD.$PR 광고 마그넷 ($NUM) :$BANMAGNET" >> $LOG
			echo "$MD|$LTIME|$CYMD.$PR 광고 마그넷이 예상됩니다. $BANMAGNET" >> $TVLOG
			sleep $ITV
			continue
		fi
		
		# 있으면 해당 마그넷 밴처리하고 다시 검색 시작
	###################################################
	fi

done

