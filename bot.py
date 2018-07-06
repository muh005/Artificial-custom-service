import argparse
import sys
from classifier import classify

corpus = ["1. Hello, I am the customer service trail of Lu Fund, which is specially designed to help customers do asset allocation. Recently, we are about to have a star product on the shelves, I think it is suitable for you. Do you have time to figure out?",
		  "2. This is an equity-based investment project that invests in companies that are not yet listed on the market but are valuable. Have you ever been heard of this type of product before?",
		  "3. Oh, ok. Simply tell you about the fact that the fund we raised this time will be invested in Nanfu Battery, a leading domestic alkaline battery company. I don’t know if you are interested?",
		  "4. Our project is an equity private equity fund. The term is 3+2 years, and the initial investment amount is 1 million. In the future, it will be obtained through the independent listing of Nanfu or being acquired by M&A. Our project is a private equity fund. The term is 3+2 years, and the initial investment amount is 1 million. In the future, it will be obtained through the independent listing of Nanfu or by merger and acquisition.",
		  "5. After the product expires, if the Nanfu battery is not successfully listed, the owners of the repurchased Fang Yafeng Group and Fangding Investment will provide an annual repurchase of 8%. They also have the ability to buy back.",
		  "6. Our project is 3+2 years combo. If Nanfu fails to go public before the end of 2020, it will repurchase at 10% annualized income. If Nanfu is successfully listed before 2020, there will be a two-year capital withdrawal period, and the principal and income will be settled after exit.",
		  "7. Equity projects are not promised, mainly depending on the appreciation of investment projects. The valuation we entered this time is relatively low. As a stable growth industry leader, the future of Nanfu is still worth looking forward to.",
	      "8. Our project has a starting amount of 1 million yuan and a subscription fee of 2%. This threshold is very low compared to other equity projects.",
	      "9. The manager of our contractual fund level is Shanghai Zhichen Management Co., Ltd.",
		  "10. The reason why I introduce this project to you is that there are many investment opportunities, but good projects are rare. This is our star project this year, the recruitment time is short, I hope you have the opportunity to understand",
		  "11. Excuse me, the signal was not very good, can you say it again?",
	      "12. My phone number is 888-888-8888. Welcome to consult. If there is anything, I will provide you with services. Do you have any questions?",
		  "13. Then, will I call you later, when is it convenient?",
		  "14. Ok, we will call you again, thank you for your cooperation, goodbye.",
		  "15. I am sorry to bother you, I wish you a happy life, goodbye.",
		  "16. Ok, then there will be a voice version of the product interpretation sent to your phone, you can understand the product details when you have time. If you have more questions after listening, you can call us. I am sorry to bother you, I wish you a happy life, thank you",
		  "17. Sorry, your question may require a more professional person to answer. I will send the voice version of the product brief to your mobile phone later. You can listen to it when you have time. If you have more questions after listening, you can also consult your account manager or investment consultant. I wish you a happy life, goodbye.",
		  "18. Do you still want to know more about the project?",
		  "19. Hello. I am listening"]

status = 1
one = False
five = False
six = False
seven = False
eight = False
nine = False
result = ""

def gonext():
	if five is False:
		print(corpus[4])
		status = 5
	elif six is False:
		print(corpus[5])
		status = 6
	elif seven is False:
		print(corpus[6])
		status = 7
	elif eight is False:
		print(corpus[7])
		status = 8
	elif nine is False:
		print(corpus[8])
		status = 9
	else:
		print(corpus[16])
		status = 17

while True:
	if one is False:
		print(corpus[0])
		one = True

	line = sys.stdin.readline().strip()

	# no response, goto 18
	if line == "no response":
		print(corpus[17])

	return_results = classify(line)

	if len(return_results) > 1:
		print(corpus[status])
		status = status + 1

	if len(return_results) > 0:
		result = return_results[0][0]

	if result == "goodbye":
		break

	# first case
	if status == 1:
		if result == "notime":
			print(corpus[12])
			status = 13
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			print(corpus[status])
			status = status + 1

	# second case
	elif status == 2:
		if result == "positive":
			print(corpus[2])
			status = 3
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			print(corpus[status])
			status = status + 1

	# third case
	elif status == 3:
		if result == "negative":
			print(corpus[9])
			status = 10
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			print(corpus[status])
			status = status + 1

	# fourth case
	elif status == 4:
		if result == "safety":
			if five is False:
				print(corpus[4])
				status = 5
			else:
				print(corpus[16])
				status = 17
		elif result == "time":
			if six is False:
				print(corpus[5])
				status = 6
			else:
				print(corpus[16])
				status = 17
		elif result == "profit":
			if seven is False:
				print(corpus[6])
				status = 7
			else:
				print(corpus[16])
				status = 17
		elif result == "invest":
			if eight is False:
				print(corpus[7])
				status = 8
			else:
				print(corpus[16])
				status = 17
		elif result == "manager":
			if nine is False:
				print(corpus[8])
				status = 9
			else:
				print(corpus[16])
				status = 17
		elif result == "confuse":
				print(corpus[10])
				status = 11
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			print(corpus[status])
			status = status + 1

	# fifth case
	elif status == 5:
		five = True
		if result == "time":
			if six is False:
				print(corpus[5])
				status = 6
			else:
				print(corpus[16])
				status = 17
		elif result == "profit":
			if seven is False:
				print(corpus[6])
				status = 7
			else:
				print(corpus[16])
				status = 17
		elif result == "invest":
			if eight is False:
				print(corpus[7])
				status = 8
			else:
				print(corpus[16])
				status = 17
		elif result == "manager":
			if nine is False:
				print(corpus[8])
				status = 9
			else:
				print(corpus[16])
				status = 17
		elif result == "confuse":
				print(corpus[10])
				status = 11
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			if six is False:
				print(corpus[status])
				status = status + 1
			else:
				gonext()

	# sixth case
	elif status == 6:
		six = True
		if result == "safety":
			if five is False:
				print(corpus[4])
				status = 5
			else:
				print(corpus[16])
				status = 17
		elif result == "profit":
			if seven is False:
				print(corpus[6])
				status = 7
			else:
				print(corpus[16])
				status = 17
		elif result == "invest":
			if eight is False:
				print(corpus[7])
				status = 8
			else:
				print(corpus[16])
				status = 17
		elif result == "manager":
			if nine is False:
				print(corpus[8])
				status = 9
			else:
				print(corpus[16])
				status = 17
		elif result == "confuse":
				print(corpus[10])
				status = 11
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			if seven is False:
				print(corpus[status])
				status = status + 1
			else:
				gonext()

	# seventh case
	elif status == 7:
		seven = True
		if result == "safety":
			if five is False:
				print(corpus[4])
				status = 5
			else:
				print(corpus[16])
				status = 17
		elif result == "time":
			if six is False:
				print(corpus[5])
				status = 6
			else:
				print(corpus[16])
				status = 17
		elif result == "invest":
			if eight is False:
				print(corpus[7])
				status = 8
			else:
				print(corpus[16])
				status = 17
		elif result == "manager":
			if nine is False:
				print(corpus[8])
				status = 9
			else:
				print(corpus[16])
				status = 17
		elif result == "confuse":
				print(corpus[10])
				status = 11
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			if eight is False:
				print(corpus[status])
				status = status + 1
			else:
				gonext()

	# eighth case
	elif status == 8:
		eight = True
		if result == "safety":
			if five is False:
				print(corpus[4])
				status = 5
			else:
				print(corpus[16])
				status = 17
		elif result == "time":
			if six is False:
				print(corpus[5])
				status = 6
			else:
				print(corpus[16])
				status = 17
		elif result == "profit":
			if seven is False:
				print(corpus[6])
				status = 7
			else:
				print(corpus[16])
				status = 17
		elif result == "manager":
			if nine is False:
				print(corpus[8])
				status = 9
			else:
				print(corpus[16])
				status = 17
		elif result == "confuse":
				print(corpus[10])
				status = 11
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			if nine is False:
				print(corpus[status])
				status = status + 1
			else:
				gonext()

	# ninth case
	elif status == 9:
		nine = True
		if result == "safety":
			if five is False:
				print(corpus[4])
				status = 5
			else:
				print(corpus[16])
				status = 17
		elif result == "time":
			if six is False:
				print(corpus[5])
				status = 6
			else:
				print(corpus[16])
				status = 17
		elif result == "profit":
			if seven is False:
				print(corpus[6])
				status = 7
			else:
				print(corpus[16])
				status = 17
		elif result == "invest":
			if eight is False:
				print(corpus[7])
				status = 8
			else:
				print(corpus[16])
				status = 17
		elif result == "confuse":
				print(corpus[10])
				status = 11
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			print(corpus[status])
			status = status + 1

	# tenth case
	elif status == 10:
		if result == "safety":
			if five is False:
				print(corpus[4])
				status = 5
			else:
				print(corpus[16])
				status = 17
		elif result == "time":
			if six is False:
				print(corpus[5])
				status = 6
			else:
				print(corpus[16])
				status = 17
		elif result == "profit":
			if seven is False:
				print(corpus[6])
				status = 7
			else:
				print(corpus[16])
				status = 17
		elif result == "invest":
			if eight is False:
				print(corpus[7])
				status = 8
			else:
				print(corpus[16])
				status = 17
		elif result == "manager":
			if nine is False:
				print(corpus[8])
				status = 9
			else:
				print(corpus[16])
				status = 17
		elif result == "confuse":
				print(corpus[10])
				status = 11
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			print(corpus[status])
			status = status + 1
	# eleventh case
	elif status == 11:
		if result == "safety":
			if five is False:
				print(corpus[4])
				status = 5
			else:
				print(corpus[16])
				status = 17
		elif result == "time":
			if six is False:
				print(corpus[5])
				status = 6
			else:
				print(corpus[16])
				status = 17
		elif result == "profit":
			if seven is False:
				print(corpus[6])
				status = 7
			else:
				print(corpus[16])
				status = 17
		elif result == "invest":
			if eight is False:
				print(corpus[7])
				status = 8
			else:
				print(corpus[16])
				status = 17
		elif result == "manager":
			if nine is False:
				print(corpus[8])
				status = 9
			else:
				print(corpus[16])
				status = 17
		elif result == "confuse":
				print(corpus[16])
				status = 17
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			print(corpus[status])
			status = status + 1

	# twelveth case
	elif status == 12:
		if result == "safety":
			if five is False:
				print(corpus[4])
				status = 5
			else:
				print(corpus[16])
				status = 17
		elif result == "time":
			if six is False:
				print(corpus[5])
				status = 6
			else:
				print(corpus[16])
				status = 17
		elif result == "profit":
			if seven is False:
				print(corpus[6])
				status = 7
			else:
				print(corpus[16])
				status = 17
		elif result == "invest":
			if eight is False:
				print(corpus[7])
				status = 8
			else:
				print(corpus[16])
				status = 17
		elif result == "manager":
			if nine is False:
				print(corpus[8])
				status = 9
			else:
				print(corpus[16])
				status = 17
		elif result == "confuse":
				print(corpus[10])
				status = 11
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			print(corpus[status])
			status = status + 1
	# thirteenth case
	elif status == 13:
		if result == "positive":
			print(corpus[13])
			status = 14
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			print(corpus[14])
			status = 15

	# fourteenth case
	elif status == 14:
		break
	# fifteenth case
	elif status == 15:
		break
	# sixteenth case
	elif status == 16:
		break
	# seventeenth case
	elif status == 17:
		break
	# eighteenth case
	elif status == 18:
		if result == "negative":
			print(corpus[15])
			status = 16
		if result == "safety":
			if five is False:
				print(corpus[4])
				status = 5
			else:
				print(corpus[16])
				status = 17
		elif result == "time":
			if six is False:
				print(corpus[5])
				status = 6
			else:
				print(corpus[16])
				status = 17
		elif result == "profit":
			if seven is False:
				print(corpus[6])
				status = 7
			else:
				print(corpus[16])
				status = 17
		elif result == "invest":
			if eight is False:
				print(corpus[7])
				status = 8
			else:
				print(corpus[16])
				status = 17
		elif result == "manager":
			if nine is False:
				print(corpus[8])
				status = 9
			else:
				print(corpus[16])
				status = 17
		elif result == "confuse":
				print(corpus[10])
				status = 11
		elif result == "harass":
			print(corpus[11])
			status = 12
		else:
			print(corpus[status])
			status = status + 1






