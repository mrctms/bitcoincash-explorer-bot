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
	"math"
	"net/http"
	"strconv"
	"time"
)

const satoshi = 0.00000001

var (
	bot, _ = tb.NewBot(tb.Settings{
		Token:  "",
		Poller: &tb.LongPoller{Timeout: 10 * time.Second},
	})
)

func Start() {
	bot.Handle("/start", func(m *tb.Message) {
		bot.Send(m.Sender, "There is a bot for the BitcoinCash Blockchain Explorer."+"\n"+
			"You can use this command:"+"\n"+"\n"+
			"/blockchainstatus"+"\n"+
			"/price"+"\n"+"\n"+
			"Or send an address or a transaction hash for check informations about it."+"\n"+"\n"+
			"If you have a problem with the bot or you want send me your feedback, contact me @MarckTomack")
	})
}

func AddressAndTransaction() {
	bot.Handle(tb.OnText, func(m *tb.Message) {
		addr := m.Text
		tx := m.Text
		if len(addr) == 34 || len(addr) == 42 || len(addr) == 54 {
			url := "https://api.blockchair.com/bitcoin-cash/dashboards/address/"
			getRequest, _ := http.Get(url + addr)
			readBody, _ := ioutil.ReadAll(getRequest.Body)
			json := []byte(readBody)
			parseBalanceBCH, _ := jsonparser.GetFloat(json, "data", fmt.Sprintf(`%v`, addr), "address", "balance")
			balanceBCH := parseBalanceBCH * satoshi
			roundBalanceBCH := math.Round(balanceBCH)
			balanceBCHToPrint := fmt.Sprintf("%.2f", roundBalanceBCH)
			balanceUSD, _ := jsonparser.GetFloat(json, "data", fmt.Sprintf(`%v`, addr), "address", "balance_usd")
			roundBalanceUSD := math.Round(balanceUSD)
			balanceUSDToPrint := fmt.Sprintf("%.2f", roundBalanceUSD)

			transactionCount, _ := jsonparser.GetInt(json, "data", fmt.Sprintf(`%v`, addr), "address", "transaction_count")

			bot.Send(m.Sender, "<b>Total Balance BCH: </b>"+fmt.Sprintf(`<code>%v</code>`, balanceBCHToPrint)+"\n"+
				"<b>Total Balance USD: </b>"+
				fmt.Sprintf(`<code>%v</code>`, balanceUSDToPrint)+"\n"+
				"<b>Transactions: </b>"+fmt.Sprintf(`<code>%v</code>`, transactionCount), tb.ModeHTML)
		} else if len(tx) == 64 {
			url := "https://api.blockchair.com/bitcoin-cash/dashboards/transaction/"
			getRequest, _ := http.Get(url + tx)
			readBody, _ := ioutil.ReadAll(getRequest.Body)
			json := []byte(readBody)

			totalInputValueBCH, _ := jsonparser.GetInt(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "input_total")
			totalInputValueUSD, _ := jsonparser.GetFloat(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "input_total_usd")
			totalOutputValueBCH, _ := jsonparser.GetInt(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "output_total")
			totalOutputValueUSD, _ := jsonparser.GetFloat(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "output_total_usd")
			size, _ := jsonparser.GetInt(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "size")
			initBlock, _ := jsonparser.GetInt(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "block_id")
			currentBlock, _ := jsonparser.GetInt(json, "context", "state")
			confirmations := currentBlock - initBlock
			fees, _ := jsonparser.GetInt(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "fee")
			coinbase, _ := jsonparser.GetFloat(json, "data", fmt.Sprintf(`%v`, tx), "transaction", "is_coinbase")

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

func BlockchainStatus() {
	bot.Handle("/blockchainstatus", func(m *tb.Message) {
		getRequest, _ := http.Get("https://api.blockchair.com/bitcoin-cash/stats")
		readBody, _ := ioutil.ReadAll(getRequest.Body)
		json := []byte(readBody)

		blocks, _ := jsonparser.GetInt(json, "data", "blocks")
		blocksIn24h, _ := jsonparser.GetInt(json, "data", "blocks_24h")
		transactions, _ := jsonparser.GetUnsafeString(json, "data", "transactions")
		transactionsIn24h, _ := jsonparser.GetInt(json, "data", "transactions_24h")
		miningDifficulty, _ := jsonparser.GetUnsafeString(json, "data", "difficulty")
		hashrate24h, _ := jsonparser.GetUnsafeString(json, "data", "hashrate_24h")
		outputs, _ := jsonparser.GetInt(json, "data", "outputs")
		mempoolTransactions, _ := jsonparser.GetInt(json, "data", "mempool_transactions")
		totalFeesInMempool, _ := jsonparser.GetFloat(json, "data", "mempool_total_fee_usd")
		roundTotalFeesInMempool := math.Round(totalFeesInMempool)
		totalFeesInMempoolToPrint := fmt.Sprintf("%.2f", roundTotalFeesInMempool)
		txPerSecondInMempool, _ := jsonparser.GetFloat(json, "data", "mempool_tps")
		roundTxPerSecondInMempool := math.Round(txPerSecondInMempool)
		txPerSecondInMempoolToPrint := fmt.Sprintf("%.2f", roundTxPerSecondInMempool)

		currentlyNodes, _ := jsonparser.GetInt(json, "data", "nodes")
		circulationSupply, _ := jsonparser.GetFloat(json, "data", "circulation")
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

func Price() {
	bot.Handle("/price", func(m *tb.Message) {
		getRequest, _ := http.Get("https://api.blockchair.com/bitcoin-cash/stats")
		readBody, _ := ioutil.ReadAll(getRequest.Body)
		json := []byte(readBody)

		priceUSD, _ := jsonparser.GetFloat(json, "data", "market_price_usd")
		volume24h, _ := jsonparser.GetUnsafeString(json, "data", "volume_24h")
		percentChange24h, _ := jsonparser.GetFloat(json, "data", "market_price_usd_change_24h_percentage")
		roundPercentChange := math.Round(percentChange24h)
		formatedPercentChange := fmt.Sprintf("%.2f", roundPercentChange)
		percentChangeToPrint := formatedPercentChange + "%"
		marketcapUSD, _ := jsonparser.GetUnsafeString(json, "data", "market_cap_usd")
		marketDominance, _ := jsonparser.GetFloat(json, "data", "marke_dominance_percentage")
		marketDominanceToPrint := strconv.Itoa(int(marketDominance)) + "%"

		bot.Send(m.Sender, "<b>Price USD: </b>"+fmt.Sprintf(`<code>%v</code>`, priceUSD)+"\n"+
			"<b>Volume 24h: </b>"+fmt.Sprintf(`<code>%v</code>`, volume24h)+"\n"+
			"<b>Percent Change 24h: </b>"+fmt.Sprintf(`<code>%v</code>`, percentChangeToPrint)+"\n"+
			"<b>Market Cap USD: </b>"+fmt.Sprintf(`<code>%v</code>`, marketcapUSD)+"\n"+
			"<b>Market Dominance: </b>"+fmt.Sprintf(`<code>%v</code>`, marketDominanceToPrint), tb.ModeHTML)

	})

}

func main() {
	Start()
	AddressAndTransaction()
	BlockchainStatus()
	Price()
	bot.Start()
}
