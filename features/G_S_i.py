import threading
import requests
import psutil
print("G_S_I.py = True")
try:
    import GPUtil
except ImportError:
    GPUtil = None

_saved_ip = "Scanning..."

def _fetch_ip_in_background():
    """این تابع در پس‌زمینه اجرا شده و سرعت سیستم را قفل نمی‌کند"""
    global _saved_ip
    try:
        _saved_ip = requests.get("https://api.ipify.org", timeout=3).text
    except Exception:
        _saved_ip = "OFFLINE / ERROR"

threading.Thread(target=_fetch_ip_in_background, daemon=True).start()

def get_SI():    
    try:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        
        gpu = 0
        if GPUtil:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = int(gpus[0].load * 100)
            except Exception:
                gpu = 0
            
        system_data = {
            "cpu": cpu,
            "ram": ram,
            "disk": disk,
            "gpu": gpu,
            "ip": _saved_ip  
        }
        return system_data
        
    except Exception as e:
        print(f"Error in get_SI module: {e}")
        return None