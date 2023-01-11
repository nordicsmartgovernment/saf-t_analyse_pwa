# Leser en SAF-T-fil og lager en Pandas DataFrame av data
# fra alle "Transaction"-elementene
# 
# Dokumentasjon av ET: https://docs.python.org/3/library/xml.etree.elementtree.html
#
# Known bugs:
# Hopper over "Analysis"-elementet som det kan være flere av pr linje


import pandas as pd
import xml.etree.ElementTree as ET
from typing import List

def saft2dataframe(file: str) -> pd.DataFrame:
    '''
        leser en SAF-T Financial NO-fil og returnerer alle "Transaction"
        som en pandas DataFrame
    '''
    if file == None:
        print("Mangler en fil, avslutter, returnerer None")
        return None
        
    tree = ET.parse(file)

    df = pd.DataFrame()

    journal = tree.getroot().find('*/{urn:StandardAuditFile-Taxation-Financial:NO}Journal')
    # Note: Can be useful to have data about the journal later. And the organisation etc.
    # But focusing on the transactions first ...

    transactions = journal.findall('{urn:StandardAuditFile-Taxation-Financial:NO}Transaction')

    for transaction in transactions:
        df = pd.concat([df, pd.DataFrame(process_transaction(transaction))])

    df = df.convert_dtypes() # gjør om de fleste fra object til string
    df = df.astype({ # valg av datatype pr felt bør verifiseres av noen ...
    #    'Transaction.Transaction': str,
    #    'Transaction.TransactionID': str,
        'Transaction.Period': int,
        'Transaction.PeriodYear': int,
        'Transaction.TransactionDate': 'datetime64',
        'Transaction.TransactionType': 'category',
    #    'Transaction.Description': str,
        'Transaction.SystemEntryDate': 'datetime64',
        'Transaction.GLPostingDate': 'datetime64',
    #    'Line.Line': str,
    #    'Line.RecordID': str,
        'Line.AccountID': int,
    #    'Line.Analysis': 'str',
    #    'Line.AnalysisType': 'category',
    #    'Line.AnalysisID': 'category',
    #    'Line.AnalysisAmount': str,
    #    'Line.Amount': float, # OOOOOOPs ... kan være både Tax Amount, og Analysis Amount
        'Line.ValueDate': 'datetime64',
    #    'Line.SourceDocumentID': str,
    #    'Line.Description': str,
    #    'Line.DebitAmount': str,
        'Line.DebitAmount.Amount': float,
    #    'Line.TaxInformation': str,
        'Line.TaxType': 'category',
        'Line.TaxCode': 'category',
        'Line.TaxPercentage': float,
        'Line.TaxBase': float,
        'Line.TaxAmount.Amount': float, # Her skulle det kommet en "Amount" rett etterpå ...
    #    'Line.ReferenceNumber': str,
    #    'Line.SupplierID': str,
        'Line.CreditAmount.Amount': float,
    #    'Line.CustomerID': str,
    })
    return df


def process_line(line: ET.Element) -> dict:
    '''lager dict for en line
        NB!! Ignorerer "Analysis"-elementene'''

    analysis = line.findall('{urn:StandardAuditFile-Taxation-Financial:NO}Analysis')
    for analyse in analysis:
        line.remove(analyse)

    res = {}
    for ld in line.iter():
        name = 'Line.' + str(ld.tag).split('}')[1]
        if name == 'Line.Amount':
            name = list(res.keys())[-1] + '.' + name.split('.')[-1]

        res[name] = ld.text.strip() if ld.text.strip() != '' else None

    return res


def process_transaction(transaction: ET.Element) -> List[dict]:
    '''lager en liste av dicts om hver transaction
    dict-listen kan legges til en dataframe'''

    resultat = []
    transaction_res = {}
    line_res = []
    lines = transaction.findall('{urn:StandardAuditFile-Taxation-Financial:NO}Line')
    for line in lines:
        line_res.append(process_line(line))
        transaction.remove(line)

    for transaction_data in transaction.iter(): 
        name = 'Transaction.' +  str(transaction_data.tag).split('}')[1]
        transaction_res[name] = transaction_data.text.strip() if \
            transaction_data.text.strip() != '' else None
    
    if len(line_res) == 0:
        resultat.append(transaction_res)

    else:
        for line in line_res:
            resultat.append({**transaction_res, **line})        

    return resultat


if __name__ == '__main__':
    df = saft2dataframe('saft.xml')
    print(df.describe())
    print(df.columns)
    print(df.info())
    print(df)