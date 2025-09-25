import pandas as pd
from ..tools.api import get_price_history
from ..graph.state import AgentState
from ..agents import valuation_analyst, warren_buffet, rakesh_jhunjhunwala

class Backtester:
    def __init__(self, ticker:str, period:str="1y", initial_cash:float=10000):
        self.ticker = ticker
        self.period = period
        self.cash = initial_cash
        self.price_data = get_price_history(ticker, period)
        self.holdings = 0
        self.history = []

    def run(self):
        #Fetching Historical Price Data
        hist = get_price_history(self.ticker, self.period)
        trades = 0

        for date, row in hist.iterrows():
            price = row["Close"]

            #Now intializing Agent State for this day
            state = AgentState(ticker=self.ticker, price=price)
            #Initializing and running Agents 
            state = valuation_analyst.analyze(state)
            state = warren_buffet.analyze(state)
            state = rakesh_jhunjhunwala.analyze(state)

            #Decision Making based on Agent Recommendations
            decision = self.aggregate_decisions(state.signals)
            # Count trades
            if decision in ["BUY", "SELL"]:
                trades += 1
            #Executing Trades Based on Decisions
            self.execute_trade(decision, price, date)
        
        
        # Convert to DataFrame
        df = pd.DataFrame(self.history)

        # Final portfolio value
        final_value = df.iloc[-1]["value"]
        total_return = (final_value - self.cash) / self.cash * 100

        summary = {
            "Final Portfolio Value": round(final_value, 2),
            "Total Return %": round(total_return, 2),
            "Number of Trades": trades
        }

        return df, summary
    
    def aggregate_decisions(self, signals:dict) -> str :
        votes = list(signals.values())
        if(votes.count("BUY") > votes.count("SELL")):
            return "BUY"
        elif votes.count("SELL") > votes.count("BUY"):
            return "SELL"
        return "HOLD"
    
    def execute_trade(self, decision:str, price: float, date):
        if decision == "BUY" and self.cash >=price:
             #Buy one share
            self.holdings +=1
            self.cash -= price
        elif decision == "SELL" and self.holdings >0:
            #Sell one share
            self.holdings -=1
            self.cash += price

        #Track Portfolio Value
        portfolio_value = self.cash + (self.holdings * price)
        self.history.append({
            "date": date, 
            "cash": self.cash, 
            "holdings": self.holdings, 
            "value": portfolio_value,
            "price": price
        })
   