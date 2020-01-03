import quandl
import numpy as np
import numpy.random as npr
import pandas as pd
from pandas import DataFrame as df
from scipy import stats
import scipy.optimize as sco
from pylab import plt
from datetime import datetime
import time
import heapq
from static import SP500, ISO3



quandl.ApiConfig.api_key = '-kw-n8eEQg3ZaUP8tUsr'


def SMA(select):

    if select == 'Select Stock':
        return 'Error: Select a stock from the drop down!'

    else:

        ticker = SP500.get(select)
        data = quandl.get_table('WIKI/PRICES', qopts = {'columns': ['date', 'close', 'ticker']}, ticker = ticker, paginate=True)
        data.rename(columns={'date': 'Date'}, inplace=True)


        data = data.sort_values(by=['Date'])
        data = data.set_index('Date')


        SMAs_Short = 42
        SMAs_Long = 252


        df = data[data['ticker'] == ticker]
        df['SMAs_Short'] = df['close'].rolling(SMAs_Short).mean()
        df['SMAs_Long'] = df['close'].rolling(SMAs_Long).mean()
        df.rename(columns={'ticker': 'Ticker'}, inplace=True)
        df.dropna(inplace=True)
        df.rename(columns={'close': select}, inplace=True)
        df.plot(figsize=(15, 7.5))
        plt.ylabel('Price')
        df['Position'] = np.where(df['SMAs_Short'] > df['SMAs_Long'], 1, -1)
        df['Trade'] = np.where(df['Position'] != df['Position'].shift(1), 'Trade', 'Still')
        ax = df.plot(secondary_y='Position', figsize=(15, 7.5))
        plt.ylabel('Position')
        plt.show()
        df.rename(columns={select: 'Close'}, inplace=True)
        print(df)
        df = df[df['Trade'] == 'Trade'].drop(['Ticker', 'SMAs_Short', 'SMAs_Long', 'Trade'], axis=1)


        res = []
        for i in range(len(df)):
            if df['Position'][i] == 1:
                res.append('Buy ' + ticker + ' on ' + str(df.index[i].date().strftime("%b %d, %Y")) + ' Price at ' + str(df['Close'][i]))
            else:
                res.append('Sell ' + ticker + ' on ' + str(df.index[i].date().strftime("%b %d, %Y")) + ' Price at ' + str(df['Close'][i]))
        res = np.array(res).reshape(-1, 1)
        return 'Trading Strategy for ' + str(select) + ' (Ticker: ' + ticker + ')' +\
               '\n'*2 + str(res)



def MPT(select):

    if 'Select Stock' in select:
        select.remove('Select Stock')

    if len(select) < 2:
        return 'Error: Select at least 2 stocks from the drop down!'

    else:

        products = []
        for item in select:
            products.append(SP500.get(item))


        Inv_Universe = ('Investment Universe: ' + str(products))
        print(Inv_Universe)

        data = quandl.get_table('WIKI/PRICES', qopts={'columns': ['date', 'close', 'ticker']}, ticker=products, paginate=True).dropna()
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.sort_values(by=['Date'])
        print(data)

        start = []
        end = []
        for i in products:
            individual = pd.DataFrame()
            individual = data[data['ticker'] == i]
            print(i, individual.set_index('Date'))
            start.append(individual.values[0][0].date())
            end.append(individual.values[-1][0].date())
        start = heapq.nlargest(1, start)[0]
        end = heapq.nsmallest(1, end)[0]
        print('start date: ' + str(start) + ' / end date: ' + str(end))


        consolidated = pd.DataFrame()
        for j in products:
            adjusted = pd.DataFrame()
            adjusted = data[data['ticker'] == j]
            adjusted = adjusted.set_index('Date')
            adjusted = adjusted[str(start):str(end)]
            if products.index(j) == 0:
                consolidated = adjusted.drop('ticker', axis=1)
                consolidated.rename(columns={'close': j}, inplace=True)
            else:
                consolidated[j] = adjusted['close']
        print('CONSOLIDATED ', consolidated)


        noa = len(products)
        consolidated = consolidated[products]
        consolidated = consolidated.dropna()
        rets = np.log(consolidated / consolidated.shift(1))
        print(rets)


        def Return(weights):
            return np.sum(rets.mean() * weights) * 252


        def Volatility(weights):
            return np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))


        prets = []
        pvols = []
        for p in range(1000):
            weights = np.random.random(noa)
            weights /= np.sum(weights)
            prets.append(Return(weights))
            pvols.append(Volatility(weights))
        prets = np.array(prets)
        pvols = np.array(pvols)


        def Minimum_Sharpe_Ratio(weights):
            return -Return(weights) / Volatility(weights)


        cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bnds = tuple((0, 1) for x in range(noa))
        eweights = np.array(noa * [1 / noa])


        opts = sco.minimize(Minimum_Sharpe_Ratio, eweights, method='SLSQP', bounds=bnds, constraints=cons)
        MXS_Title = 'Maximum Sharpe Ratio details:'
        MXS_SR = 'Sharpe Ratio: ' + str((Return(opts['x']) / Volatility(opts['x'])).round(3))
        MXS_VOL = 'Volatility: ' + str(Volatility(opts['x']).round(3))
        MXS_PR = 'Portfolio Return: ' + str(Return((opts['x'])).round(3))
        MXS_Alloc_Title = 'Allocation details:'
        MXS_Alloc = []
        for allocation in range(len(opts['x'].round(3))):
            MXS_Alloc.append('Allocation for ' + str(products[allocation]) + ': ' +
                 str(opts['x'].round(3)[allocation]))
        MXS_Alloc = np.array(MXS_Alloc).reshape(-1, 1)


        optv = sco.minimize(Volatility, eweights, method='SLSQP', bounds=bnds, constraints=cons)
        MXV_Title = ('Minimum Volatility details:')
        MXV_VOL = ('Volatility: ' + str(Volatility(optv['x']).round(3)))
        MXV_SR = ('Sharpe Ratio: ' + str((Return(optv['x']) / Volatility(optv['x'])).round(3)))
        MXV_PR = ('Portfolio Return: ' + str(Return(optv['x']).round(3)))
        MXV_Alloc_Title = ('Allocation details:')
        MXV_Alloc = []
        for allocation in range(len(optv['x'].round(3))):
           MXV_Alloc.append('Allocation for ' + str(products[allocation]) + ': ' +
                 str(optv['x'].round(3)[allocation]))
        MXV_Alloc = np.array(MXV_Alloc).reshape(-1, 1)


        cons = ({'type': 'eq', 'fun': lambda x: Return(x) - tret},
              {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bnds = tuple((0, 1) for x in weights)


        trets = np.linspace(Return(optv['x']),Return(opts['x']), 50)
        tvols = []
        for tret in trets:
          res = sco.minimize(Volatility, eweights, method='SLSQP',
                             bounds=bnds, constraints=cons)
          tvols.append(res['fun'])
        tvols = np.array(tvols)


        plt.figure(figsize=(15, 7.5))
        plt.scatter(pvols, prets, c=prets / pvols, marker='.', alpha=0.8, cmap='coolwarm')
        plt.plot(tvols, trets, 'b', lw=2.5)
        plt.plot(Volatility(optv['x']), Return(optv['x']),
               'r*', markersize=10)
        plt.plot(Volatility(opts['x']), Return(opts['x']),
               'y*', markersize=10)
        plt.xlabel('expected volatility')
        plt.ylabel('expected return')
        plt.colorbar(label='Sharpe ratio')
        plt.show()


        return str(Inv_Universe) + '\n'*2 + \
               str(MXS_Title) + '\n'*2 + str(MXS_SR) + '\n' + str(MXS_VOL) + '\n' + \
               str(MXS_PR) + '\n' + str(MXS_Alloc_Title) + '\n' + str(MXS_Alloc) + '\n'*2 + \
               str(MXV_Title) + '\n'*2 + str(MXV_VOL) + '\n' + str(MXV_SR) + '\n' + \
               str(MXV_PR) + '\n' + str(MXV_Alloc_Title) + '\n' + str(MXV_Alloc)



def OPV(S0, K, r, T, option_type):

    M = 50
    I = 10000
    sigma = 0.25


    def standard_normal_dist(M, I, anti_paths=True, mo_match=True):
        if anti_paths is True:
           sn = npr.standard_normal((M + 1, int(I / 2)))
           sn = np.concatenate((sn, -sn), axis=1)
        else:
           sn = npr.standard_normal((M + 1, I))
        if mo_match is True:
           sn = (sn - sn.mean()) / sn.std()
        return sn


    def monte_carlo_brownian_motion(S0, K, r, T, option_type):
        S0 = float(S0)
        K = float(K)
        r = float(r)
        T = float(T)
        if option_type == 'Yes':
            option_type = 'Call'
        else:
            option_type = 'Put'
        dt = T / M
        S = np.zeros((M + 1, I))
        S[0] = S0
        sn = standard_normal_dist(M, I)
        for t in range(1, M + 1):
           S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * sn[t])
        if option_type == 'Call':
           hT = np.maximum(S[-1] - K, 0)
        else:
           hT = np.maximum(K - S[-1], 0)
        C0 = np.exp(-r * T) * np.mean(hT)
        return option_type + ' option value: ' + str(C0)

    return monte_carlo_brownian_motion(S0, K, r, T, option_type)


def IMF_Release(raw, data_type):
    country = []
    if data_type == 'population':
        suffix = '_LP'
    elif data_type == 'gdp':
        suffix = '_NGDPD'
    elif data_type == 'import':
        suffix = '_TMG_RPCH'
    elif data_type == 'export':
        suffix = '_TXG_RPCH'
    elif data_type == 'unemployment':
        suffix = '_LUR'

    raw = list(set(raw))
    for i in raw:
        country.append('ODA/' + ISO3[i] + suffix)
    print(country)
    data = quandl.get(country, authtoken="-kw-n8eEQg3ZaUP8tUsr")
    data = pd.DataFrame(data)

    for j in range(len(raw)):
        data.rename(columns={'ODA/' + ISO3[raw[j]] + suffix + ' - Value': raw[j]}, inplace=True)

    print(data)
    data.plot(figsize=(15, 7.5))
    plt.xlabel('Years')

    if data_type == 'population':
        plt.ylabel('Population in Millions')
    elif data_type == 'gdp':
        plt.ylabel('GDP in USD Billions')
    elif data_type == 'import':
        plt.ylabel('Percentage change in Imports')
        plt.show()
        return
    elif data_type == 'export':
        plt.ylabel('Percentage change in Exports')
        plt.show()
        return
    elif data_type == 'unemployment':
        plt.ylabel('Unemployment Rate in percentage')

    plt.show()
    data_relative = data.dropna()


    for k in range(len(raw)):
        res = []
        ind = data_relative[raw[k]][0]
        for l in range(len(data_relative)):
            res.append(data_relative[raw[k]][l]*100 / ind)
        data_relative[raw[k]] = res
    print(data_relative)
    data_relative.plot(figsize=(15, 7.5))
    plt.plot(data_relative)
    plt.xlabel('Years')
    if data_type == 'population':
        plt.ylabel('Percentage change in Population')
    elif data_type == 'gdp':
        plt.ylabel('Percentage change in GDP')
    elif data_type == 'unemployment':
        plt.ylabel('Percentage change in Unemployment Rate')

    plt.show()
