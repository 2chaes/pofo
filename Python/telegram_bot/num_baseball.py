#!/usr/bin/python3

import sys
import random
import traceback
import telepot
from telepot.delegate import per_chat_id, create_open


# 야구게임 봇


# Strike인지 Ball인지 판단하는 함수이다.
def Check_StrikeBall(gNum,ans):
	SBarr=[0,0] # 일치한 만큼 증가, 순서대로 strike,ball
	for i,sb in enumerate(gNum):
		if sb in ans: # 해당 숫자가 존재함
			if ans[i] == sb: # 숫자가 존재하고, 위치도 일치한다면 strike
				SBarr[0]+=1
			else: # 위치가 일치하지 않는다면 ball
				SBarr[1]+=1

	return SBarr



class Player(telepot.helper.ChatHandler):
	def __init__(self, seed_tuple, timeout):
		super(Player, self).__init__(seed_tuple, timeout)
		# 보통의 숫자야구는 같은 숫자를 사용하지 않기때문에
		# 일련의 숫자들을 반복해서 생성하는 과정에서 집합에 넣어 중복을 제거한다.
		# 집합의 길이가 4라면 생성, 아니라면 패스한다.
		self.arr = [str(x0)+str(x1)+str(x2)+str(x3) for x0 in range(10) for x1 in range(10) for x2 in range(10) for x3 in range(10) if len({x0,x1,x2,x3}) == 4]

		self.chan_Num=1
		self.input_check=0
		self.choiceNum = self.arr[random.randrange(0,len(self.arr))]


# 상대방이 불러준 스트라이크, 볼 조건에 맞지 않는 숫자들은 제거한다.
	def GuessNum(self, choiceNum, sbArr):
		for num in self.arr[:]:
			if sbArr != Check_StrikeBall(num,self.choiceNum):
				self.arr.remove(num)


	# num은 몇번째인지 받아오는 변수
	def PlayerInput(self, msg):
		#self.sender.sendMessage(str(self.chan_Num)+"번째 Player's Pick?")
		pNum = msg['text']
		if len(pNum) !=4 or not pNum.isnumeric():
			return 1
		self.result=Check_StrikeBall(pNum, self.choiceNum)
		if self.result == [4,0]:
			self.sender.sendMessage("정답입니다.")
			self.close()
		self.sender.sendMessage("Strike : {0}, Ball : {1}".format(self.result[0],self.result[1]))
		self.input_check=1


	# 유저 인스턴스가 생성될때 초기화 하는 함수(open) 오버라이딩.
	def open(self, initial_msg, seed):
		# 여기서 세팅함
		liststr = initial_msg['text']
		if liststr not in ['/guess', '/game', 'guess']:
			self.sender.sendMessage('guess 를 입력하세요')
			self.close()
		if liststr in ['/guess', 'guess']:
			self.guessMode="y"
			self.input_check = 1
			self.sender.sendMessage("""***Guess Mode Start***
상대방의 숫자와 Strike,Ball을 입력해주세요
(ex : 1234 12)
all : 현재 상태에서 가능한 모든 경우의 수를 보여줍니다.
exit : 종료합니다.""")
		#ACmode = input("Auto Choice  활성화? (y/n) : ")
		#GameMode = input("Game 활성화? (y/n) : ")
		return True  # prevent on_message() from being called on the initial message


	#
	def on_chat_message(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg)

		if content_type != 'text':
			self.sender.sendMessage('Give me a number, please.')
			return

		if msg['text'] in ['/exit', 'exit']:
			self.sender.sendMessage('종료합니다.')
			self.close()

		if self.guessMode != "y":
			if self.input_check == 0:
				if self.PlayerInput(msg) == 1:
					self.sender.sendMessage('잘못 입력했습니다.')
				return

		if self.input_check == 1:
			if msg['text'] in ['/all', 'all']:
				if len(self.arr) <= 300:
					self.sender.sendMessage(str(self.arr))
				else:
					self.sender.sendMessage("경우의 수가 너무 많아 전송 할 수 없습니다. ({0}개)".format(len(self.arr)))
				return
			self.choiceNum=""
			self.result = []
			n=0
			for i in msg['text']:
				if not i.isnumeric():
					continue
				if n<4:
					self.choiceNum+=i
					n+=1
				elif n<6:
					self.result.append(int(i))
					n+=1
				else:
					break

			try:
				if not (self.choiceNum.isnumeric() and len(self.choiceNum) == 4 and self.result != [3,1] and self.result[0]+self.result[1] <= 4):
					self.sender.sendMessage("***입력에러 입니다***.\n상대방의 숫자와 Strike,Ball을 입력해주세요\n(ex : 1234 12)")
					return
			except:
				self.sender.sendMessage("***입력에러 입니다***.\n상대방의 숫자와 Strike,Ball을 입력해주세요\n(ex : 1234 12)")
				return
			# if guess모드라면 inputnum, [strike ball]도 입력해야함.
			self.GuessNum(self.choiceNum, self.result)
			#self.input_check = 0

			if len(self.arr) == 0:
				self.sender.sendMessage("해당하는 숫자가 없습니다.\n잘못된 입력이 예상됩니다.")
				self.close()
			elif len(self.arr) == 1:
				self.sender.sendMessage("The Answer is " + self.arr[0])
				self.close()
			elif len(self.arr) >= 5:
				rand_pick = [self.arr[i] for i in random.sample(range(len(self.arr)),5)]
				self.sender.sendMessage("Random Pick (1/{0}, {1:.5}%)\n상대방에게 불러볼 수 있는 수\n{2}".format(len(self.arr), 100/len(self.arr), str(rand_pick)))
			else:
				self.sender.sendMessage("Pick (1/{0}, {1:.5}%)\n{2}".format(len(self.arr), 100/len(self.arr), str(self.arr)))
		
		return



	# 유저 인스턴스가 종료될때 호출되는 함수 오버라이딩.
	def on_close(self, exception):
		if isinstance(exception, telepot.exception.WaitTooLong):
			self.sender.sendMessage('Expired.')


TOKEN = ' *** 봇파더에게서 부여받은 토큰을 입력하세요 ***'

# 유저 넘버를 이용해서 각 유저마다 인스터스를 생성한다.
# 1대 다의 응답이 가능한 방식이다.
# 5분간 입력이 없다면 인스턴스 close
bot = telepot.DelegatorBot(TOKEN, [
	(per_chat_id(), create_open(Player, timeout=300)),
])
bot.message_loop(run_forever='Listening ...')
