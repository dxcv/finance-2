import numpy as np
import numpy.random as npr

M = 50
I = 10000
S0 = 100
T = 1
r = 0.05
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

def monte_carlo_brownian_motion(strike, option='call'):
   dt = T / M
   S = np.zeros((M + 1, I))
   S[0] = S0
   sn = standard_normal_dist(M, I)
   for t in range(1, M + 1):
       S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * sn[t])
   if option.lower() == 'call':
       hT = np.maximum(S[-1] - strike, 0)
   else:
       hT = np.maximum(strike - S[-1], 0)
   C0 = np.exp(-r * T) * np.mean(hT)
   return option + ' option value with strike price of ' + str(strike) + ': ' + str(C0)

print(monte_carlo_brownian_motion(strike=110, option='call'))
print(monte_carlo_brownian_motion(strike=110, option='put'))
