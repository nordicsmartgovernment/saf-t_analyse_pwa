
from numpy import datetime64
import pandas as pd
from saft2dataframe import saft2dataframe

def analyse(
    from_and_included_date: str,
    to_date: str,
    from_and_included_account_id: int,
    to_account_id: int,
    df: pd.DataFrame, # dataframe converted from SAF-T by saft2dataframe
    ) -> dict:

    return dict(df.loc[
        (                                                         # filtering transactions:
            df['Transaction.TransactionDate'] >= from_and_included_date)     # from January 1st ...
            & (df['Transaction.TransactionDate'] < to_date)   # ... to (but not included) February 1st
            & (df['Line.AccountID'] >= from_and_included_account_id)           # including the accounts for "sales" (3000-group)
            & (df['Line.AccountID'] < to_account_id)] \
            [[  
            'Line.DebitAmount.Amount',  # selecting the amount-columns
            'Line.TaxAmount.Amount',
            'Line.CreditAmount.Amount',]].sum())

if __name__ == '__main__':
    print(analyse(
        from_and_included_date = '2017-01-01',
        to_date = '2017-02-01',
        from_and_included_account_id = 3000,
        to_account_id = 4000,
        saft_df = saft2dataframe('saft.xml'),        
    ))