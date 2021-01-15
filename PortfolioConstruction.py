import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#read portfolio data
Return = pd.DataFrame()
p = pd.read_csv('Portfolio.csv', parse_dates=['Date'])
Return['Date'] = p['Date']
Return['Date'] = pd.DatetimeIndex(Return['Date']).year.astype(float)
print(p.head)

def CalculateReturn(Equity,Bond,Investment):
    # Equity
    PGSF = 0.15
    PIX = 0.15
    PFES = 0.7

    # Bond
    PBOND = 1.0

    portfolio = pd.read_csv('Portfolio.csv', parse_dates=['Date'])
    EquityInvestment = Equity*Investment
    BondInvestment = Bond*Investment

    portfolio['PGSF Value'] = ""
    portfolio['PIX Value'] = ""
    portfolio['PFES Value'] = ""
    portfolio['PBOND Value'] = ""
    portfolio['Rebalanced E'] = ""
    portfolio['Rebalanced B'] = ""

    #first year value
    portfolio['PGSF Value'][0] = EquityInvestment * PGSF * portfolio['PGSF'][0]
    portfolio['PIX Value'][0] = EquityInvestment * PIX * portfolio['PIX'][0]
    portfolio['PFES Value'][0] = EquityInvestment * PFES * portfolio['PFES'][0]
    portfolio['PBOND Value'][0] = BondInvestment * PBOND * portfolio['PBOND'][0]

    portfolio['Rebalanced E'][0] = portfolio['PGSF Value'][0] + portfolio['PIX Value'][0] + portfolio['PFES Value'][0]
    portfolio['Rebalanced B'][0] = portfolio['PBOND Value'][0]

    for i in range(1,15):

        portfolio['PGSF Value'][i] = portfolio['Rebalanced E'][i-1] * PGSF * portfolio['PGSF'][i]
        portfolio['PIX Value'][i] = portfolio['Rebalanced E'][i-1] * PIX * portfolio['PIX'][i]
        portfolio['PFES Value'][i] = portfolio['Rebalanced E'][i-1] * PFES * portfolio['PFES'][i]
        portfolio['PBOND Value'][i] = portfolio['Rebalanced B'][i-1] * PBOND * portfolio['PBOND'][i]

        totalVal = portfolio['PGSF Value'][i] + portfolio['PIX Value'][i] + portfolio['PFES Value'][i] + portfolio['PBOND Value'][i]

        portfolio['Rebalanced E'][i] = totalVal * Equity
        portfolio['Rebalanced B'][i] = totalVal * Bond

    portfolio['Total'] = portfolio['Rebalanced B'] + portfolio['Rebalanced E']

    return portfolio['Total']

Return['Equity'] = CalculateReturn(1,0,20000).astype(float)
Return['Bond'] = CalculateReturn(0,1,20000).astype(float)
Return['50/50 Equity/Bond'] = CalculateReturn(0.5,0.5,20000).astype(float)
print(Return)
sns.set_style("darkgrid")
p = sns.color_palette("hls", 8)

ax = sns.lineplot(data=Return,y='Equity',x='Date',label="Full Equity", color='skyblue', marker='^',markeredgecolor="black",linewidth=5)
ax = sns.lineplot(data=Return,y='Bond',x='Date',label="Full Bond",color='lightcoral',marker="x",markeredgecolor="black",linewidth=5)
ax = sns.lineplot(data=Return,y='50/50 Equity/Bond',x='Date',color='palegreen',label="50/50 Equity/Bond",marker="o",markeredgecolor="black",linewidth=5)

ax.set(xlabel="Date",ylabel="RM10k Invested")
plt.legend()
plt.show()








