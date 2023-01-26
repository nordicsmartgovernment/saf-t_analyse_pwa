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