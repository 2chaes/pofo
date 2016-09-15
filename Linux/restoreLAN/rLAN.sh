
# 테스트함
ping -c1 8.8.8.8 > /dev/null

if [ $? != 0 ];
then
YMD=`date +%y%m%d`
MD=`date +%m-%d`
TIME=`date +%H:%M:%S`
LTIME=`date +%H:%M`
LOG=`sed -n 3p /Scripts/.info`
TVLOG=`sed -n 4p /Scripts/.info`
#echo "$YMD | $TIME | 인터넷 문제로 인해 net재부팅을 시행하였습니다." >> $LOG
#echo "$MD|$LTIME|!alert [알림] 인터넷 문제 발생. Network reboot." >> $TVLOG
sudo service networking reload > /dev/null
ping -c1 8.8.8.8 > /dev/null
if [ $? != 0 ];
then
	echo "1" > /Scripts/restoreLAN/VLAN
sudo reboot
fi
fi
