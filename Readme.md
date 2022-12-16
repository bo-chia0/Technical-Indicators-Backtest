# Technical Indicator Backtest --- Using Crypto
此專案共分為四個部分:

### 一、	Data
儲存 BTC, ETH, BNB, ADA 四種虛擬貨幣從 2020/08/02 ~ 2022/06/13 的

- unix 
- date - 日期
- symbol - 幣別
- open - 開盤價
- high - 最高價
- low - 最低價
- close - 收盤價
- Volume - (Crypto) 單位為虛擬貨幣之成交量
- Volume - USDT 單位為美元之成交量
- tradecount - 成交數目

等十種資訊

### 二、	Program
共有四個檔案：Account, Analysis, Strategies, Visualize
```sh
1.	Account
	回測使用，能記錄交易紀錄，並計算各項表現（勝率、報酬率...）
2.	Analysis
	對四種虛擬貨幣做基本資料分析並做成圖表（價格走勢、報酬率相關係數...）
3.	Strategies
	測試策略的主要程式。對每種策略進行模擬，最後將結果輸出成csv檔
4.	Visualize
	將 Strategies 輸出的結果製成圖表
```
### 三、	Results
儲存由 Strategies 和 Visualize 輸出的csv檔及圖表，內容為各技術指標之績效表現。

### 四、	Documents
技術指標應用於虛擬貨幣市場的分析報告