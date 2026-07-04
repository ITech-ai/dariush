from openai import OpenAI
from urllib.parse import urlparse
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from site_control import open_web
print("ai.py = True")
#________________________________________open_web_________________________
def is_website(text):
    try:
        result = urlparse(text)

        return all([result.scheme in ['http', 'https'], result.netloc])

    except:
        return False
    
#________________________________________ai_ansawer_______________________-
client = OpenAI(
    base_url="https://api.sambanova.ai/v1",
    api_key="d4bb6709-111e-4f24-9754-59303edb17f3"
)
def ask_ai(text):
    try:
        response = client.chat.completions.create(
            model="Meta-Llama-3.3-70B-Instruct",
            messages=[
                {
                    "role": "system", 
                    "content": "تو یک دستیار فوق‌العاده خلاصه هستی. فقط جواب نهایی را در کمتر از یک خط بده. اگر آدرس سایت خواستند فقط و فقط لینک مستقیم (URL) بده. اگر کلمات ورودی کاملاً بی‌معنی، تصادفی، نامفهوم یا نامشخص بود، فقط بنویس None."
                },
                {"role": "user", "content": text}
            ],
            temperature=0.1
        )
        massage = response.choices[0].message.content.strip()
        if is_website(massage) ==True:
            open_web(massage)
        else:
            return "Dariush : ",massage
    except:
        return "None"




