import requests
import json
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, BaseFilter)
import telegram
import logging
updater = Updater(token="")
bot=telegram.Bot(token="")
dispatcher=updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)




def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello, there is a bot for the BitcoinCash Blockchain Explorer. You can use these command:\n"
    "/check_address\n"
    "/check_transactions\n"
    "/blockchainstatus\n"
    "/price\n"
    "/start (this message)\n"
    "\n"
    "<b>If you add this bot in a chat group, do not give him permission to read the messages</b>\n"
    "\n"
    "If you have a problem with bot or you want send me your feedback, contact me @MarckTomack\n", parse_mode=telegram.ParseMode.HTML)
start_handler=CommandHandler("start", start)
dispatcher.add_handler(start_handler)


def check_address(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Send me the BitcoinCash address for check the balance")
check_a_handler=CommandHandler("check_address", check_address)
dispatcher.add_handler(check_a_handler)

def check_transactions(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Send me the transaction hash for check the informations in the transaction")
check_t_handler=CommandHandler("check_transactions", check_transactions)
dispatcher.add_handler(check_t_handler)


class Filter_address(BaseFilter):
    def filter(self, message):
        return len(message.text) == 34 or len(message.text) == 42
filter_address= Filter_address()
def addr(bot,update):
    addr=(update.message.text)
    link="https://api.blockchair.com/bitcoin-cash/dashboards/address/"
    get_address=requests.get(link+addr)
    date=get_address.json()
    satoshi=0.00000001
    conv=date["data"][addr]["address"]["balance"]
    final=satoshi*float(conv)
    bot.send_message(chat_id=update.message.chat_id, text="<b>Total Balance BCH: </b>" + str(final) + "\n"
    "<b>Total Balance USD: </b>" + str(date["data"][addr]["address"]["balance_usd"]) + "\n"
    "<b>Transactions: </b>" + str(date["data"][addr]["address"]["transaction_count"]), parse_mode=telegram.ParseMode.HTML)
addr_handler=MessageHandler(filter_address, addr)
dispatcher.add_handler(addr_handler)

class Filter_tx(BaseFilter):
    def filter(self, message):
        return len(message.text) == 64
filter_tx=Filter_tx()
def tx(bot, update):
    tx=(update.message.text)
    link="https://api.blockchair.com/bitcoin-cash/dashboards/transaction/"
    get_tx=requests.get(link+tx)
    date=get_tx.json()
    satoshi=0.00000001
    conv=date["data"][tx]["transaction"]["input_total"]
    final=satoshi*float(conv)
    conv_two=date["data"][tx]["transaction"]["output_total"]
    final_two=satoshi*float(conv_two)
    current_block=date["context"]["state"]
    init_block=date["data"][tx]["transaction"]["block_id"]
    conf=current_block-init_block
    bot.send_message(chat_id=update.message.chat_id, text="<b>Total Input Value BCH: </b>" + str(final) + "\n"
    "<b>Total Input Value USD: </b>" + str(date["data"][tx]["transaction"]["input_total_usd"]) + "\n"
    "<b>Total Output Value BCH: </b>" + str(final_two) + "\n"
    "<b>Total Output Valie USD: </b>" + str(date["data"][tx]["transaction"]["output_total_usd"]) + "\n"
    "<b>Size (byte): </b>" + str(date["data"][tx]["transaction"]["size"]) + "\n"
    "<b>Confirmations: </b>" + str(conf) + "\n"
    "<b>Fees: </b>" + str(date["data"][tx]["transaction"]["fee"]) + " " + "satoshi" "\n"
    "<b>Coinbase: </b>" + str(date["data"][tx]["transaction"]["is_coinbase"]), parse_mode=telegram.ParseMode.HTML)
tx_handler=MessageHandler(filter_tx, tx)
dispatcher.add_handler(tx_handler)




def blockchainstatus(bot, update):
    status="https://api.blockchair.com/bitcoin-cash/stats"
    status_get=requests.get(status)
    date=status_get.json()
    bot.send_message(chat_id=update.message.chat_id, text=
    "<b>Blocks: </b>" + str(date["data"]["blocks"]) + "\n"
    "<b>Blocks in 24h: </b>" + str(date["data"]["blocks_24h"]) + "\n"
    "<b>Transactions in 24h: </b>" + str("{:,}".format(date["data"]["transactions_24h"])) + "\n"
    "<b>Mining Difficulty: </b>" + str("{:,}".format(date["data"]["difficulty"])) + "\n"
    "<b>Hashrate 24h: </b>" + str(date["data"]["hashrate_24h"]) + "\n"
    "<b>Transactions: </b>" + str("{:,}".format(date["data"]["transactions"])) + "\n"
    "<b>Outputs: </b>" + str("{:,}".format(date["data"]["outputs"])) + "\n"
    "<b>Mempool transactions: </b>" + str(date["data"]["mempool_transactions"]) + "\n"
    "<b>Total fees in mempool (USD): </b>" + str(date["data"]["mempool_total_fee_usd"]) + "\n"
    "<b>Transactions per second in mempool: </b>" + str(round(date["data"]["mempool_tps"], 2)) + "\n"
    "<b>Currently nodes: </b>" + str("{:,}".format(date["data"]["nodes"])) + "\n"
    "<b>Circulation supply: </b>" + str("{:,}".format(date["data"]["circulation"])) + "/" + str("21,000,000"),
    parse_mode=telegram.ParseMode.HTML)
status_handler=CommandHandler("blockchainstatus", blockchainstatus)
dispatcher.add_handler(status_handler)

def price(bot, update):
    link="https://api.blockchair.com/bitcoin-cash/stats"
    link_get=requests.get(link)
    date=link_get.json()
    bot.send_message(chat_id=update.message.chat_id, text="<b>Price: </b>" + str(round(date["data"]["market_price_usd"], 2)) + " " + "USD" + "\n"
    "<b>Volume 24h: </b>" + str("{:,}".format(date["data"]["volume_24h"])) + "\n"
    "<b>Percent change 24h: </b>" + str(round(date["data"]["market_price_usd_change_24h_percentage"], 2)) + "%" + "\n"
    "<b>Market cap USD: </b>" + str("{:,}".format(date["data"]["market_cap_usd"])) + "\n"
    "<b>Market dominance: </b>" + str(date["data"]["market_dominance_percentage"]) + "%",
    parse_mode=telegram.ParseMode.HTML)
price_handler=CommandHandler("price", price)
dispatcher.add_handler(price_handler)



#Error section

class Filter_address_no(BaseFilter):
    def filter(self, message):
        return len(message.text) != 34, 42, 64
filter_address_no=Filter_address_no()
def addrno(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This is not a valid format of BitcoinCash address or a transaction hash, check if it's correct.\n"
                    "If your address starts with \"bitcoincash:\", remove it.")
no_handler=MessageHandler(filter_address_no, addrno)
dispatcher.add_handler(no_handler)



updater.start_polling()
updater.idle()
