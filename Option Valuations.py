import numpy as np
import numpy.random as npr

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
   dt = T / M
   S = np.zeros((M + 1, I))
   S[0] = S0
   sn = standard_normal_dist(M, I)
   for t in range(1, M + 1):
       S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * sn[t])
   if option_type.lower() == 'call':
       hT = np.maximum(S[-1] - K, 0)
   else:
       hT = np.maximum(K - S[-1], 0)
   C0 = np.exp(-r * T) * np.mean(hT)
   return option_type + ' option value: ' + str(C0)


parameters = {}
try:
    S0 = float(input('Initial Price of an underlying product(example 100): '))
    parameters['Initial Price'] = S0
except:
    S0 = 'ERROR'
    print('ERROR: Input value needs to be a number')
    parameters['Initial Price'] = S0

try:
    K = float(input('Strike price(example 120): '))
    parameters['Strike Price'] = K
except:
    K = 'ERROR'
    print('ERROR: Input value needs to be a number')
    parameters['Strike Price'] = K

try:
    r = float(input('Risk Free Interest Rate(example 0.05): '))
    parameters['Risk Free Interest Rate'] = r
except:
    r = 'ERROR'
    print('ERROR: Input value needs to be a number')
    parameters['Risk Free Interest Rate'] = r

try:
    T = float(input('Time Horizon in years(example 2): '))
    parameters['Time Horizon'] = T
except:
    T = 'ERROR'
    print('ERROR: Input value needs to be a number')
    parameters['Time Horizon'] = T

option_type = str(input('Call[Yes]/Put[No](example Yes): '))

if option_type.lower() == 'yes':
    option_type = 'call'
    parameters['Option Type'] = option_type
elif option_type.lower() == 'no':
    option_type = 'put'
    parameters['Option Type'] = option_type
else:
    option_type = 'ERROR'
    print('ERROR: Choose either Yes or No')
    parameters['Option Type'] = option_type


def compute():
    if 'ERROR' in parameters.values():
        return
    else:
        print('\n' + 'Option Valuation with following parameters:')
        for k, v in parameters.items():
            print(k + ':', v)
        print('\n' + monte_carlo_brownian_motion(S0, K, r, T, option_type))
compute()
