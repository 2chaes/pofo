#!/bin/sh

# 사용법 : macsale.sh '앱이름' '아이튠즈주소' 형식으로 crontab에 등록하면 됩니다.
# 사용 예시 : crontab에 아래와 같이 등록합니다.
# * */4 * * * /script_location/salecheck.sh 'icon_cast' 'https://itunes.apple.com/kr/app/icon-cast/id861460136'
# 사용자 홈dir에 앱이름으로 임시파일이 저장됩니다.
# 구매하셨거나 구매의사가 없어졌다면 홈dir의 임시파일은 삭제해주세요.

#Pushbullet을 사용하신다면 아래에 token을 넣어주세요
#BUPUSH=""

#$2 확인
if [ -z "$2" ]; then
        echo "명령어 'app_name' 'itunes_app_addr' 의 형태로 넣어주세요"
        exit 0
fi

#이전에 저장한 가격을 불러온다. (임시파일 가장 아래에 존재)
if [ -e "./$1" ];
then
	#echo "임시파일 존재함"
	PRICE0=`sed -n "$"p ./$1`
	#echo $PRICE0
else # 첫번째 시행일 경우 임시파일 생성 및 가격을 기록해둔다.
	#echo "임시파일 존재하지 않음."
	touch ./"$1"
	curl -s "$2" > ./"$1"
	sed s/volumePrice\":/\\nvolumePrice,/ ./"$1" | egrep '^volumePrice' | cut -d',' -f2 >> ./"$1"
	#echo "임시파일 없어서 종료"
	exit
fi

# 현재가격을 가져오고 저장한다.
curl -s "$2" > "$1"
sed s/volumePrice\":/\\nvolumePrice,/ ./"$1" | egrep '^volumePrice' | cut -d',' -f2 >> ./"$1"

PRICE1=`sed -n "$"p ./$1`
#echo $PRICE1

# 이곳에 alert을 넣으면 됩니다.
# cron mail로 받고싶다면 echo 주석을, Pushbullet을 사용한다면 curl 주석을 해제하면 됩니다.
# 이전에 저장한 가격과 비교한다.
if [ $PRICE0 != $PRICE1 ];
then
#echo "$1 가격변동 알림! $PRICE0 에서 $PRICE1 로 가격이 변동 되었습니다."
curl -u "$BUPUSH": https://api.pushbullet.com/v2/pushes -d type=note -d title="$1 가격변동 알림!" -d body="$PRICE0 에서 $PRICE1 로 가격이 변동 되었습니다." --insecure 1> /dev/null 2>&1
fi
