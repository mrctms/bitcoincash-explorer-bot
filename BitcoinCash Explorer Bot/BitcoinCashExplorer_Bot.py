import requests
import json
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, BaseFilter)
import telegram
import logging
updater = Updater(token='')
bot=telegram.Bot(token="")
dispatcher=updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.DEBUG)




def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello, there is a bot for the BitcoinCash Blockchain Explorer. You can use these command:\n"
    "/check_address\n"
    "/check_transactions\n"
    "/estimate_fee\n"
    "/blockchain_status\n"
    "/supply\n"
    "/price\n"
    "/start (this message)\n"
    "\n"
    "Other command:\n"
    "/donations\n"
    "My website: domestic.pythonanywhere.com")
start_handler=CommandHandler("start", start)
dispatcher.add_handler(start_handler)


def check_address(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Send me the BitcoinCash address for check the balance")

check_a_handler=CommandHandler("check_address", check_address)
dispatcher.add_handler(check_a_handler)

def check_transactions(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Send me the transaction hash for check the informations in the transaction")
    update.message.forward(chat_id_group)
check_t_handler=CommandHandler("check_transactions", check_transactions)
dispatcher.add_handler(check_t_handler)


def donations(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="If you appreciate the bot, consider making a small donation to keep the development active. It will be greatly appreciated.\n"
    "bitcoincash:qqykq7adrqssm2e2gmz6ln440tup2qxuhqndwwlqfj")
don_handler=CommandHandler("donations", donations)
dispatcher.add_handler(don_handler)


class Filter_address_two(BaseFilter):
    def filter(self, message):
        return len(message.text) == 42
filter_address_two= Filter_address_two()
def addrtwo(bot,update):
    address=(update.message.text)
    link="https://api.blockchair.com/bitcoin-cash/dashboards/address/"
    get_address=requests.get(link+address)
    date=get_address.json()
    satoshi=0.00000001
    conv=date["data"][0]["sum_value_unspent"]
    final=satoshi*float(conv)
    bot.send_message(chat_id=update.message.chat_id, text="Total Balance BCH: " + str(final) + "\n"
    "Total Balance USD: " + str(date["data"][0]["sum_value_unspent_usd"]))
addrtwo_handler=MessageHandler(filter_address_two, addrtwo)
dispatcher.add_handler(addrtwo_handler)

class Filter_address(BaseFilter):
    def filter(self, message):
        return len(message.text) == 34
filter_address= Filter_address()
def addr(bot,update):
    address=(update.message.text)
    link="https://api.blockchair.com/bitcoin-cash/dashboards/address/"
    get_address=requests.get(link+address)
    date=get_address.json()
    satoshi=0.00000001
    conv=date["data"][0]["sum_value_unspent"]
    final=satoshi*float(conv)
    bot.send_message(chat_id=update.message.chat_id, text="Total Balance BCH: " + str(final) + "\n"
    "Total Balance USD: " + str(date["data"][0]["sum_value_unspent_usd"]))
addr_handler=MessageHandler(filter_address, addr)
dispatcher.add_handler(addr_handler)

class Filter_tx(BaseFilter):
    def filter(self, message):
        return len(message.text) == 64
filter_tx=Filter_tx()
def tx(bot, update):
    txtwo=(update.message.text)
    txone=(update.message.text)
    linktwo="https://www.blockdozer.com/api/tx/"
    linkone="https://bch-chain.api.btc.com/v3/tx/"
    get_tx_one=requests.get(linkone+txone)
    date=get_tx_one.json()
    get_tx_two=requests.get(linktwo+txtwo)
    dates=get_tx_two.json()
    bot.send_message(chat_id=update.message.chat_id, text="Total Input Value: " + str(dates["valueIn"]) + "\n"
    "Total Output Value: " + str(dates["valueOut"]) + "\n"
    "Size (byte): " + str(dates["size"]) + "\n"
    "Confirmations: " + str(dates[("confirmations")]) + "\n"
    "Fees: " + str(date["data"]["fee"]) + " " + "satoshi" + "\n"
    "Coinbase: " + str(dates["isCoinBase"]))
tx_handler=MessageHandler(filter_tx, tx)
dispatcher.add_handler(tx_handler)



def estimate_fee(bot, update):
    estimate_one="https://www.blockdozer.com/api/utils/estimatefee?nbBlocks=1"
    estimate_one_get=requests.get(estimate_one)
    date_one=estimate_one_get.json()
    estimate_three="https://www.blockdozer.com/api/utils/estimatefee?nbBlocks=3"
    estimate_three_get=requests.get(estimate_three)
    date_three=estimate_three_get.json()
    estimate_six="https://www.blockdozer.com/api/utils/estimatefee?nbBlocks=6"
    estimate_six_get=requests.get(estimate_six)
    date_six=estimate_six_get.json()
    bot.send_message(chat_id=update.message.chat_id, text="Estimate fee for confirmations in 1 block: " + str(date_one["1"]) + " " + "BCH" + "\n" "Estimate fee for confirmations in 3 blocks: " + str(date_three["3"]) + " " + "BCH" + "\n" "Estimate fee for confirmations in 6+ blocks: " + str(date_six["6"]) + " " + "BCH")
fee_handler=CommandHandler("estimate_fee", estimate_fee)
dispatcher.add_handler(fee_handler)

def blockchain_status(bot, update):
    status="https://www.blockdozer.com/api/status"
    status_get=requests.get(status)
    date=status_get.json()
    mem="https://api.blockchair.com/bitcoin-cash/mempool"
    mem_get=requests.get(mem)
    dates=mem_get.json()
    for t in dates["data"]:
        if t["e"] == "mempool_transactions":
            mem_t = str(t["c"])
    for t in dates["data"]:
        if t["e"] == "mempool_total_fee_usd":
            mem_usd = str(t["c"])
    for t in dates["data"]:
        if t["e"] == "mempool_tps":
            mem_tps = str(t["c"])
    for t in dates["data"]:
        if t["e"] == "nodes":
            mem_n = str(t["c"])
    for t in dates["data"]:
        if t["e"] == "transactions":
            mem_tx = str(t["c"])
    bot.send_message(chat_id=update.message.chat_id, text="Blocks: " + str(date["info"]["blocks"]) + "\n" "Mining Difficulty: " + str(date["info"]["difficulty"]) + "\n" "Transactions: " + mem_tx + "\n" "Mempool transactions: " + mem_t + "\n" "Total fees in mempool (USD): " + mem_usd + "\n" "Transactions per second in mempool: " + mem_tps + "\n" "Currently nodes: " + mem_n)
status_handler=CommandHandler("blockchain_status", blockchain_status)
dispatcher.add_handler(status_handler)

def price(bot, update):
    link="https://api.coinmarketcap.com/v2/ticker/1831/"
    link_get=requests.get(link)
    date=link_get.json()
    bot.send_message(chat_id=update.message.chat_id, text="Price: " + str(date["data"]["quotes"]["USD"]["price"]) + " " + "USD" + "\n" "Volume 24h: " + str(date["data"]["quotes"]["USD"]["volume_24h"]) + "\n" "Percent change 24h: " + str(date["data"]["quotes"]["USD"]["percent_change_24h"]) + "%")
price_handler=CommandHandler("price", price)
dispatcher.add_handler(price_handler)

def supply(bot, update):
    link="https://api.coinmarketcap.com/v2/ticker/1831/"
    link_get=requests.get(link)
    date=link_get.json()
    bot.send_message(chat_id=update.message.chat_id, text="Circulating supply: " + str(date["data"]["circulating_supply"]) + "\n" "Max supply: " + str(date["data"]["max_supply"]))
supply_handler=CommandHandler("supply", supply)
dispatcher.add_handler(supply_handler)


#error section

class Filter_address_no(BaseFilter):
    def filter(self, message):
        return len(message.text) <= 33
filter_address_no=Filter_address_no()
def addrno(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This is not a valid format of BitcoinCash address, check if it is correct.")
no_handler=MessageHandler(filter_address_no, addrno)
dispatcher.add_handler(no_handler)

class Filter_address_no_two(BaseFilter):
    def filter(self, message):
        return len(message.text) == 54
filter_address_no_due=Filter_address_no_two()
def addrnotwo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This is not a valid format of BitcoinCash address, if you put \"bitcoincash:\", remove it.")
no_two_handler=MessageHandler(filter_address_no_two, addrnotwo)
dispatcher.add_handler(no_two_handler)

class Filter_tx_no(BaseFilter):
    def filter(self, message):
        return len(message.text) > 64
filter_tx_no=Filter_tx_no()
def txno(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This hash is not valid, check if it is correct.")
no_tx_handler=MessageHandler(filter_tx_no, txno)
dispatcher.add_handler(no_tx_handler)






updater.start_polling()
updater.idle()
