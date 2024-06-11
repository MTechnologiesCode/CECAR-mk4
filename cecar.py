from speak import speak
from listen import listen
from utils import get_time, get_date, get_weather, get_wikipedia_summary
from datautils import save_data, load_data, calculate
from msgutils import send_whatsapp_message
from ard import send_arduino_command
import spacy
import os
import json
import time

colourlist = ["red", "blue", "green"]


time.sleep(3)

nlp = spacy.load("en_core_web_sm")


def greet():
    speak("Hello sir, how can I assist you today?")

def shutdown():
    speak("Shutting down. Goodbye!")

def process_command(command):
    doc = nlp(command)
    if any(token.lemma_ in ["time", "clock"] for token in doc):
        return "time"
    if any(token.lemma_ in ["unlock"] for token in doc):
        return "unlock"
    if any(token.lemma_ in ["lock"] for token in doc):
        return "lock"
    if any(token.lemma_ in ["light", "color", "red", "green", "blue", "change color"] for token in doc):
        if any(token.lemma_ in ["on"] for token in doc):
            return "led on"
        elif any(token.lemma_ in ["off"] for token in doc):
            return "led off"
        if any(token.lemma_ in ["red", "blue", "color", "green", "change color"] for token in doc):
            return "change colour"
    elif any(token.lemma_ in ["date", "day"] for token in doc):
        return "date"
    elif any(token.lemma_ in ["weather", "forecast"] for token in doc):
        for ent in doc.ents:
            if ent.label_ == "GPE":
                return ("weather", ent.text)
        return "ask_city"
    elif any(token.lemma_ in ["data", "save", "retrieve", "load"] for token in doc):
        if any(token.lemma_ in ["save"] for token in doc):
            return "save"
        elif any(token.lemma_ in ["retrieve", "load"] for token in doc):
            return "load"
    elif any(token.lemma_ in ["+", "-", "/", "*"] for token in doc):
        return "math"
    elif any(token.lemma_ in ["what", "search"] for token in doc):
        return "wiki"
    elif any(token.lemma_ in ["send", "message", "text"] for token in doc):
        return "msg"
    elif any(token.lemma_ in ["stop", "shutdown", "turn off" "off"] for token in doc):
        return "shutdown"
    else:
        return "unknown"

def main():
    greet()
    while True:
        command = listen()
        if command is None: #keeps listening till commanded
            continue
        intent = process_command(command) #processes verbal input
        
        #util functions
        if intent == "time": 
            speak(f"The current time is {get_time()}")
        elif intent == "date":
            speak(f"Today's date is {get_date()}")
        elif intent == "ask_city":
            speak("Which city?")
            city = listen()
            if city:
                weather_info = get_weather(city)
                speak(weather_info)
            elif isinstance(intent, tuple) and intent[0] == "weather":
                city = intent[1]
                weather_info = get_weather(city)
                speak(weather_info)
        elif intent == "wiki":
            if ("what is " not in command) and ("search for" not in command):
                speak("what should I search for?")
                search = listen()
            else:
                if ("what is " in command):
                    search = command[command.index("what is ")+7:]
                else:
                    search = command[command.index("search for ")+10:]
            speak(get_wikipedia_summary(search))

        #data util functions
        elif intent == "save":
            speak("which file")
            filename = listen()
            speak("What do you want me to save")
            datatype = listen()
            speak("What " + str(datatype) + "do you want me to save?")
            datavalue = listen()
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    data = json.load(file)
                data[datatype] = datavalue
                save_data(data, filename)
            else:
                datatemp = {}
                datatemp[datatype] = datavalue
                save_data(datatemp, filename)
            speak("Data saved successfully.")
        elif intent == "load":
            speak("which file")
            filename = listen()
            speak(load_data(filename))
        
        elif intent == "math":
            if "what is " not in command:
                speak(str(calculate(command)))
            else:
                speak(str(calculate(command[8:])))

        #msg util functions
        elif intent == "msg":
            parts = command.split(" ")
            to_index = parts.index("to")
            phone_number = parts[to_index + 1]
            if not phone_number.isdigit() and not phone_number.startswith('+'):
                with open('contacts', 'r') as file:
                    contacts = json.load(file)
                if phone_number in contacts:
                    phone_number = contacts[phone_number]
            message = " ".join(parts[to_index + 2:])
            send_whatsapp_message(phone_number, message)
            
        #arduino util functions
        elif intent == "unlock":
            response = send_arduino_command("unlock")
            speak(response)
        elif intent == "lock":
            response = send_arduino_command("lock")
            speak(response)
        elif intent == "change colour":
            if "to" in command:
                rest = command[command.index("to ")+3:]
                parts = rest.split(" ")
                if parts[0] in colourlist:
                    colour = parts[0]
                else:
                    speak("what color")
                    colour = listen()
            else:
                speak("what color")
                colour = listen()
            response = send_arduino_command(colour)
            speak(response)
        elif "set color value" in command:
            # Extract RGB values from the command
            try:
                parts = command.split("set color value")[1].strip().split()
                r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
                response = send_arduino_command(f"color {r} {g} {b}")
                speak(response)
            except ValueError:
                speak("I couldn't understand the RGB values. Please try again.")
        elif intent == "led on":
            response = send_arduino_command("led on")
            speak(response)
        elif intent == "led off":
            response = send_arduino_command("led off")
            speak(response)

        #shutdown function
        elif intent == "shutdown":
            shutdown()
            break

        #if no function
        else:
            speak("Sorry, I cannot help with that yet.")

if __name__ == "__main__":
    main()