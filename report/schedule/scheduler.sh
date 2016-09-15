#!/bin/sh

# 오늘의 Month, Day를 받아온다.
MM=`date|cut -c7-8` 
DD=`date|cut -c11-12`

case "$1" in


"CT") # Change Task : 날짜를 입력하면 일정을 입력 및 수정할 수 있다.

	if [ -z "$2" ]
	then
	echo "날짜를 입력해주세요"
	return 1
	fi	

	#Save Line : 이걸 이용해서 필요한 부분의 라인을 저장
	SL=`grep "$2" cal.txt`

	# 위에서 저장한 라인을 이용해서 날짜 및 요일부분만 저장
	XDAY=`echo $SL|cut -c1-11`

	# 일정 입력 받음
	echo "일정을 입력하세요 : \c"
	read TASK

	#Selected Month, #Selected Day 아래의 sed 명령어에서 검색하기 위해서 월/일을 분리함
	SM=`echo $2|cut -c1-2`
	SD=`echo $2|cut -c4-5`

	# [] = 안에 들어가는 문자중 하나를 검색. /를 검색하면 명령어로 인식하므로 /를 문자화 시키기위한 트릭
	sed /"$SM"[/]"$SD"/c"$XDAY""$TASK." cal.txt > calsample.txt

	# 저장되었다는 멘트 출력 및 변경결과를 같은 이름으로 저장하기 위한 저장작업
	echo "$XDAY$TASK.\n저장되었습니다."
	rm cal.txt
	mv calsample.txt cal.txt
;;	

"DT") # Delete Task : 날짜를 입력하면 지정한 날짜의 일정이 초기화된다. 위의 구조와 비슷

	if [ -z "$2" ]
	then
	echo "날짜를 입력해주세요"
	return 1
	fi

	SL=`grep "$2" cal.txt`
	XDAY=`echo $SL|cut -c1-11`

	SM=`echo $2|cut -c1-2`
	SD=`echo $2|cut -c4-5`

	sed /"$SM"[/]"$SD"/c"$XDAY"\* cal.txt > calsample.txt # cal.txt 파일에서 빈 일정을 뜻하는 * 삽입.

	echo "일정이 초기화 되었습니다."
	rm cal.txt
	mv calsample.txt cal.txt
;;	

"BU") # Back Up : 사용자의 홈 디렉토리에 calbackup폴더를 만들어서 달력을 백업


	if [ "$2" = "r" ] #CT와 DT에서 MM/DD형식을 지키지 않고 쳤을때 cal.txt가 이상해질 우려가있음.
	then
	cp -f ~/calbackup/cal.txt cal.txt
	echo "default 달력으로 복구 되었습니다." # 따라서 cal.txt 파일이 날아갈 경우에 대비해서 초기달력 불러오기
	
	else
	savename=`date|cut -c7-8``date|cut -c11-12``date|cut -c20-21``date|cut -c23-24``date|cut -c26-27`.txt

	# 디렉토리가 없다면 만들고, 있다면 에러 메세지 뜨니까 서버 에러 메세지 휴지통으로 보낸다.
	# 파일백업 및 저장멘트 출력
	mkdir ~/calbackup 2> /dev/null 
	cp cal.txt ~/calbackup/$savename

	echo "`date|cut -c7-8`월 `date|cut -c11-12`일 `date|cut -c20-21`시 `date|cut -c23-24`분 `date|cut -c26-27`초에 백업 되었습니다."
	fi
;;

"LT")


# List of Task : 일정 목록을 확인하는 명령.
# LT만 쳤을 경우, 공휴일을 포함한 모든 일정을 출력한다.
# LT 0을 쳤을 경우, 공휴일을 제외한 모든일정을 출력한다.
# LT 숫자를 쳤을 경우, 오늘부터 숫자만큼의 일정을 출력한다.
# 달력의 구성은 빈 일정인 Line은 *을 포함하고, 일정이 있는 Line끝에는 항상 . 이 저장되어있다.

	if [ -z "$2" ] # $2에 해당하는 인자가 null 일때 모든 일정을 출력
	then

	 echo "공휴일을 포함한 모든 일정을 출력합니다."
	 grep "\." cal.txt

	elif [ "$2" = 0 ] # 0을 적으면 공휴일을 제외한 모든일정이 출력되도록 설정!
	then

	 echo "공휴일을 제외한 모든 일정을 출력합니다."
	 grep "\." cal.txt | grep -v "#"


	else # 이외의 숫자를 적으면 숫자일수 만큼 일정 출력
	 echo "오늘부터 $2개의 일정을 출력합니다.\n"

	 # Line Number : 날짜를 index 하기위해 Line Number를 저장 후 이를 이용해 숫자만큼 일정 출력

	 LN=`grep -n $MM/$DD cal.txt | cut -d':' -f1`
	 more +$LN -$2 cal.txt > cal1.txt

	 grep "\." cal1.txt > cal2.txt # 오늘 이후의 일정을 체크하기 위해서 재검색후 저장

	 sed "$2q" cal2.txt
	 rm cal1.txt cal2.txt
	fi
;;

"MT") #Month Task : 입력한 달의 모든 일정 출력


	if [ -z "$2" ]
	then
	 echo "Month를 입력해주세요."

	# 앞부분만 검색하는 연산자 ^를 사용함
	# 1이나 2만 입력하면 11월, 12월도 함께 검색되니까 아래처럼 설정

	elif [ "$2" = 1 ]
	then
	 grep ^"01/" cal.txt

	elif [ "$2" = 2 ]
	then
	 grep ^"02/" cal.txt

	else # 달만 검색되게 /를 추가하여 검색하도록 설정
	 grep $2/ cal.txt

	fi
;;

"ST") # Search Task : 날짜나 단어로 일정을 검색한다


	# SW를 이용해서 날짜나 단어를 입력받고 일정 검색 실행후 출력

	echo "일정을 검색합니다. 날짜나 단어를 입력해 주세요 : \c"
	read SW
	grep -w $SW cal.txt
;;

"TT")  #Today Task : 오늘 일정을 출력한다. 뒤에 숫자를 입력하면 오늘부터 n일동안의 일정을 출력한다.


	if [ -z "$2" ] # 뒤에 인자가 없으면 오늘 일정만 출력
	then
	 echo "오늘의 일정은.."
	 grep $MM/$DD cal.txt

	else # 뒤에 인자가 있으면 인자만큼의 일정을 출력

	 # Line Number 밑으로 출력되는 파일을 생성후
	 # 그 파일의 $2번째 줄까지만 출력하고, 다시 파일을 삭제한다.
	 echo "오늘부터 $2일간의 일정을 출력합니다."
	 LN=`grep -n $MM/$DD cal.txt | cut -d':' -f1` 
	 more +$LN -$2 cal.txt > cal1.txt

	 sed "$2q" cal1.txt
	 rm cal1.txt
	fi
;;

"WT") # Week task : 이번주의 일정을 출력한다.


	# Line Number, DAY (요일)을 저장한다.
	LN1=`grep -n $MM/$DD cal.txt | cut -d':' -f1`
	DAY=`date|cut -c16-17`

	# LN과 DAY를 이용하여 항상 월요일부터 출력 될 수 있도록 설정한다.
	echo "이번주의 일정을 출력 합니다."
	if [ "$DAY" = "월" ]
	then
	 more +"$LN1" -7 cal.txt > cal1.txt

	 sed "7q" cal1.txt
	 rm cal1.txt

	elif [ "$DAY" = "화" ]
	then
	 more +`expr "$LN1" - 1` -7 cal.txt > cal1.txt

	 sed "7q" cal1.txt
	 rm cal1.txt

	elif [ "$DAY" = "수" ]
	then
	 more +`expr "$LN1" - 2` -7 cal.txt > cal1.txt

	 sed "7q" cal1.txt
	 rm cal1.txt

	elif [ "$DAY" = "목" ]
	then
	 more +`expr "$LN1" - 3` -7 cal.txt > cal1.txt

	 sed "7q" cal1.txt
	 rm cal1.txt

	elif [ "$DAY" = "금" ]
	then
	 more +`expr "$LN1" - 4` -7 cal.txt > cal1.txt

	 sed "7q" cal1.txt
	 rm cal1.txt

	elif [ "$DAY" = "토" ]
	then
	 more +`expr "$LN1" - 5` -7 cal.txt > cal1.txt

	 sed "7q" cal1.txt
	 rm cal1.txt

	elif [ "$DAY" = "일" ]
	then
	 more +`expr "$LN1" - 6` -7 cal.txt > cal1.txt

	 sed "7q" cal1.txt
	 rm cal1.txt

	fi
;;

"DDAY") # D-DAY : 오늘부터 몇일이 남았는지 체크한다.

	echo "몇월 몇일을 체크하시겠습니까?"
	echo "(월(MM) 입력 후 Enter / 일(DD) 입력 후 Enter) \c"
	read RM
	read RD

	# 입력받은 Month를 Day로 변환 (case문을 사용하여 line수를 줄이려했으나 중첩case문은 안되는것 같음)
	if [ "$RM" = "01" ]
	then
	RM1=30
	elif [ "$RM" = "02" ]
	then
	RM1=58
	elif [ "$RM" = "03" ]
	then
	RM1=89
	elif [ "$RM" = "04" ]
	then
	RM1=119
	elif [ "$RM" = "05" ]
	then
	RM1=150
	elif [ "$RM" = "06" ]
	then
	RM1=180
	elif [ "$RM" = "07" ]
	then
	RM1=211
	elif [ "$RM" = "08" ]
	then
	RM1=242
	elif [ "$RM" = "09" ]
	then
	RM1=272
	elif [ "$RM" = "10" ]
	then
	RM1=303
	elif [ "$RM" = "11" ]
	then
	RM1=333
	elif [ "$RM" = "12" ]
	then
	RM1=364
	else
	echo "월을 바르게 입력해주세요 (1월 -> 01)" # 형식과 다르게 입력을 받았을경우 안내문 출력후 바로종료
	return 1
	fi

	if [ "$MM" = "01" ]
	then
	MM1=30
	elif [ "$MM" = "02" ]
	then
	MM1=58
	elif [ "$MM" = "03" ]
	then
	MM1=89
	elif [ "$MM" = "04" ]
	then
	MM1=119
	elif [ "$MM" = "05" ]
	then
	MM1=150
	elif [ "$MM" = "06" ]
	then
	MM1=180
	elif [ "$MM" = "07" ]
	then
	MM1=211
	elif [ "$MM" = "08" ]
	then
	MM1=242
	elif [ "$MM" = "09" ]
	then
	MM1=272
	elif [ "$MM" = "10" ]
	then
	MM1=303
	elif [ "$MM" = "11" ]
	then
	MM1=333
	elif [ "$MM" = "12" ]
	then
	MM1=364
	else
	return 1
	fi
	
	SL=`grep $RM/$RD cal.txt`

	# 날짜 계산후 양수이면 "남았습니다" 음수이면 "지났습니다" 출력

	DY=`expr $RM1 - $MM1 + $RD - $DD` 
	if [ "$DY" -ge 0 ]
	then
	echo "$SL 까지 $DY일 남았습니다."
	else
	DY=`expr $DY \* -1`
	echo "$SL 부터 $DY일 지났습니다."
	fi
;;

*)

	echo " 올바른 명령어를 입력해주세요\n"
	echo " ******주의 : 날짜를 입력할때 MM/DD (01/01) 형태로 사용해주세요******"
	echo "  *****cal.txt 파일에 이상이 생겼을경우에는 ca BU r로 복구하세요****"
	echo "     *******alias로 먼저 등록하고 사용하는것을 권장합니다.*******\n"
	echo " (Change Task)\tCT : 날짜를 입력하면 일정을 입력 및 수정할 수 있다. + MM/DD"
	echo " (Delete Task)\tDT : 날짜를 입력하면 지정한 날짜의 일정이 초기화 된다. + MM/DD"
	echo " (Back Up)\tBU : 사용자의 홈 디렉토리에 calbackup폴더를 만들어서 달력을 백업 + 공백,r"
	echo " (List of Task)\tLT : 일정 목록을 확인하는 명령. + 공백,0,숫자"
	echo " (Month Task)\tMT : 입력한 달의 모든 일정 출력 + 01월~12월"
	echo " (Search Task)\tST : 날짜나 단어로 일정을 검색한다"
	echo " (Today Task)\tTT : 오늘 일정을 출력한다. 숫자를 입력하면 n일동안의 일정을 출력한다.+ 공백,숫자"
	echo " (Week Task)\tWT : 이번주의 일정을 출력한다."
	echo " (D-Day)\tDDAY : 오늘부터 몇일이 남았는지(지났는지) 출력한다."
;;

esac