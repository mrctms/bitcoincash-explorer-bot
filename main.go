/* Copyright (C) MarckTomack <marcktomack@tutanota.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>. */

package main

import (
	"fmt"
	"github.com/buger/jsonparser"
	tb "gopkg.in/tucnak/telebot.v2"
	"io/ioutil"
	"log"
	"math"
	"net/http"
	"strconv"
	"time"
)

const satoshi = 0.00000001

func logError(err error) {
	if err != nil {
		log.Println(err)
	}
}

func start(bot *tb.Bot) {
	bot.Handle("/start", func(m *tb.Message) {
		bot.Send(m.Sender, "This is a bot for the BitcoinCash Blockchain.\n"+
			"You can use these commands:\n"+"\n"+
			"/blockchainstatus\n"+
			"/price\n"+"\n"+
			"Or send an address or a transaction hash for check informations about it.")
	})
}

func addressAndTransaction(bot *tb.Bot) {
	bot.Handle(tb.OnText, func(m *tb.Message) {
		addr, tx := m.Text, m.Text

		if len(addr) == 34 || len(addr) == 42 || len(addr) == 54 {
			url := "https://api.blockchair.com/bitcoin-cash/dashboards/address/"
			getRequest, err := http.Get(url + addr)
			logError(err)
			readBody, err := ioutil.ReadAll(getRequest.Body)
			logError(err)
			json := []byte(readBody)
			parseBalanceBCH, err := jsonparser.GetFloat(json, "data", fmt.Sprintf(`%v`, addr), "address", "balance")
			logError(err)
			balanceBCH := parseBalanceBCH * satoshi
			roundBalanceBCH := math.Round(balanceBCH)
			balanceBCHToPrint := fmt.Sprintf("%.2f", roundBalanceBCH)
			balanceUSD, err := jsonparser.GetFloat(json, "data", fmt.Sprintf(`%v`, addr), "address", "balance_usd")
			logError(err)
			roundBalanceUSD := math.Round(balanceUSD)
			balanceUSDToPrint := fmt.Sprintf("%.2f", roundBalanceUSD)

			transactionCount, err := jsonparser.GetInt(json, "data", fmt.Sprintf(`%v`, addr), "address", "transaction_count")
			logError(err)
			bot.Send(m.Sender, "<b>Total Balance BCH: </b>"+fmt.Sprintf(`<code>%v</code>`, balanceBCHToPrint)+"\n"+
				"<b>Total Balance USD: </b>"+
				fmt.Sprintf(`<code>%v</code>`, balanceUSDToPrint)+"\n"+
				"<b>Transactions: </b>"+fmt.Sprintf(`<code>%v</code>`, transactionCount), tb.ModeHTML)
		} else if len(tx) == 64 {
			url := "https://api.blockchair.com/bitcoin-cash/dashboards/transaction/"
			getRequest, err := http.Get(url + tx)
			logError(err)
			readBody, err := ioutil.ReadAll(getRequest.Body)
			logError(err)
			json := []byte(readBody)

			totalInputValueBCH, err := jsonparser.GetInt(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "input_total")
			logError(err)
			totalInputValueUSD, err := jsonparser.GetFloat(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "input_total_usd")
			logError(err)
			totalOutputValueBCH, err := jsonparser.GetInt(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "output_total")
			logError(err)
			totalOutputValueUSD, err := jsonparser.GetFloat(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "output_total_usd")
			logError(err)
			size, err := jsonparser.GetInt(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "size")
			logError(err)
			initBlock, err := jsonparser.GetInt(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "block_id")
			logError(err)
			currentBlock, err := jsonparser.GetInt(json, "context", "state")
			logError(err)
			confirmations := currentBlock - initBlock
			fees, err := jsonparser.GetInt(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "fee")
			logError(err)
			coinbase, err := jsonparser.GetFloat(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "is_coinbase")
			logError(err)

			bot.Send(m.Sender, "<b>Total Input Value BCH: </b>"+fmt.Sprintf(`<code>%v</code>`, float64(totalInputValueBCH)*satoshi)+"\n"+
				"<b>Total Input Value USD: </b>"+fmt.Sprintf(`<code>%v</code>`, totalInputValueUSD)+"\n"+
				"<b>Total Output Value BCH: </b>"+fmt.Sprintf(`<code>%v</code>`, float64(totalOutputValueBCH)*satoshi)+"\n"+
				"<b>Total Output Value USD: </b>"+fmt.Sprintf(`<code>%v</code>`, totalOutputValueUSD)+"\n"+
				"<b>Size: </b>"+fmt.Sprintf(`<code>%v</code>`, size)+"\n"+
				"<b>Confirmations: </b>"+fmt.Sprintf(`<code>%v</code>`, confirmations)+"\n"+
				"<b>Fees: </b>"+fmt.Sprintf(`<code>%v</code>`, fees)+"\n"+
				"<b>Is Coinbase: </b>"+fmt.Sprintf(`<code>%v</code>`, coinbase), tb.ModeHTML)
		} else {
			bot.Send(m.Sender, "This is not a valid BCH address or transaction hash")
		}

	})
}

func blockchainStatus(bot *tb.Bot) {
	bot.Handle("/blockchainstatus", func(m *tb.Message) {
		getRequest, err := http.Get("https://api.blockchair.com/bitcoin-cash/stats")
		logError(err)
		readBody, err := ioutil.ReadAll(getRequest.Body)
		logError(err)
		json := []byte(readBody)

		blocks, err := jsonparser.GetInt(json, "data", "blocks")
		logError(err)
		blocksIn24h, err := jsonparser.GetInt(json, "data", "blocks_24h")
		logError(err)
		transactions, err := jsonparser.GetUnsafeString(json, "data", "transactions")
		logError(err)
		transactionsIn24h, err := jsonparser.GetInt(json, "data", "transactions_24h")
		logError(err)
		miningDifficulty, err := jsonparser.GetUnsafeString(json, "data", "difficulty")
		logError(err)
		hashrate24h, err := jsonparser.GetUnsafeString(json, "data", "hashrate_24h")
		logError(err)
		outputs, err := jsonparser.GetInt(json, "data", "outputs")
		logError(err)
		mempoolTransactions, err := jsonparser.GetInt(json, "data", "mempool_transactions")
		logError(err)
		totalFeesInMempool, err := jsonparser.GetFloat(json, "data", "mempool_total_fee_usd")
		logError(err)
		roundTotalFeesInMempool := math.Round(totalFeesInMempool)
		totalFeesInMempoolToPrint := fmt.Sprintf("%.2f", roundTotalFeesInMempool)
		txPerSecondInMempool, err := jsonparser.GetFloat(json, "data", "mempool_tps")
		logError(err)
		roundTxPerSecondInMempool := math.Round(txPerSecondInMempool)
		txPerSecondInMempoolToPrint := fmt.Sprintf("%.2f", roundTxPerSecondInMempool)

		currentlyNodes, err := jsonparser.GetInt(json, "data", "nodes")
		logError(err)
		circulationSupply, err := jsonparser.GetFloat(json, "data", "circulation")
		logError(err)
		roundCirculationSupply := math.Round(circulationSupply)
		formatedCirculationSupply := fmt.Sprintf("%.2f", roundCirculationSupply*satoshi)
		circulationSupplyToPrint := formatedCirculationSupply + "/" + strconv.Itoa(21000000)

		bot.Send(m.Sender, "<b>Blocks: </b>"+fmt.Sprintf(`<code>%v</code>`, blocks)+"\n"+
			"<b>Blocks in 24h: </b>"+fmt.Sprintf(`<code>%v</code>`, blocksIn24h)+"\n"+
			"<b>Transactions: </b>"+fmt.Sprintf(`<code>%v</code>`, transactions)+"\n"+
			"<b>Transactions in 24h: </b>"+fmt.Sprintf(`<code>%v</code>`, transactionsIn24h)+"\n"+
			"<b>Mining Difficulty: </b>"+fmt.Sprintf(`<code>%v</code>`, miningDifficulty)+"\n"+
			"<b>Hashrate 24: </b>"+fmt.Sprintf(`<code>%v</code>`, hashrate24h)+"\n"+
			"<b>Outputs: </b>"+fmt.Sprintf(`<code>%v</code>`, outputs)+"\n"+
			"<b>Mempoll Transactions: </b>"+fmt.Sprintf(`<code>%v</code>`, mempoolTransactions)+"\n"+
			"<b>Total Fees in Mempool USD: </b>"+fmt.Sprintf(`<code>%v</code>`, totalFeesInMempoolToPrint)+"\n"+
			"<b>Transactions per Second in Mempool: </b>"+fmt.Sprintf(`<code>%v</code>`, txPerSecondInMempoolToPrint)+"\n"+
			"<b>Currently Nodes: </b>"+fmt.Sprintf(`<code>%v</code>`, currentlyNodes)+"\n"+
			"<b>Circulation Supply: </b>"+fmt.Sprintf(`<code>%v</code>`, circulationSupplyToPrint), tb.ModeHTML)
	})
}

func price(bot *tb.Bot) {
	bot.Handle("/price", func(m *tb.Message) {
		getRequest, err := http.Get("https://api.blockchair.com/bitcoin-cash/stats")
		readBody, err := ioutil.ReadAll(getRequest.Body)
		json := []byte(readBody)

		priceUSD, err := jsonparser.GetFloat(json, "data", "market_price_usd")
		logError(err)
		volume24h, err := jsonparser.GetUnsafeString(json, "data", "volume_24h")
		logError(err)
		percentChange24h, err := jsonparser.GetFloat(json, "data", "market_price_usd_change_24h_percentage")
		logError(err)
		roundPercentChange := math.Round(percentChange24h)
		formatedPercentChange := fmt.Sprintf("%.2f", roundPercentChange)
		percentChangeToPrint := formatedPercentChange + "%"
		marketcapUSD, err := jsonparser.GetUnsafeString(json, "data", "market_cap_usd")
		logError(err)
		marketDominance, err := jsonparser.GetFloat(json, "data", "marke_dominance_percentage")
		logError(err)
		marketDominanceToPrint := strconv.Itoa(int(marketDominance)) + "%"

		bot.Send(m.Sender, "<b>Price USD: </b>"+fmt.Sprintf(`<code>%v</code>`, priceUSD)+"\n"+
			"<b>Volume 24h: </b>"+fmt.Sprintf(`<code>%v</code>`, volume24h)+"\n"+
			"<b>Percent Change 24h: </b>"+fmt.Sprintf(`<code>%v</code>`, percentChangeToPrint)+"\n"+
			"<b>Market Cap USD: </b>"+fmt.Sprintf(`<code>%v</code>`, marketcapUSD)+"\n"+
			"<b>Market Dominance: </b>"+fmt.Sprintf(`<code>%v</code>`, marketDominanceToPrint), tb.ModeHTML)

	})

}

func main() {
	var jsonFile, err = ioutil.ReadFile("config.json")
	if err != nil {
		log.Fatal(err)
	}
	var config, _ = jsonparser.GetString(jsonFile, "token")

	bot, err := tb.NewBot(tb.Settings{
		Token:  config,
		Poller: &tb.LongPoller{Timeout: 10 * time.Second},
	})
	if err != nil {
		log.Fatal(err)
	}
	start(bot)
	addressAndTransaction(bot)
	blockchainStatus(bot)
	price(bot)
	bot.Start()
}
