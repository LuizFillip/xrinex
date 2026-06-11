import xrinex as rx 
import pandas as pd 
import numpy as np



class rinex2(object):
    
    
    def __init__(self, infile):
        
        self.attrs = rx.headerRINEX2(infile)
        
        self.ob = rx.obs2(self.attrs.lines, self.attrs.num_of_obs)
        
        self.header = self.attrs.attrs
        
    @property
    def prns(self):
        return np.unique(self.ob.prns_list)
        
    def dataset(self, values = 'obs', drop_ssi = True):
        
        if values == 'obs':
            data = self.ob.obs
        elif values == 'lli':
            data = self.ob.lli
        else:
            data = self.ob.ssi 
            
            
        df =  pd.DataFrame(
                data, 
                index = self.ob.time_list,
                columns = self.attrs.obs_names
            )
        
        df['prn'] = self.ob.prns_list
        
        if drop_ssi:
            columns = [col for col in df.columns 
                       if ('S' in col) or 
                       ('D' in col)]
            df = df.drop(columns = columns)
        
        return df
    
    def sel(self, prn):
        
        df = self.dataset(values = 'obs')
        
        
        df = df.loc[df["prn"] == prn]
        
        df = df.loc[:, df.count() != 0].iloc[:, :4]
        
        lli_df = self.dataset(values = 'lli')
        
        lli_df = lli_df.loc[lli_df["prn"] == prn, df.columns]
        lli_df.columns = [f'{c}lli' for c in lli_df.columns]
        
        df_filtered = lli_df[
            [col for col in lli_df.columns 
             if 'L' in col]]

        
        return pd.concat([df, df_filtered], axis = 1).dropna()
            
# def main():
    
# import GNSS as gs 
# import datetime as dt
# dn = dt.datetime(2024, 6, 1, 20)

# path = gs.paths(dn, root = 'F:\\').fn_rinex('salu')

# # infile = 'database/GNSS/rinex/amco0011.23o'

# df = rinex2(path)

# df.dataset()

# # df.attrs 
    
    
    