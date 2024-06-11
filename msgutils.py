import pywhatkit as kit
import datetime

#whatsapp
    
def send_whatsapp_message(phone_number, message):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute + 1
    print(hour)
    print(minute)
    kit.sendwhatmsg(phone_number, message, hour, minute)
    