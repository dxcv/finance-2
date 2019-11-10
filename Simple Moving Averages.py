import numpy as np
import pandas as pd
from pylab import plt


price_table = '/Users/username/Documents/finance/GOOGLE-Table 1.csv' #full folder path
data = pd.read_csv(price_table, index_col=0)
rows = pd.read_csv(price_table, nrows=0, index_col=0)

product = []
for r in rows:
  if r.lower() != 'date':
      product.append(r)

SMAs1 = 42
SMAs2 = 252

data['SMAs1'] = data[product].rolling(SMAs1).mean()
data['SMAs2'] = data[product].rolling(SMAs2).mean()

data.plot(figsize=(10, 6))

data.dropna(inplace=True)
data['Position'] = np.where(data['SMAs1'] > data['SMAs2'], 1, -1)
print(data)

ax = data.plot(secondary_y='Position', figsize=(10, 6))
ax.get_legend().set_bbox_to_anchor((0.25, 0.85))
plt.show()
