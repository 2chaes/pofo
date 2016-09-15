#!/bin/sh

# info 경로를 설정해주세요.
SERVER=`sed -n 1p /Scripts/.info`
SITE=`sed -n 2p /Scripts/.info`
LOG=`sed -n 3p /Scripts/.info`
KEY=`echo $* | sed 's/\ /+/g'`

if [ -z $KEY ]; then
echo "**(날짜) 프로그램 제목 (화질)을 적으세요.**"
exit 0
fi

# 검색 키워드를 가져옴
PNAME="$KEY"

# 토렌트 서버 부하를 줄이기 위해 임시파일을 저장해서 사용한다.
echo `curl -s "$SITE""$KEY"` > ~/temp_torlist
sed -i 's/<item><title>/<item><title>\n/g' ~/temp_torlist 

LNUM=`grep -cv [*] ~/temp_torlist`

if [ $LNUM -eq 1 ]; then
echo "검색결과가 없습니다."
rm ~/temp_torlist
exit 0
fi

num=2
# rotn=`wc -l ~/temp_torlist`

# 라인수 기본이 1이므로 2부터 검색결과가 확인됨.
rotn=`grep -cv [*] ~/temp_torlist`

echo "총 `expr $rotn \- 1`개가 검색되었습니다."

while [ $num -le $LNUM ]
do

	# 게시물 제목 / 마그넷 가져옴
	TITLE=`sed -n "$num"p ~/temp_torlist | cut -d'<' -f1`
	MAG=`sed -n "$num"p ~/temp_torlist | cut -d : -f 4 | cut -d'&' -f1`


	echo "(`expr $num \- 1`/`expr $LNUM \- 1`) $TITLE"

	echo "를 다운로드 하시겠습니까? (h: 네, j: 이전파일, k: 다음파일, l: 취소)"
	read ANS

	case $ANS in
	h|H|ㅗ)
		rm ~/temp_torlist
		break;
	;;
	j|J|ㅓ) # num이 2랑 같으면 무시
		if [ $num -eq "2" ]; then
		echo "첫번째 파일입니다."
		else
		num=`expr $num \- 1`
		fi
	;;
	k|K|ㅏ)
		if [ $num -eq $LNUM ]; then
	        echo "마지막 파일입니다."
	        else
		num=`expr $num \+ 1` # LNUM이랑 같으면 종료
		fi
	;;
	*)
		rm ~/temp_torlist
		exit 0
	;;
	esac
done

# 쓸데없는 말 발생 안시키려고 변수에 저장
ANS=`transmission-remote $SERVER -a 'magnet:?xt=urn:btih:'"$MAG"`

YMD=`date +%y%m%d`
TIME=`date +%H:%M:%S`
echo "$TITLE 다운 시작합니다."
echo "$YMD | $TIME | $* 다운 시작!!" >> $LOG
