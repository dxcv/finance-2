import quandl
import numpy as np
import numpy.random as npr
import pandas as pd
from pandas import DataFrame as df
from scipy import stats
import scipy.optimize as sco
from pylab import plt
from datetime import datetime
import heapq



SP500 = {'A.O. Smith Corp': 'AOS',
         'Abbott Laboratories': 'ABT',
         'AbbVie Inc.': 'ABBV',
         'Accenture plc': 'ACN',
         'Activision Blizzard': 'ATVI',
         'Acuity Brands Inc': 'AYI',
         'Adobe Systems Inc': 'ADBE',
         'Advance Auto Parts': 'AAP',
         'Advanced Micro Devices Inc': 'AMD',
         'AES Corp': 'AES',
         'Aetna Inc': 'AET',
         'Affiliated Managers Group Inc': 'AMG',
         'AFLAC Inc': 'AFL',
         'Agilent Technologies Inc': 'A',
         'Air Products & Chemicals Inc': 'APD',
         'Akamai Technologies Inc': 'AKAM',
         'Alaska Air Group Inc': 'ALK',
         'Albemarle Corp': 'ALB',
         'Alexandria Real Estate Equities Inc': 'ARE',
         'Alexion Pharmaceuticals': 'ALXN',
         'Align Technology': 'ALGN',
         'Allegion': 'ALLE',
         'Allergan, Plc': 'AGN',
         'Alliance Data Systems': 'ADS',
         'Alliant Energy Corp': 'LNT',
         'Allstate Corp': 'ALL',
         'Alphabet Inc Class A': 'GOOGL',
         'Alphabet Inc Class C': 'GOOG',
         'Altria Group Inc': 'MO',
         'Amazon.com Inc.': 'AMZN',
         'Ameren Corp': 'AEE',
         'American Airlines Group': 'AAL',
         'American Electric Power': 'AEP',
         'American Express Co': 'AXP',
         'American International Group, Inc.': 'AIG',
         'American Tower Corp A': 'AMT',
         'American Water Works Company Inc': 'AWK',
         'Ameriprise Financial': 'AMP',
         'AmerisourceBergen Corp': 'ABC',
         'AMETEK Inc.': 'AME',
         'Amgen Inc.': 'AMGN',
         'Amphenol Corp': 'APH',
         'Anadarko Petroleum Corp': 'APC',
         'Analog Devices, Inc.': 'ADI',
         'Andeavor': 'ANDV',
         'ANSYS': 'ANSS',
         'Anthem Inc.': 'ANTM',
         'Aon plc': 'AON',
         'Apache Corporation': 'APA',
         'Apartment Investment & Management': 'AIV',
         'Apple Inc.': 'AAPL',
         'Applied Materials Inc.': 'AMAT',
         'Aptiv Plc': 'APTV',
         'Archer-Daniels-Midland Co': 'ADM',
         'Arconic Inc.': 'ARNC',
         'Arthur J. Gallagher & Co.': 'AJG',
         'Assurant Inc.': 'AIZ',
         'AT&T Inc.': 'T',
         'Autodesk Inc.': 'ADSK',
         'Automatic Data Processing': 'ADP',
         'AutoZone Inc': 'AZO',
         'AvalonBay Communities, Inc.': 'AVB',
         'Avery Dennison Corp': 'AVY',
         'Baker Hughes, a GE Company': 'BHGE',
         'Ball Corp': 'BLL',
         'Bank of America Corp': 'BAC',
         'Baxter International Inc.': 'BAX',
         'BB&T Corporation': 'BBT',
         'Becton Dickinson': 'BDX',
         'Berkshire Hathaway': 'BRK.B',
         'Best Buy Co. Inc.': 'BBY',
         'Biogen Inc.': 'BIIB',
         'BlackRock': 'BLK',
         'Block H&R': 'HRB',
         'Boeing Company': 'BA',
         'Booking Holdings Inc': 'BKNG',
         'BorgWarner': 'BWA',
         'Boston Properties': 'BXP',
         'Boston Scientific': 'BSX',
         'Brighthouse Financial Inc': 'BHF',
         'Bristol-Myers Squibb': 'BMY',
         'Broadcom': 'AVGO',
         'Brown-Forman Corp.': 'BF.B',
         'C. H. Robinson Worldwide': 'CHRW',
         'CA, Inc.': 'CA',
         'Cabot Oil & Gas': 'COG',
         'Cadence Design Systems': 'CDNS',
         'Campbell Soup': 'CPB',
         'Capital One Financial': 'COF',
         'Cardinal Health Inc.': 'CAH',
         'Carmax Inc': 'KMX',
         'Carnival Corp.': 'CCL',
         'Caterpillar Inc.': 'CAT',
         'Cboe Global Markets': 'CBOE',
         'CBRE Group': 'CBRE',
         'CBS Corp.': 'CBS',
         'Celgene Corp.': 'CELG',
         'Centene Corporation': 'CNC',
         'CenterPoint Energy': 'CNP',
         'CenturyLink Inc': 'CTL',
         'Cerner': 'CERN',
         'CF Industries Holdings Inc': 'CF',
         'Charles Schwab Corporation': 'SCHW',
         'Charter Communications': 'CHTR',
         'Chevron Corp.': 'CVX',
         'Chipotle Mexican Grill': 'CMG',
         'Chubb Limited': 'CB',
         'Church & Dwight': 'CHD',
         'CIGNA Corp.': 'CI',
         'Cimarex Energy': 'XEC',
         'Cincinnati Financial': 'CINF',
         'Cintas Corporation': 'CTAS',
         'Cisco Systems': 'CSCO',
         'Citigroup Inc.': 'C',
         'Citizens Financial Group': 'CFG',
         'Citrix Systems': 'CTXS',
         'CME Group Inc.': 'CME',
         'CMS Energy': 'CMS',
         'Coca-Cola Company (The)': 'KO',
         'Cognizant Technology Solutions': 'CTSH',
         'Colgate-Palmolive': 'CL',
         'Comcast Corp.': 'CMCSA',
         'Comerica Inc.': 'CMA',
         'Conagra Brands': 'CAG',
         'Concho Resources': 'CXO',
         'ConocoPhillips': 'COP',
         'Consolidated Edison': 'ED',
         'Constellation Brands': 'STZ',
         'Corning Inc.': 'GLW',
         'Costco Wholesale Corp.': 'COST',
         'Coty, Inc': 'COTY',
         'Crown Castle International Corp.': 'CCI',
         'CSRA Inc.': 'CSRA',
         'CSX Corp.': 'CSX',
         'Cummins Inc.': 'CMI',
         'CVS Health': 'CVS',
         'D. R. Horton': 'DHI',
         'Danaher Corp.': 'DHR',
         'Darden Restaurants': 'DRI',
         'DaVita Inc.': 'DVA',
         'Deere & Co.': 'DE',
         'Delta Air Lines Inc.': 'DAL',
         'Dentsply Sirona': 'XRAY',
         'Devon Energy Corp.': 'DVN',
         'Digital Realty Trust Inc': 'DLR',
         'Discover Financial Services': 'DFS',
         'Discovery Inc. Class A': 'DISCA',
         'Discovery Inc. Class C': 'DISCK',
         'Dish Network': 'DISH',
         'Dollar General': 'DG',
         'Dollar Tree': 'DLTR',
         'Dominion Energy': 'D',
         'Dover Corp.': 'DOV',
         'DowDuPont': 'DWDP',
         'Dr Pepper Snapple Group': 'DPS',
         'DTE Energy Co.': 'DTE',
         'Duke Energy': 'DUK',
         'Duke Realty Corp': 'DRE',
         'DXC Technology': 'DXC',
         'E*Trade': 'ETFC',
         'Eastman Chemical': 'EMN',
         'Eaton Corporation': 'ETN',
         'eBay Inc.': 'EBAY',
         'Ecolab Inc.': 'ECL',
         'Edison International': 'EIX',
         'Edwards Lifesciences': 'EW',
         'Electronic Arts': 'EA',
         'Emerson Electric Company': 'EMR',
         'Entergy Corp.': 'ETR',
         'Envision Healthcare': 'EVHC',
         'EOG Resources': 'EOG',
         'EQT Corporation': 'EQT',
         'Equifax Inc.': 'EFX',
         'Equinix': 'EQIX',
         'Equity Residential': 'EQR',
         'Essex Property Trust, Inc.': 'ESS',
         'Estee Lauder Cos.': 'EL',
         'Everest Re Group Ltd.': 'RE',
         'Eversource Energy': 'ES',
         'Exelon Corp.': 'EXC',
         'Expedia Inc.': 'EXPE',
         'Expeditors International': 'EXPD',
         'Express Scripts': 'ESRX',
         'Extra Space Storage': 'EXR',
         'Exxon Mobil Corp.': 'XOM',
         'F5 Networks': 'FFIV',
         'Facebook, Inc.': 'FB',
         'Fastenal Co': 'FAST',
         'Federal Realty Investment Trust': 'FRT',
         'FedEx Corporation': 'FDX',
         'Fidelity National Information Services': 'FIS',
         'Fifth Third Bancorp': 'FITB',
         'FirstEnergy Corp': 'FE',
         'Fiserv Inc': 'FISV',
         'FLIR Systems': 'FLIR',
         'Flowserve Corporation': 'FLS',
         'Fluor Corp.': 'FLR',
         'FMC Corporation': 'FMC',
         'Foot Locker Inc': 'FL',
         'Ford Motor': 'F',
         'Fortive Corp': 'FTV',
         'Fortune Brands Home & Security': 'FBHS',
         'Franklin Resources': 'BEN',
         'Freeport-McMoRan Inc.': 'FCX',
         'Gap Inc.': 'GPS',
         'Garmin Ltd.': 'GRMN',
         'Gartner Inc': 'IT',
         'General Dynamics': 'GD',
         'General Electric': 'GE',
         'General Growth Properties Inc.': 'GGP',
         'General Mills': 'GIS',
         'General Motors': 'GM',
         'Genuine Parts': 'GPC',
         'Gilead Sciences': 'GILD',
         'Global Payments Inc.': 'GPN',
         'Goldman Sachs Group': 'GS',
         'Goodyear Tire & Rubber': 'GT',
         'Grainger (W.W.) Inc.': 'GWW',
         'Halliburton Co.': 'HAL',
         'Hanesbrands Inc': 'HBI',
         'Harley-Davidson': 'HOG',
         'Harris Corporation': 'HRS',
         'Hartford Financial Svc.Gp.': 'HIG',
         'Hasbro Inc.': 'HAS',
         'HCA Holdings': 'HCA',
         'HCP Inc.': 'HCP',
         'Helmerich & Payne': 'HP',
         'Henry Schein': 'HSIC',
         'Hess Corporation': 'HES',
         'Hewlett Packard Enterprise': 'HPE',
         'Hilton Worldwide Holdings Inc': 'HLT',
         'Hologic': 'HOLX',
         'Home Depot': 'HD',
         'Honeywell International Inc.': 'HON',
         'Hormel Foods Corp.': 'HRL',
         'Host Hotels & Resorts': 'HST',
         'HP Inc.': 'HPQ',
         'Humana Inc.': 'HUM',
         'Huntington Bancshares': 'HBAN',
         'Huntington Ingalls Industries': 'HII',
         'IDEXX Laboratories': 'IDXX',
         'IHS Markit Ltd.': 'INFO',
         'Illinois Tool Works': 'ITW',
         'Illumina Inc': 'ILMN',
         'Incyte': 'INCY',
         'Ingersoll-Rand PLC': 'IR',
         'Intel Corp.': 'INTC',
         'Intercontinental Exchange': 'ICE',
         'International Business Machines': 'IBM',
         'International Paper': 'IP',
         'Interpublic Group': 'IPG',
         'Intl Flavors & Fragrances': 'IFF',
         'Intuit Inc.': 'INTU',
         'Intuitive Surgical Inc.': 'ISRG',
         'Invesco Ltd.': 'IVZ',
         'IPG Photonics Corp.': 'IPGP',
         'IQVIA Holdings Inc.': 'IQV',
         'Iron Mountain Incorporated': 'IRM',
         'J. B. Hunt Transport Services': 'JBHT',
         'Jacobs Engineering Group': 'JEC',
         'JM Smucker': 'SJM',
         'Johnson & Johnson': 'JNJ',
         'Johnson Controls International': 'JCI',
         'JPMorgan Chase & Co.': 'JPM',
         'Juniper Networks': 'JNPR',
         'Kansas City Southern': 'KSU',
         'Kellogg Co.': 'K',
         'KeyCorp': 'KEY',
         'Kimberly-Clark': 'KMB',
         'Kimco Realty': 'KIM',
         'Kinder Morgan': 'KMI',
         'KLA-Tencor Corp.': 'KLAC',
         'Kohls Corp.': 'KSS',
         'Kraft Heinz Co': 'KHC',
         'Kroger Co.': 'KR',
         'L Brands Inc.': 'LB',
         'L-3 Communications Holdings': 'LLL',
         'Laboratory Corp. of America Holding': 'LH',
         'Lam Research': 'LRCX',
         'Leggett & Platt': 'LEG',
         'Lennar Corp.': 'LEN',
         'Leucadia National Corp.': 'LUK',
         'Lilly (Eli) & Co.': 'LLY',
         'Lincoln National': 'LNC',
         'LKQ Corporation': 'LKQ',
         'Lockheed Martin Corp.': 'LMT',
         'Loews Corp.': 'L',
         'Lowes Cos.': 'LOW',
         'LyondellBasell': 'LYB',
         'M&T Bank Corp.': 'MTB',
         'Macerich': 'MAC',
         'Macys Inc.': 'M',
         'Marathon Oil Corp.': 'MRO',
         'Marathon Petroleum': 'MPC',
         'Marriott International.': 'MAR',
         'Marsh & McLennan': 'MMC',
         'Martin Marietta Materials': 'MLM',
         'Masco Corp.': 'MAS',
         'Mastercard Inc.': 'MA',
         'Mattel Inc.': 'MAT',
         'McCormick & Co.': 'MKC',
         'McDonalds Corp.': 'MCD',
         'McKesson Corp.': 'MCK',
         'Medtronic plc': 'MDT',
         'Merck & Co.': 'MRK',
         'MetLife Inc.': 'MET',
         'Mettler Toledo': 'MTD',
         'MGM Resorts International': 'MGM',
         'Michael Kors Holdings': 'KORS',
         'Microchip Technology': 'MCHP',
         'Micron Technology': 'MU',
         'Microsoft Corp.': 'MSFT',
         'Mid-America Apartments': 'MAA',
         'Mohawk Industries': 'MHK',
         'Molson Coors Brewing Company': 'TAP',
         'Mondelez International': 'MDLZ',
         'Monsanto Co.': 'MON',
         'Monster Beverage': 'MNST',
         'Moodys Corp': 'MCO',
         'Morgan Stanley': 'MS',
         'Motorola Solutions Inc.': 'MSI',
         'Mylan N.V.': 'MYL',
         'Nasdaq, Inc.': 'NDAQ',
         'National Oilwell Varco Inc.': 'NOV',
         'Navient': 'NAVI',
         'Nektar Therapeutics': 'NKTR',
         'NetApp': 'NTAP',
         'Netflix Inc.': 'NFLX',
         'Newell Brands': 'NWL',
         'Newfield Exploration Co': 'NFX',
         'Newmont Mining Corporation': 'NEM',
         'News Corp. Class A': 'NWSA',
         'News Corp. Class B': 'NWS',
         'NextEra Energy': 'NEE',
         'Nielsen Holdings': 'NLSN',
         'Nike': 'NKE',
         'NiSource Inc.': 'NI',
         'Noble Energy Inc': 'NBL',
         'Nordstrom': 'JWN',
         'Norfolk Southern Corp.': 'NSC',
         'Northern Trust Corp.': 'NTRS',
         'Northrop Grumman Corp.': 'NOC',
         'Norwegian Cruise Line': 'NCLH',
         'NRG Energy': 'NRG',
         'Nucor Corp.': 'NUE',
         'Nvidia Corporation': 'NVDA',
         'OReilly Automotive': 'ORLY',
         'Occidental Petroleum': 'OXY',
         'Omnicom Group': 'OMC',
         'ONEOK': 'OKE',
         'Oracle Corp.': 'ORCL',
         'PACCAR Inc.': 'PCAR',
         'Packaging Corporation of America': 'PKG',
         'Parker-Hannifin': 'PH',
         'Paychex Inc.': 'PAYX',
         'PayPal': 'PYPL',
         'Pentair Ltd.': 'PNR',
         'Peoples United Financial': 'PBCT',
         'PepsiCo Inc.': 'PEP',
         'PerkinElmer': 'PKI',
         'Perrigo': 'PRGO',
         'Pfizer Inc.': 'PFE',
         'PG&E Corp.': 'PCG',
         'Philip Morris International': 'PM',
         'Phillips 66': 'PSX',
         'Pinnacle West Capital': 'PNW',
         'Pioneer Natural Resources': 'PXD',
         'PNC Financial Services': 'PNC',
         'Polo Ralph Lauren Corp.': 'RL',
         'PPG Industries': 'PPG',
         'PPL Corp.': 'PPL',
         'Praxair Inc.': 'PX',
         'Principal Financial Group': 'PFG',
         'Procter & Gamble': 'PG',
         'Progressive Corp.': 'PGR',
         'Prologis': 'PLD',
         'Prudential Financial': 'PRU',
         'Public Serv. Enterprise Inc.': 'PEG',
         'Public Storage': 'PSA',
         'Pulte Homes Inc.': 'PHM',
         'PVH Corp.': 'PVH',
         'Qorvo': 'QRVO',
         'QUALCOMM Inc.': 'QCOM',
         'Quanta Services Inc.': 'PWR',
         'Quest Diagnostics': 'DGX',
         'Range Resources Corp.': 'RRC',
         'Raymond James Financial Inc.': 'RJF',
         'Raytheon Co.': 'RTN',
         'Realty Income Corporation': 'O',
         'Red Hat Inc.': 'RHT',
         'Regency Centers Corporation': 'REG',
         'Regeneron': 'REGN',
         'Regions Financial Corp.': 'RF',
         'Republic Services Inc': 'RSG',
         'ResMed': 'RMD',
         'Robert Half International': 'RHI',
         'Rockwell Automation Inc.': 'ROK',
         'Rockwell Collins': 'COL',
         'Roper Technologies': 'ROP',
         'Ross Stores': 'ROST',
         'Royal Caribbean Cruises Ltd': 'RCL',
         'S&P Global, Inc.': 'SPGI',
         'Salesforce.com': 'CRM',
         'SBA Communications': 'SBAC',
         'SCANA Corp': 'SCG',
         'Schlumberger Ltd.': 'SLB',
         'Seagate Technology': 'STX',
         'Sealed Air': 'SEE',
         'Sempra Energy': 'SRE',
         'Sherwin-Williams': 'SHW',
         'Simon Property Group Inc': 'SPG',
         'Skyworks Solutions': 'SWKS',
         'SL Green Realty': 'SLG',
         'Snap-On Inc.': 'SNA',
         'Southern Co.': 'SO',
         'Southwest Airlines': 'LUV',
         'Stanley Black & Decker': 'SWK',
         'Starbucks Corp.': 'SBUX',
         'State Street Corp.': 'STT',
         'Stericycle Inc': 'SRCL',
         'Stryker Corp.': 'SYK',
         'SunTrust Banks': 'STI',
         'SVB Financial': 'SIVB',
         'Symantec Corp.': 'SYMC',
         'Synchrony Financial': 'SYF',
         'Synopsys Inc.': 'SNPS',
         'Sysco Corp.': 'SYY',
         'T. Rowe Price Group': 'TROW',
         'Take-Two Interactive': 'TTWO',
         'Tapestry, Inc.': 'TPR',
         'Target Corp.': 'TGT',
         'TE Connectivity Ltd.': 'TEL',
         'TechnipFMC': 'FTI',
         'Texas Instruments': 'TXN',
         'Textron Inc.': 'TXT',
         'The Bank of New York Mellon Corp.': 'BK',
         'The Clorox Company': 'CLX',
         'The Cooper Companies': 'COO',
         'The Hershey Company': 'HSY',
         'The Mosaic Company': 'MOS',
         'The Travelers Companies Inc.': 'TRV',
         'The Walt Disney Company': 'DIS',
         'Thermo Fisher Scientific': 'TMO',
         'Tiffany & Co.': 'TIF',
         'Time Warner Inc.': 'TWX',
         'TJX Companies Inc.': 'TJX',
         'Torchmark Corp.': 'TMK',
         'Total System Services': 'TSS',
         'Tractor Supply Company': 'TSCO',
         'TransDigm Group': 'TDG',
         'TripAdvisor': 'TRIP',
         'Twenty-First Century Fox Class A': 'FOXA',
         'Twenty-First Century Fox Class B': 'FOX',
         'Tyson Foods': 'TSN',
         'U.S. Bancorp': 'USB',
         'UDR Inc': 'UDR',
         'Ulta Beauty': 'ULTA',
         'Under Armour Class A': 'UAA',
         'Under Armour Class C': 'UA',
         'Union Pacific': 'UNP',
         'United Continental Holdings': 'UAL',
         'United Health Group Inc.': 'UNH',
         'United Parcel Service': 'UPS',
         'United Rentals, Inc.': 'URI',
         'United Technologies': 'UTX',
         'Universal Health Services, Inc.': 'UHS',
         'Unum Group': 'UNM',
         'V.F. Corp.': 'VFC',
         'Valero Energy': 'VLO',
         'Varian Medical Systems': 'VAR',
         'Ventas Inc': 'VTR',
         'Verisign Inc.': 'VRSN',
         'Verisk Analytics': 'VRSK',
         'Verizon Communications': 'VZ',
         'Vertex Pharmaceuticals Inc': 'VRTX',
         'Viacom Inc.': 'VIAB',
         'Visa Inc.': 'V',
         'Vornado Realty Trust': 'VNO',
         'Vulcan Materials': 'VMC',
         'Wal-Mart Stores': 'WMT',
         'Walgreens Boots Alliance': 'WBA',
         'Waste Management Inc.': 'WM',
         'Waters Corporation': 'WAT',
         'Wec Energy Group Inc': 'WEC',
         'Wells Fargo': 'WFC',
         'Welltower Inc.': 'WELL',
         'Western Digital': 'WDC',
         'Western Union Co': 'WU',
         'WestRock Company': 'WRK',
         'Weyerhaeuser Corp.': 'WY',
         'Whirlpool Corp.': 'WHR',
         'Williams Cos.': 'WMB',
         'Willis Towers Watson': 'WLTW',
         'Wyndham Worldwide': 'WYN',
         'Wynn Resorts Ltd': 'WYNN',
         'Xcel Energy Inc': 'XEL',
         'Xerox Corp.': 'XRX',
         'Xilinx Inc': 'XLNX',
         'XL Capital': 'XL',
         'Xylem Inc.': 'XYL',
         'Yum! Brands Inc': 'YUM',
         'Zimmer Biomet Holdings': 'ZBH',
         'Zions Bancorp': 'ZION',
         'Zoetis': 'ZTS'}


quandl.ApiConfig.api_key = '-kw-n8eEQg3ZaUP8tUsr'


def SMA(select):

    ticker = SP500.get(select)
    data = quandl.get_table('WIKI/PRICES', qopts = {'columns': ['date', 'close', 'ticker']}, ticker = ticker, paginate=True)
    data.rename(columns={'date': 'Date'}, inplace=True)


    data = data.sort_values(by=['Date'])
    data = data.set_index('Date')


    SMAs1 = 42
    SMAs2 = 252


    df = data[data['ticker'] == ticker]
    df['SMAs1'] = df['close'].rolling(SMAs1).mean()
    df['SMAs2'] = df['close'].rolling(SMAs2).mean()
    df.rename(columns={'ticker': 'Ticker'}, inplace=True)
    df.dropna(inplace=True)
    df.rename(columns={'close': select}, inplace=True)
    df.plot(figsize=(10, 6))
    df['Position'] = np.where(df['SMAs1'] > df['SMAs2'], 1, -1)
    df['Trade'] = np.where(df['Position'] != df['Position'].shift(1), 'Trade', 'Still')
    ax = df.plot(secondary_y='Position', figsize=(10, 6))
    ax.get_legend().set_bbox_to_anchor((0.25, 0.85))
    plt.show()
    df.rename(columns={select: 'Close'}, inplace=True)
    print(df)
    df = df[df['Trade'] == 'Trade'].drop(['Ticker', 'SMAs1', 'SMAs2', 'Trade'], axis=1)


    res = []
    for i in range(len(df)):
        if df['Position'][i] == 1:
            res.append('Go Long on ' + str(df.index[i].date()) + ' Price at ' + str(df['Close'][i]))
        else:
            res.append('Go Short on ' + str(df.index[i].date()) + ' Price at ' + str(df['Close'][i]))
    res = np.array(res).reshape(-1, 1)
    return 'Trading Strategy for ' + str(select) + '\n'*2 + str(res)



def MPT(select):

    products = []
    for item in select:
        products.append(SP500.get(item))

    print('Investment Universe: ' + str(products), '\n')

    data = quandl.get_table('WIKI/PRICES', qopts={'columns': ['date', 'close', 'ticker']}, ticker=products, paginate=True).dropna()
    data.rename(columns={'date': 'Date'}, inplace=True)
    data = data.sort_values(by=['Date'])


    start = []
    end = []
    for i in products:
        individual = pd.DataFrame()
        individual = data[data['ticker'] == i]
        print(i, individual.set_index('Date'))
        start.append(individual.values[0][0].date())
        end.append(individual.values[-1][0].date())
    start = heapq.nlargest(1, start)[0]
    print(start, type(start))
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
    MXS_SR = 'Sharpe Ratio: ' + str(Return(opts['x']) / Volatility(opts['x']))
    MXS_VOL = 'Volatility: ' + str(Volatility(opts['x']).round(3))
    MXS_PR = 'Portfolio Return: ' + str(Return((opts['x'])).round(3))
    MXS_Alloc_Title = 'Allocation details:'
    MXS_Alloc = []
    for allocation in range(len(opts['x'].round(3))):
        MXS_Alloc.append('Allocation for ' + str(products[allocation]) + ': ' +
             str(opts['x'].round(3)[allocation]))
    MXS_Alloc = np.array(MXS_Alloc).reshape(len(products), 1)


    optv = sco.minimize(Volatility, eweights, method='SLSQP', bounds=bnds, constraints=cons)
    MXV_Title = ('Minimum Volatility details:')
    MXV_VOL = ('Volatility: ' + str(Volatility(optv['x']).round(3)))
    MXV_SR = ('Sharpe Ratio: ' + str(Return(optv['x']) / Volatility(optv['x'])))
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


    plt.figure(figsize=(10, 6))
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


    return str(MXS_Title) + '\n'*2 + str(MXS_SR) + '\n' + str(MXS_VOL) + '\n' + \
           str(MXS_PR) + '\n' + str(MXS_Alloc_Title) + '\n' + str(MXS_Alloc) + '\n'*3 + \
           str(MXV_Title) + '\n'*2 + str(MXV_VOL) + '\n' + str(MXV_SR) + '\n' + \
           str(MXV_PR) + '\n'+ str(MXV_Alloc_Title) + '\n' + str(MXV_Alloc)



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
        if option_type.lower() == 'yes':
            option_type = 'call'
        else:
            option_type = 'put'
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
        print(option_type + ' option value: ' + str(C0))

    monte_carlo_brownian_motion(S0, K, r, T, option_type)