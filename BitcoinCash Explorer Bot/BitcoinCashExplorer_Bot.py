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
    "If you add this bot in a chat group, do not give him permission to read the messages\n"
    "\n"
    "Other command:\n"
    "/donations\n"
    "My website: domestic.pythonanywhere.com\n"
    "If you have a problem with bot or you want send me your feedback, contact me @domestic2citsemod")
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
    bot.send_message(chat_id=update.message.chat_id, text="<b>Total Balance BCH: </b>" + str(final) + "\n"
    "<b>Total Balance USD: </b>" + str(date["data"][0]["sum_value_unspent_usd"]), parse_mode=telegram.ParseMode.HTML)
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
    bot.send_message(chat_id=update.message.chat_id, text="<b>Total Balance BCH: </b>" + str(final) + "\n"
    "<b>Total Balance USD: </b>" + str(date["data"][0]["sum_value_unspent_usd"]), parse_mode=telegram.ParseMode.HTML)
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
    bot.send_message(chat_id=update.message.chat_id, text="<b>Total Input Value: </b>" + str(dates["valueIn"]) + " " + "<b>BCH</b>" + "\n"
    "<b>Total Output Value: </b>" + str(dates["valueOut"]) + "  " + "<b>BCH</b>" + "\n"
    "<b>Size (byte): </b>" + str(dates["size"]) + "\n"
    "<b>Confirmations: </b>" + str(dates[("confirmations")]) + "\n"
    "<b>Fees: </b>" + str(dumb["data"]["fee"]) + " " + "<b>satoshi</b>" + "\n"
    "<b>Coinbase: </b>" + str(dates["isCoinBase"]), parse_mode=telegram.ParseMode.HTML)
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
    bot.send_message(chat_id=update.message.chat_id, text="<b>Estimate fee for confirmations in 1 block: </b>" + str(date_one["1"]) + " " + "<b>BCH</b>" + "\n" 
                     "<b>Estimate fee for confirmations in 3 blocks: </b>" + str(date_three["3"]) + " " + "<b>BCH</b>" + "\n" 
                     "<b>Estimate fee for confirmations in 6+ blocks: </b>" + str(date_six["6"]) + " " + "<b>BCH</b>", parse_mode=telegram.ParseMode.HTML)
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
    bot.send_message(chat_id=update.message.chat_id, text="<b>Blocks: </b>" + str(date["info"]["blocks"]) + "\n" "<b>Mining Difficulty: </b>" + str(date["info"]["difficulty"]) + "\n" "<b>Transactions: </b>" + mem_tx + "\n" "<b>Mempool transactions: </b>" + mem_t + "\n" "<b>Total fees in mempool (USD): </b>" + mem_usd + "\n" "<b>Transactions per second in mempool: </b>" + mem_tps + "\n" "<b>Currently nodes: </b>" + mem_n,
    parse_mode=telegram.ParseMode.HTML)
status_handler=CommandHandler("blockchain_status", blockchain_status)
dispatcher.add_handler(status_handler)

def price(bot, update):
    link="https://api.coinmarketcap.com/v2/ticker/1831/"
    link_get=requests.get(link)
    date=link_get.json()
    bot.send_message(chat_id=update.message.chat_id, text="<b>Price: </b>" + str(date["data"]["quotes"]["USD"]["price"]) + " " + "<b>USD</b>" + "\n" "<b>Volume 24h: </b>" + str(date["data"]["quotes"]["USD"]["volume_24h"]) + "\n" "<b>Percent change 24h: </b>" + str(date["data"]["quotes"]["USD"]["percent_change_24h"]) + "%",
    parse_mode=telegram.ParseMode.HTML)
price_handler=CommandHandler("price", price)
dispatcher.add_handler(price_handler)

def supply(bot, update):
    link="https://api.coinmarketcap.com/v2/ticker/1831/"
    link_get=requests.get(link)
    date=link_get.json()
    bot.send_message(chat_id=update.message.chat_id, text="<b>Circulating supply: </b>" + str(date["data"]["circulating_supply"]) + "\n" "<b>Max supply: </b>" + str(date["data"]["max_supply"]), parse_mode=telegram.ParseMode.HTML)
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
