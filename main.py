import threading
import json
import webview
import os
import time
import sys
from listening import listen
from features.ai import ask_ai 
from speak import speak as original_speak
from features.G_S_i import get_SI
from features.Global_price import get_price
from features.temperature import get_weather
from features.daily_schedule import schudel__main
file_path = os.path.abspath("UI/main.html")

jarvis_window = None

class JarvisAPI:
    def process_text_input(self, text):
        threading.Thread(target=generate_ai_response, args=(text,), daemon=True).start()



def generate_ai_response(user_text):
    global jarvis_window
    if not user_text.strip():
        return

    ui_add_message(user_text, 'user')
    reply = ask_ai(user_text)
    ui_add_message(reply, 'jarvis')

# def dashboard_updater():
#     global jarvis_window
#     counter = 0
#     while True:
    
#         if jarvis_window:
#             try:
#                 if counter % 50 == 0:
#                     sys_info = get_SI()
#                     if sys_info:
#                         cpu = sys_info.get("cpu", 0)
#                         ram = sys_info.get("ram", 0)
#                         disk = sys_info.get("disk", 0)
#                         gpu = sys_info.get("gpu", 0)
#                         ip = sys_info.get("ip", "Scanning...")
#                         jarvis_window.evaluate_js(
#                             f"updateSystemStats('{cpu}', '{ram}', '{disk}', '{gpu}', '{ip}');"
#                         )
#                     weather_data = get_weather() 
           
#                     if weather_data:
#                         city = weather_data.get("city" , "---")
#                         temp = weather_data.get("temp" , "---")
#                         humidity = weather_data.get("humidity" , "---")
#                         condition = weather_data.get("condition" , "---")
#                         jarvis_window.evaluate_js(f"updateWeather('{city}', '{temp}', '{humidity}', '{condition}');")
#                     price_data = get_price() 
#                     if price_data:
#                         gold = price_data.get("gold", "---")
#                         coin = price_data.get("coin", "---")
#                         usd = price_data.get("dollar", "---")
#                         jarvis_window.evaluate_js(f"updatePrices('{usd}', '{coin}', '{gold}');")
#             except Exception as e:
#                 print(f"Dashboard Telemetry Error: {e}")
 
#             counter += 1




def ui_add_message(text, sender):
    global jarvis_window
    if jarvis_window:
        safe_text = json.dumps(text)[1:-1]
        jarvis_window.evaluate_js(f"addUserMessage('{safe_text}', '{sender}');")

def speak(text):
    global jarvis_window
    if jarvis_window:
        jarvis_window.evaluate_js("setSpeakingState(true);")
        ui_add_message(text, 'jarvis')
    original_speak(text)
    if jarvis_window:
        jarvis_window.evaluate_js("setSpeakingState(false);")
site_word=["سایت","باز" ]




def main():
    
    global jarvis_window 
    print("Voice system started...")
    loop = True
    speak("Hi sir, How can i help you today")
    while loop:
        sound = listen()
        if sound != None:
            print(sound)
            ui_add_message(sound , 'user')
            print(f"you said: {sound}")
            #________________________________________________finish___________________________________
            if sound == "خروج":
                speak("dariush will be shutdown")
                ui_add_message("خورج",'jarvis')
                loop =False
                time.sleep(3)
                jarvis_window.destroy()
            #______________________________________________Hello______________________________________
            elif "سلام" in sound:
                speak("HI sir ")
            #______________________________________________about_____________________________________
            elif "درباره" in sound:
                speak("Im dariush , an ai agent that will be help you to your work and days")
            #_____________________________________________open_Site__________________________________
            elif any(word in sound for word in site_word):
                speak("okay")
                generate_ai_response(sound)
            #_____________________________________________open_schudel________________________________
            if "برنامه روزانه" in sound:
                speak("ok Sir")
                
                schudel__main()
        time.sleep(0.05)

    
if __name__ == '__main__':
  
    api = JarvisAPI()
    jarvis_window = webview.create_window(
        title="Jarvis ", 
        url=f"file://{file_path}",
        js_api=api, 
        background_color="#000000",
        width=1000,
        height=700,
        fullscreen=True,
        resizable=True
    )
   
    threading.Thread(target=      main        , daemon=True).start()
    # threading.Thread(target=dashboard_updater , daemon=True).start()
    webview.start()