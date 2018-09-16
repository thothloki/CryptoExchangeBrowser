import requests, json, sys, time, datetime
from decimal import Decimal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
     QLabel, QLineEdit, QGridLayout, QComboBox, QDesktopWidget
from PyQt5.QtCore import Qt
from time import gmtime, strftime
import time

import exchanges
from exchanges import MapleExchange, TradeOgre

class App (QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Crypto Exchange Coin Values'
        
        self.defineGUI()
        self.updateMainCoins()
        self.pairsList()
        self.layoutGUI()
            
    def closeEvent(self,event):
        event.accept()
        sys.exit

    def updateMainCoins(self):
        coinp = mainCoins()
        self.btc = coinp[0]
        self.ltc = coinp[1]
        self.xmr = coinp[2]
        self.eth = coinp[3]
        self.time = coinp[4]
        self.btcPrice.setText('BTC: $' + str(self.btc))
        self.ltcPrice.setText('LTC: $' + str(self.ltc))
        self.xmrPrice.setText('XMR: $' + str(self.xmr))
        self.ethPrice.setText('ETH: $' + str(self.eth))
        self.pullTime.setText('Updated: ' + str(self.time))
                
    def defineGUI(self):
        self.setWindowTitle(self.title)
        #Exchanges
        self.exchangeLabel = QLabel('Select Exchange:')
        self.exchangeSelect = QComboBox(self)
        #main coin prices
        self.mainCoins = QLabel('Main Coin Prices')
        self.btcPrice = QLabel('')
        self.ltcPrice = QLabel('')
        self.xmrPrice = QLabel('')
        self.ethPrice = QLabel('')
        self.pullTime = QLabel('')
        self.updateMainCoinsBtn = QPushButton('Update Prices', self)
        self.updateMainCoinsBtn.clicked.connect(self.updateMainCoins)
        #trading pairs
        self.coinLabel = QLabel('Trading Pairs:')
        self.coinSelect = QComboBox(self)
        self.coinSelectBtn = QPushButton('Check Coin', self)
        self.coinSelectBtn.clicked.connect(self.checkCoin)
        #coin info
        self.ask = QLabel('Ask: ')
        self.bid = QLabel('Bid: ')
        self.last = QLabel('Last: ')
        #coind amounts
        self.enterAmount = QLabel('Enter Coin Amount: ')
        self.qty = QLineEdit(self)
        self.askUSD = QLabel('')
        self.bidUSD = QLabel('')
        self.lastUSD = QLabel('')
        #MISC
        
        self.spacer = QLabel('')
        donateLink ="<a href=\"https://github.com/thothloki/CryptoExchangeBrowser/blob/master/Donate\">'Buy the Dev a beer'</a>" 
        self.donate = QLabel(donateLink)
        self.donate.setOpenExternalLinks(True)
        self.dev = QLabel('Written and Developed by ThothLoki')

    def layoutGUI(self):
        #layout setup
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.exchangeLabel, 0,0)
        grid.addWidget(self.exchangeSelect, 0,1)
        grid.addWidget(self.donate, 0, 3)
        grid.addWidget(self.mainCoins, 0,4)
        grid.addWidget(self.btcPrice, 1, 4)
        grid.addWidget(self.bid, 2, 0)
        grid.addWidget(self.ask, 2, 1)
        grid.addWidget(self.last, 2, 2)
        grid.addWidget(self.ltcPrice, 2, 4)
        grid.addWidget(self.xmrPrice, 3, 4)
        grid.addWidget(self.coinLabel, 4,0)
        grid.addWidget(self.coinSelect, 4,1)
        grid.addWidget(self.enterAmount, 4,2)
        grid.addWidget(self.qty, 4,3)
        grid.addWidget(self.ethPrice, 4, 4)
        #need spacing row
        grid.addWidget(self.spacer,5,0)
        grid.addWidget(self.bidUSD, 6,0)
        grid.addWidget(self.askUSD, 6,1)
        grid.addWidget(self.lastUSD, 6,2)
        grid.addWidget(self.pullTime, 6,4)
        grid.addWidget(self.coinSelectBtn, 7, 0)
        grid.addWidget(self.dev, 7, 1, 1, 2)
        grid.addWidget(self.donate, 7, 3)
        grid.addWidget(self.updateMainCoinsBtn, 7,4)

        self.loadPairs(self.exchangeSelect.currentIndex())
        self.exchangeSelect.currentIndexChanged.connect(self.indexChanged, self.exchangeSelect.currentIndex())
        
        self.center()
        self.show()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def pairsList(self):
        ex = exchanges.exchangeList
        for i in ex:
            self.coinSelect.clear()
            self.exchangeSelect.addItem(i, [eval(i).getPairs()])

    def loadPairs(self, index):
        self.coinSelect.clear()
        data = self.exchangeSelect.itemData(index)
        if data is not None:
            for x in data:
                self.coinSelect.addItems(sorted(x))

    def indexChanged(self, index):
        self.coinSelect.clear()
        data = self.exchangeSelect.itemData(index)
        if data is not None:
            for x in data:
                self.coinSelect.addItems(sorted(x))

    def checkCoin(self):
        e = self.exchangeSelect.currentText()
        selected = str(self.coinSelect.currentText())
        if len(self.qty.text()) == 0:
            self.qty.setText('0')
        main, bid, ask, last = eval(e).getCoin(selected)
        if main == 'BTC':
            self.checkCalcs(self.btc, bid, ask, last)
        elif main == 'LTC':
            self.checkCalcs(self.ltc, bid, ask, last)
        elif main == 'XMR':
            self.checkCalcs(self.xmr, bid, ask, last)
        elif main == 'ETH':
            self.checkCalcs(self.eth, bid, ask, last)
        else:
            self.bid.setText('Bid: ' + bid)
            self.ask.setText('Ask: ' + ask)
            self.last.setText('Last: ' + last)
            self.bidUSD.setText('Bid Value: NA')
            self.askUSD.setText('Ask Value: NA')
            self.lastUSD.setText('Last Value: NA')

    def checkCalcs(self, base, bid, ask, last):
        self.bid.setText('Bid: ' + bid)
        self.ask.setText('Ask: ' + ask)
        self.last.setText('Last: ' + last)
        bidValue = Decimal((float(bid) * float(self.qty.text())) * base)
        bidValue = round(bidValue, 2)
        askValue = Decimal((float(ask) * float(self.qty.text())) * base)
        askValue = round(askValue, 2)
        lastValue = Decimal((float(last) * float(self.qty.text())) * base)
        lastValue = round(lastValue, 2)
        self.bidUSD.setText('Bid Value: $' + str(bidValue))
        self.askUSD.setText('Ask Value: $' + str(askValue))
        self.lastUSD.setText('Lask Value: $' + str(lastValue))

def mainCoins():
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
    btc = r.json()['USD']
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD')
    ltc = r.json()['USD']
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=XMR&tsyms=USD')
    xmr = r.json()['USD']
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD')
    eth = r.json()['USD']
    now = time.strftime("%x") + ' ' + time.strftime("%X")
    return btc, ltc, xmr, eth, now

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
