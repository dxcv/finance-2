import numpy as np
import pandas as pd
from pylab import plt, mpl

data = pd.read_csv('/Users/username/Documents/finance/GOOGLE-Table 1.csv', index_col=0)

SMA1 = 42
SMA2 = 252

data['SMA1'] = data['GOOGLE'].rolling(SMA1).mean()
data['SMA2'] = data['GOOGLE'].rolling(SMA2).mean()

data.plot(figsize=(10, 6))

data.dropna(inplace=True)
data['Position'] = np.where(data['SMA1'] > data['SMA2'], 1, -1)
print(data)

ax = data.plot(secondary_y='Position', figsize=(10, 6))
ax.get_legend().set_bbox_to_anchor((0.25, 0.85))
plt.show()
