# Et sted for å utforske kode som senere legges inn i nettsiden, index.html
# Bruker VS Code "interactive mode", derav #%%-kommentarene

#%%
# Lese saft.xml og verifisere at vi har innhold i 'saft'
from saft2dataframe import saft2dataframe
saft = saft2dataframe('../testdata/saft.xml')
saft.info()
# %%

# Plan:
# Tidsserie med omsetning
# Visualisere omsetning
# Rapportere til fake API omsetning
# 

# Starter med omsetning pr måned
saft[['Transaction.TransactionDate', 'Line.AccountID', 'Line.DebitAmount.Amount', 'Line.CreditAmount.Amount']]
# %%
df = saft.loc[( # filtrerer på relevante konti
    saft['Line.AccountID'] >= 3000) 
    & (saft['Line.AccountID'] < 4000
)]\
    [[ # velger relevante kolonner
        'Transaction.TransactionDate',
        'Line.DebitAmount.Amount', 
        'Line.TaxAmount.Amount', 
        'Line.CreditAmount.Amount'
    ]]\
    .set_index('Transaction.TransactionDate',)\
    .groupby([lambda x: x.month])\
    .sum()
# %%
df.plot()
# %%
