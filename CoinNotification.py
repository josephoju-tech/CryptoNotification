# -*- coding: utf-8 -*-
"""
@author: Joseph Oju
ACE22140009

Created on Wed May 11 21:09:02 2022
This script sends notification alerts every 10mins if the price drop is below the given pricecheck
The price alert is sent to telegram bot

Create an account on https://pro.coinmarketcap.com/, generate your api key
Set up telegram app on your phone and use @BotFather to create a bot
The created bot comes with the bot token

Use @userinfobot to get the chat id

"""
#Importing all required libraries
import requests
import time


# global variables that are needed in all functions
api_key =   '***********'               # 'enter your_coinmarketcap_api_key'
bot_token = '***********'               #'enter your_telegram_bot_token'
chat_id =   '***********'               #'your_telegram_account_chat_id_here'
pricecheck = 30000
time_interval = 10 * 60 # in seconds
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'


def get_btc_price():
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key   #CoinMarket api key for json data
    }
    
    # sending request to pro coinmarketcap api
    response = requests.get(url, headers=headers)
    response_json = response.json()

    # this next line of code will extract the bitcoin price from the coinmarket data
    btc_price = response_json['data'][0]
    return btc_price['quote']['USD']['price']  #The bitcoin price are returned in USD

# fn to send_message through telegram
def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"

    # send the msg
    requests.get(url)


# main function
def main():
    price_list = []

    # This loop will be verifying price of crypto
    while True:
        price = get_btc_price()
        price_list.append(price)

        # if the price falls below threshold, send an immediate message
        if price < pricecheck:
            send_message(chat_id=chat_id, message=f'BTC Price Drop Alert: {price}')

        # send last 6 btc price
        if len(price_list) >= 6:
            send_message(chat_id=chat_id, message=price_list)
            # code that will empty the price list
            price_list = []

        # fetch the price for every dash minutes
        time.sleep(time_interval)

# The main() function that runs the script
if __name__ == '__main__':
    main()
