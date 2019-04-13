import requests
import json
from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Filters, BaseFilter)
import telegram
import logging
updater = Updater(token="813385296:AAH4kIGBkYKuJCZ_yX5wRuYsd0sw0X9SWP8")
bot = telegram.Bot(token="813385296:AAH4kIGBkYKuJCZ_yX5wRuYsd0sw0X9SWP8")
dispatcher = updater.dispatcher
satoshi = 0.00000001
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


class Filter_address(BaseFilter):
    def filter(self, message):
        return len(message.text) == 34 or len(message.text) == 42


class Filter_address_no(BaseFilter):
    def filter(self, message):
        return len(message.text) != 34, 42, 64


class Filter_tx(BaseFilter):
    def filter(self, message):
        return len(message.text) == 64


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="hello, stranger. ШУЕ ППШ. NASWAY А это командыЖ\n"
                     "/check_address\n"
                     "/check_transactions\n"
                     "/blockchainstatus\n"
                     "/price\n"
                     "/start (this message)\n"
                     "/buy_some\n"
                     "/pluses"
                     "\n"
                     "<b>If you add this bot in a chat group, do not give him permission to read the messages</b>\n"
                     "\n"
                     "If you have a problem with bot or you want send me your feedback, contact me @Mark_Chucerberc\n", parse_mode=telegram.ParseMode.HTML)


def pluses(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                    text="Если интересноБ то вот Плюсы:\n— Повышает настроение. Особенно перед закидыванием. Не знаю почему, возможно сказывается зависимость. Когда сидишь пол ночи за компом работая над очередным заказом, часто сильно напрягаешься, что-то не получается.\n" 
                     "— После работы над проектом когда напряженка в голове, насвай помогает убрать весь этот негатив. Особенно перед сном или после тренировки с гантелями.\n"
                     "— После накурки травой (или лучше хороших бошек, гашиша) усиляет эффект в три раза! Дает взрывной приход. Бывает даже сильно залипаешь. Правда только на пол часа. Но держать под губой не рекомендую больше пяти минут.\n"
                     "— Стимулирует абстрактное мышление. Во время прихода может вызывать необычный подъем эмоциональных переживаний. Особенно если слушаешь музыку в беспроводных наушниках сидя на диване. У меня вошло в привычку качать и слушать trance music и саундтреки из фильмов во время упарывания. Заметил за собой положительные изменения в восприятии мира. Сложно описать ту гамму чувств которые порой наполняют голову во время эффекта.:\n ")

def buy_some(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                    text="Диллер приходит каждый день в 23:00, сюда https://goo.gl/maps/WFnNuSGA5ew")

def check_address(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Send me the BitcoinCash address for check the balance")


def check_transactions(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Send me the transaction hash for check the informations in the transaction")


def addr(bot, update):
    addr = (update.message.text)
    link = "https://api.blockchair.com/bitcoin-cash/dashboards/address/"
    get_address = requests.get(link+addr)
    date = get_address.json()
    conv = date["data"][addr]["address"]["balance"]
    final = satoshi*float(conv)
    tbbch = str(final)
    tbusd = str(date["data"][addr]["address"]["balance_usd"])
    t = str(date["data"][addr]["address"]["transaction_count"])
    bot.send_message(chat_id=update.message.chat_id, text=f"<b>Total Balance BCH:</b> <code>{tbbch}</code>" + "\n"
                     f"<b>Total Balance USD:</b> <code>{tbusd}</code>" + "\n"
                     f"<b>Transactions:</b> <code>{t}</code>", parse_mode=telegram.ParseMode.HTML)


def tx(bot, update):
    tx = (update.message.text)
    link = "https://api.blockchair.com/bitcoin-cash/dashboards/transaction/"
    get_tx = requests.get(link+tx)
    date = get_tx.json()
    conv = date["data"][tx]["transaction"]["input_total"]
    final = satoshi*float(conv)
    conv_two = date["data"][tx]["transaction"]["output_total"]
    final_two = satoshi*float(conv_two)
    current_block = date["context"]["state"]
    init_block = date["data"][tx]["transaction"]["block_id"]
    conf = current_block - init_block
    tivbch = str(final)
    tivusd = str(date["data"][tx]["transaction"]["input_total_usd"])
    tovbch = str(final_two)
    tovusd = str(date["data"][tx]["transaction"]["output_total_usd"])
    sb = str(date["data"][tx]["transaction"]["size"])
    confi = str(conf)
    fees = str(date["data"][tx]["transaction"]["fee"])
    coinb = str(date["data"][tx]["transaction"]["is_coinbase"])
    bot.send_message(chat_id=update.message.chat_id, text=f"<b>Total Input Value BCH:</b> <code>{tivbch}</code>" + "\n"
                     f"<b>Total Input Value USD:</b> <code>{tivusd}</code>" + "\n"
                     f"<b>Total Output Value BCH:</b> <code>{tovbch}</code>" + "\n"
                     f"<b>Total Output Valie USD:</b> <code>{tovusd}</code>" + "\n"
                     f"<b>Size (byte):</b> <code>{sb}</code>" + "\n"
                     f"<b>Confirmations:</b> <code>{confi}</code>" + "\n"
                     f"<b>Fees:</b> <code>{fees} satoshi</code>" + "\n"
                     f"<b>Coinbase:</b> <code>{coinb}</code>", parse_mode=telegram.ParseMode.HTML)


def blockchainstatus(bot, update):
    status = "https://api.blockchair.com/bitcoin-cash/stats"
    status_get = requests.get(status)
    date = status_get.json()
    cs1 = date["data"]["circulation"]
    cs2 = round(satoshi*float(cs1), 2)
    b = str(date["data"]["blocks"])
    bh = str(date["data"]["blocks_24h"])
    th = str("{:,}".format(date["data"]["transactions_24h"]))
    md = str("{:,}".format(date["data"]["difficulty"]))
    hr = str(date["data"]["hashrate_24h"])
    t = str("{:,}".format(date["data"]["transactions"]))
    o = str("{:,}".format(date["data"]["outputs"]))
    mt = str(date["data"]["mempool_transactions"])
    tfimusd = str(date["data"]["mempool_total_fee_usd"])
    tpsm = str(round(date["data"]["mempool_tps"], 2))
    cn = str("{:,}".format(date["data"]["nodes"]))
    cs = str("{:,}".format(cs2))
    bot.send_message(chat_id=update.message.chat_id, text=f"<b>Blocks:</b> <code>{b}</code>" + "\n"
                     f"<b>Blocks in 24h:</b> <code>{bh}</code>" + "\n"
                     f"<b>Transactions in 24h:</b> <code>{th}</code>" + "\n"
                     f"<b>Mining Difficulty:</b> <code>{md}</code>" + "\n"
                     f"<b>Hashrate 24h:</b> <code>{hr}</code>" + "\n"
                     f"<b>Transactions:</b> <code>{t}</code>" + "\n"
                     f"<b>Outputs:</b> <code>{o}</code>" + "\n"
                     f"<b>Mempool transactions:</b> <code>{mt}</code>" + "\n"
                     f"<b>Total fees in mempool (USD):</b> <code>{tfimusd}</code>" + "\n"
                     f"<b>Transactions per second in mempool:</b> <code>{tpsm}</code>" + "\n"
                     f"<b>Currently nodes:</b> <code>{cn}</code>" + "\n"
                     f"<b>Circulation supply:</b> <code>{cs}/21,000,000</code>", parse_mode=telegram.ParseMode.HTML)


def price(bot, update):
    link = "https://api.blockchair.com/bitcoin-cash/stats"
    link_get = requests.get(link)
    date = link_get.json()
    p = str(round(date["data"]["market_price_usd"], 2))
    vh = str("{:,}".format(date["data"]["volume_24h"]))
    pch = str(round(date["data"]["market_price_usd_change_24h_percentage"], 2))
    mcusd = str("{:,}".format(date["data"]["market_cap_usd"]))
    qu = str(date["data"]["market_dominance_percentage"])
    bot.send_message(chat_id=update.message.chat_id, text=f"<b>Price USD:</b> <code>{p}</code>" + "\n"
                     f"<b>Volume 24h:</b> <code>{vh}</code>" + "\n"
                     f"<b>Percent change 24h:</b> <code>{pch}%</code>" + "\n"
                     f"<b>Market cap USD:</b> <code>{mcusd}</code>" + "\n"
                     f"<b>Market Dominance: </b> <code>{qu}%</code>", parse_mode=telegram.ParseMode.HTML)


def addrno(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This is not a valid format of BitcoinCash address or a transaction hash, check if it's correct.\n"
                     "If your address starts with \"bitcoincash:\", remove it.")


if __name__ == "__main__":
    filter_address = Filter_address()
    filter_tx = Filter_tx()
    filter_address_no = Filter_address_no()
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(
        CommandHandler("check_address", check_address))
    updater.dispatcher.add_handler(CommandHandler(
        "check_transactions", check_transactions))
    updater.dispatcher.add_handler(MessageHandler(filter_address, addr))

    updater.dispatcher.add_handler(MessageHandler(filter_tx, tx))
    updater.dispatcher.add_handler(CommandHandler(
        "blockchainstatus", blockchainstatus))
    updater.dispatcher.add_handler(CommandHandler("price", price))
    updater.dispatcher.add_handler(CommandHandler("pluses", pluses))
    updater.dispatcher.add_handler(CommandHandler("buy_some", buy_some))
    updater.dispatcher.add_handler(MessageHandler(filter_address_no, addrno))

    updater.start_polling()
    updater.idle()
