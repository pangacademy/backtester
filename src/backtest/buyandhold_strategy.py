'''
Classes for Buy and Hold
'''

import enum
import datetime
import pandas as pd


import common as cm
from strategy import Strategy
from datamatrix import DataMatrix, DataMatrixLoader

class BuyAndHoldStrategy(Strategy):

    def __init__(self, pref, input_datamatrix: DataMatrix, initial_capital: float, price_choice = cm.DataField.close,
                 weighing_scheme = cm.WeighingScheme.EqualDollarExposure):
        super().__init__(pref, f'Buy and Hold_{weighing_scheme.value}', input_datamatrix, initial_capital, price_choice)
        self.weighing_scheme = weighing_scheme

    def validate(self):
        '''
        validate if the input_dm has everything the strategy needs
        '''
        columns = self.input_dm.columns
        for ticker in self.universe:
            col = f"{ticker}_{self.price_choice}"
            if col not in columns:
                raise Exception(f"Cannot found {col} for {ticker}")

        if self.weighing_scheme == cm.WeighingScheme.MarketCapitalization:
            for ticker in self.universe:
                if f"{ticker}_{cm.DataField.capitalization}" not in columns:
                    raise Exception(f"Cannot found Market Capitalization for {ticker}")

    def run_model(self, model = None):
        '''
        No external prediction model needed
        return a trade signal and its corresponding shares
        '''
        taction = self.pricing_matrix.copy()
        tsignal = self.pricing_matrix.copy()
        price_row = taction.iloc[0]
        for col in taction.columns:
            taction[col] = cm.TradeAction.NONE.value
            tsignal[col] = 0
        taction.iloc[0:1, :] = cm.TradeAction.BUY.value
        tsignal.iloc[0:1, :] = cm.TradeSignal.LONG.value

        shares = tsignal.copy()
        if self.weighing_scheme == cm.WeighingScheme.EqualShares:
            sum_price = sum(price_row)
            sh = (int)(self.initial_capital / sum_price)

            for col in shares.columns:
                shares[col] = sh

        elif self.weighing_scheme == cm.WeighingScheme.EqualDollarExposure:
            mean_exposure = self.initial_capital / len(self.universe)
            for col in shares.columns:
                sh = (int) (mean_exposure / price_row[col])
                shares[col] = sh
        shares.iloc[1:, :] = 0.0

        # sell at the end
        tsignal.iloc[-1, :] = -1 # sell
        shares.iloc[-1] = shares.iloc[0]
        taction.iloc[-1, :] = cm.TradeAction.SELL_TO_CLOSE_ALL.value

        return(tsignal, taction, shares)



def _test1():

    from preference import Preference

    pref = Preference()
    # pick some random name
    universe = ['AWO', 'BDJ', 'BDTC']
    start_date = datetime.date(2013, 1, 1)
    end_date = datetime.date(2023, 1, 1)

    name = 'test'
    fields = [cm.DataField.close, cm.DataField.volume, cm.DataField.SMA_200, cm.DataField.daily_returns]

    loader = DataMatrixLoader(pref, name, universe, start_date, end_date)
    dm = loader.get_daily_datamatrix(fields)
    #print(dm.get_info())


    for weigh_scheme in [cm.WeighingScheme.EqualDollarExposure, cm.WeighingScheme.EqualShares]:
        buyandhold = BuyAndHoldStrategy(pref, dm, cm.OneMillion, weighing_scheme = weigh_scheme)
        buyandhold.validate()
        tradesignal, tradeaction, shares = buyandhold.run_model()

        print(tradeaction.head())
        print(shares)

        buyandhold.run_strategy()
        print(buyandhold.performance)

        buyandhold.save_to_csv(pref.test_output_dir)

def _test():
    _test1()


if __name__ == "__main__":
    _test()
