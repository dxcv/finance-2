import numpy as np
from scipy import stats
import scipy.optimize as sco
import pandas as pd
from pylab import plt


raw = pd.read_csv('/Users/yutakaobi/Documents/finance/price_table.csv', index_col=0, parse_dates=True).dropna()
symbols = pd.read_csv('/Users/yutakaobi/Documents/finance/price_table.csv', nrows=0)


products = []
for symbol in symbols:
  if symbol.lower() != 'date':
      products.append(symbol)
print('Investment Universe:\n', products, '\n')


noa = len(products)
data = raw[products]
data = data.dropna()
rets = np.log(data / data.shift(1))


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
print('Minimum Sharpe Ratio')
print('Sharpe Ratio: ' + str(Return(opts['x']) / Volatility(opts['x'])))
print('Return with minimum sharpe ratio: ' + str(Return((opts['x'])).round(3)))
print('Volatility with minimum sharpe ratio: ' + str(Volatility(opts['x']).round(3)))
print('Allocation details')
for allocation in range(len(opts['x'].round(3))):
   print('Allocation for ' + str(products[allocation]) + ': ' +
         str(opts['x'].round(3)[allocation]))
print('\n')


optv = sco.minimize(Volatility, eweights, method='SLSQP', bounds=bnds, constraints=cons)
print('Minimum Volatility')
print('Volatility: ' + str(Volatility(optv['x']).round(3)))
print('Return with minimum volatility: ' + str(Return(optv['x']).round(3)))
print('Sharpe Ratio: ' + str(Return(optv['x']) / Volatility(optv['x'])))
print('Allocation details')
for allocation in range(len(optv['x'].round(3))):
   print('Allocation for ' + str(products[allocation]) + ': ' +
         str(optv['x'].round(3)[allocation]))


cons = ({'type': 'eq', 'fun': lambda x: Return(x) - tret},
      {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bnds = tuple((0, 1) for x in weights)

trets = np.linspace(Return(optv['x']), Return(opts['x']), 50)
tvols = []
for tret in trets:
  res = sco.minimize(Volatility, eweights, method='SLSQP',
                     bounds=bnds, constraints=cons)
  tvols.append(res['fun'])
tvols = np.array(tvols)


plt.figure(figsize=(10, 6))
plt.scatter(pvols, prets, c=prets / pvols, marker='.', alpha=0.8, cmap='coolwarm')
plt.plot(tvols, trets, 'b', lw=2.5)
plt.plot(Volatility(opts['x']), Return(opts['x']),
       'y*', markersize=15)
plt.plot(Volatility(optv['x']), Return(optv['x']),
       'r*', markersize=15)
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')
plt.show()