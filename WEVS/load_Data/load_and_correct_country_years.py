import pandas as pd
import numpy as np
def LoadAndCorrectCountryYears():

       # load country codes
       countrys = pd.read_excel('data/F00011426-EVS_WVS_ParticipatingCountries.xlsx', sheet_name=1,index_col=0)

       current_labels = ['1981 - 1984', 'Unnamed: 2', '1989 - 1993', 'Unnamed: 4', '1994 - 1998',
              '1999 - 2004', 'Unnamed: 7', '2005 - 2009', '2008 - 2010', '2010-2014',
              '2017-2020', 'Unnamed: 12']

       new_labels = ['ev_1','wv_1','ev_2','wv_2', 'wv_3','ev_3','wv_4','wv_5', 'ev_4', 'wv_6','ev_5','wv_7']
       countrys = countrys.rename(columns=dict(zip(current_labels, new_labels))).iloc[1:,:]

       # for surveys carried out over mutiple years, use the completed year 
       double_year_d = {'1997/1998':1998, '1995/1996':1996, '2008/2009':2009 ,'2009/2010':2010, '2017/2018':2018, '2018/2019' :2019, '2019/2020': 2020}

       # ssome years do not fall in side the expected window, we assume these are errors, so move to the expected limit 
       # (e.g. surveys stated to have been conducted in 2010 in wave 7 of the WVS are moved to 2016)
       mistakes_ = {'wv_6': {2018:2015}, 'wv_7': {2010:2016}}

       for cl in new_labels:
              years = countrys[cl]

              years = years.replace(double_year_d)

              if cl in mistakes_.keys():
                     years = years.replace(mistakes_[cl])
              
              yy = years.dropna().unique()
              print(cl, yy)

              countrys[cl] = years

       return countrys