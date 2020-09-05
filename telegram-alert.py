import json, requests, time, conf
from boltiot import Bolt 

mybolt=Bolt(conf.API_KEY, conf.DEVICE_ID)

ERROR_CODE=-999

def getSensorValue(pin):
	"""Receives the sensor value. Returns ERROR_CODE if request fails"""
	try:		
			# storing sensor readings
		response=mybolt.analogRead(pin)
			# converting response to JSON format
		data=json.loads(response)
			# checking for successful request
		if(data["success"]!=1):
			print("\n\t The request was unsuccessful!")
			print("\n\t The response returned ->",data)
			return ERROR_CODE
			# return sensor readings
		else:
			sensor_value=int(data["value"])
			return sensor_value
	except Exception as e:
		print("\n\t Something went wrong while reading the sensor values! [Details below]")
		print(e)	
		return ERROR_CODE

def sendTelegramMessage(message):
	"""Sends alerts via telegram"""
		# building bot url
	url="https://api.telegram.org/"+conf.BOT_ID+"/sendMessage"
		# building channel data
	data={
		"chat_id":conf.CHAT_ID,
		"text":message
	}
	try:
			# making a HTTP "POST" request to Telegram servers	
		response=requests.request(
			"POST",
			url,
			params=data
			)
			# displaying request status
		print("\n\t The Telegram response is as follows : \n",response.text)
		telegram_data=json.loads(response.text)
		return telegram_data["ok"]
	except Exception as e:
		print("Something went wrong while sending alerts via Telegram! [Details below]")
		print(e)
		return False

if __name__=="__main__":
	while True:
			# getting sensor values
		sensor_value=getSensorValue("A0")
		reading=(100*sensor_value/1024)
			# checking whether sensor values are valid or not
		if(sensor_value==-999):
			print("\n\t Request was unsuccessful! Skipping!")
			time.sleep(10)
			continue
		print("\n\t The current temperature reading is : "+str(sensor_value)+\
		"("+str(reading)+" degrees Celcius")
			# sending Telegram alerts 
		if(sensor_value>conf.THRESHOLD):
			print("\n\t Temperature values have exceeded threshold!")
			message="Alert!!! Temperature value has exceeded threshold value of "+str(conf.THRESHOLD)+\
			"(29.29 degrees Celcius). The current temperature reading is "+str(reading)
			telegram_status=sendTelegramMessage(message)
			print("\n\t This is the status Telegram returned : ",telegram_status)
			# delaying for 10 seconds
		time.sleep(10)
