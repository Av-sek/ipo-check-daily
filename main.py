import requests
import time
import os 
from dotenv import load_dotenv

load_dotenv(override=True)

def get_users():
    return os.getenv('USERS').split(',')

def get_listed_ipos(ipos):
    listed_ipos = []
    for ipo in ipos:
        if ipo.get('shareType') == 'ordinary' and ipo.get('status') and ipo.get('status').lower() == 'open':
            listed_ipos.append(ipo)
    return listed_ipos

def prepare_message(ipo):
    return f"""
    🚀✨ <b style="color:blue;"> IPO ALERT! 🚀✨</b>

    📢 <b>{ipo['companyName']} ({ipo['stockSymbol']})</b> is launching its IPO! 🏢📈

    📅 <b>Opening Date:</b> {ipo['openingDateAD']} (AD) | {ipo['openingDateBS']} (BS)  
    ⏳ <b>Closing Date:</b> {ipo['closingDateAD']} (AD) | {ipo['closingDateBS']} (BS)  
    ⏰ <b>Closing Time:</b> {ipo['closingDateClosingTime']}  

    💰 <b>Price Per Unit:</b> <i>NPR {ipo['pricePerUnit']}</i>  
    📊 <b>Total Units Available:</b> {ipo['units']}  
    🔢 <b>Min/Max Units:</b> {ipo['minUnits']} | {ipo['maxUnits']}  
    💵 <b>Total Amount:</b> <i>NPR {ipo['totalAmount']}</i>

    🏦 <b>Sector:</b> {ipo['sectorName']}  
    📜 <b>Share Registrar:</b> {ipo['shareRegistrar']}
    """





def send_notification_to_telegram(chat_id,message):
    token = os.getenv('TELEGRAM_TOKEN')
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=html"
    process_http_request(url, 'POST')

def process_http_request(url, method):
    try:
        if method.upper() == 'GET':
            response = requests.get(url)
        elif method.upper() == 'POST':
            response = requests.post(url)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making HTTP request: {e}")
        return None


def send_ipo_notification_to_users(ipos):
    users = get_users()
    listed_ipos = get_listed_ipos(ipos)
    for user in users:
        for ipo in listed_ipos:
            message = prepare_message(ipo)
            send_notification_to_telegram(user, message)

def get_ipos_lising():
    current_timestamp = int(time.time() * 1000)
    url = os.getenv('IPO_URL').format(current_timestamp=current_timestamp)
    response = process_http_request(url, 'GET')
    send_ipo_notification_to_users(response.get('result').get('data'))


def main():
    get_ipos_lising()


if __name__ == "__main__":
    main()
