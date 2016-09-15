check=`cat /Scripts/restoreLAN/VLAN`

sleep 20

BUPUSH=`sed -n 5p /Scripts/.info`

if [ $check = 1 ]; then

    YMD=`date|cut -c3-4``date|cut -c7-8``date|cut -c11-12`
    TIME=`date|cut -c21-28`
	MD=`date|cut -c7-8`"-"`date|cut -c11-12`
	LTIME=`date|cut -c21-25`
	LOG=`sed -n 3p /Scripts/.info`
	TVLOG=`sed -n 4p /Scripts/.info`

curl -u "$BUPUSH": https://api.pushbullet.com/v2/pushes -d type=note -d title="재부팅 알림 (인터넷 연결 문제 확인)" -d body="인터넷 연결문제가 확인 되어서 재부팅을 시행하였습니다." --insecure 1> /dev/null 2>&1

	if [ $? != 0 ]; then
        echo "$YMD | $TIME | 재부팅 이후에도 인터넷 연결에 문제가 있습니다." >> $LOG
	else
        echo "$YMD | $TIME | 재부팅 이후 인터넷을 복구 했습니다." >> $LOG
        echo "$MD|$LTIME|!alert [알림] 재부팅 이후 인터넷을 복구 했습니다." >> $TVLOG
	fi

echo "0" > /Scripts/restoreLAN/VLAN

else

curl -u "$BUPUSH": https://api.pushbullet.com/v2/pushes -d type=note -d title="재부팅 알림 (임의 시행)" -d body="임의로 재부팅을 시행하였습니다." --insecure 1> /dev/null 2>&1

fi
