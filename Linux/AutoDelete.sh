#!/bin/sh

#필요한 데이터들을 불러온다.
SERVER=`sed -n 1p /Scripts/.info`
BUPUSH=`sed -n 5p /Scripts/.info`
LOG=`sed -n 3p /Scripts/.info`
TVLOG=`sed -n 4p /Scripts/.info`

#완료된 토렌트(들)의 토렌트 ID를 받아온다.
DONETORID=`transmission-remote $SERVER -l | grep -Ev 'ID|Sum' | awk '/  Done     /{print $1}'`

for TORNUM in $DONETORID
do
	YMD=`date +%y%m%d`
	MD=`date +%m-%d`
	TIME=`date +%H:%M:%S`
	LTIME=`date +%H:%M`
        
	TEMP="$TR_TORRENT_NAME"

	# 해당하는 토렌트 시드 삭제
	transmission-remote $SERVER -t $TORNUM -r
	# 지정한 경로에 다운로드 받는게 아니라면 로그를 남기지 않는다.
	if [ -s "/home/chaesl/tor/tv/$TEMP" ]; then
		#sudo /Scripts/PMchange.sh "$TEMP" 2>> $LOG

        	echo "$YMD | $TIME | $TEMP 다운 완료." >> $LOG
		echo "$MD|$LTIME|$TEMP 다운 완료." >> $TVLOG
		
		curl -u "$BUPUSH": https://api.pushbullet.com/v2/pushes -d type=note -d title="완료 : $TR_TORRENT_NAME" -d body="$YMD | $TIME | $TR_TORRENT_NAME 다운로드 완료" --insecure
	fi
done
