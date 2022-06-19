import pandas as pd
import numpy as np

def LoadSurveyData():

    # load raw data
    df_wvs = pd.read_spss('raw_survey_data/WVS_Trend_v2_0.sav', usecols=None, convert_categoricals=False)
    df_evs = pd.read_stata('raw_survey_data/ZA7503_v2-0-0.dta', convert_categoricals=False)

    # ensure that the waves of wvs and evs are seperable
    df_evs = df_evs.rename(columns={'S002EVS':'S002'})
    df_evs['S002'] = ['ev_'+ str(i) for i in df_evs['S002']]
    df_wvs['S002'] = ['wv_'+ str(int(i)) for i in df_wvs['S002']]

    ## all missing vlaues are coded as a negative value, set all these to nans
    N = 15
    missing_value_d = dict(zip([-i for i in range(1,N+1)],[np.nan]*N))
    df_evs = df_evs.replace(missing_value_d)
    df_wvs = df_wvs.replace(missing_value_d)

    #TestAndListCountriesInTheData(df_wvs,df_evs)

    df_evs = UpdateCountryNames(df_evs)
    df_wvs = UpdateCountryNames(df_wvs)

    TestAndListCountriesInTheData(df_wvs,df_evs)

    df_evs = ImputeMissingDoBData(df_evs)
    df_wvs = ImputeMissingDoBData(df_wvs)

    return df_evs, df_wvs

def UpdateCountryNames(X):

    #lookup country names and factor names 
    country_lookup=pd.read_csv('data/country_code.csv',index_col=0).iloc[:,0].to_dict()

    #recode Serbia & Montenegro and Bosnia
    country=X.loc[:,'S003']
    country[country==688]=891
    country[country==499]=891
    country[country==914]=70

    country = country.replace(country_lookup)

    X.loc[:,'S003'] = country

    return X

def TestAndListCountriesInTheData(df_wvs,df_evs):
    c_list = []
    for X in [df_wvs,df_evs]:

        #recode Serbia & Montenegro and Bosnia
        country=X.loc[:,'S003']
        unique_c = country.unique()

        c_list.append(unique_c)

    c_list = np.concatenate(c_list)
    non_str_inputs = c_list[np.asarray([ type(c_list[i]) for i in range(len(c_list)) ]) != str]
    print('countries with no labels: ', non_str_inputs)

    c_list_pd = pd.Series(c_list).unique()
    print('num of countries:', c_list_pd.shape[0])
    print('countries...')
    print(c_list_pd)

def AddMedianSurveyYear(X, wave_median_years):
    # add median survey year (gives a fixed year to a given WVS wave)
    period=X['S002']
    period = period.replace(wave_median_years)
    X['median_survey_year'] = period
    return X


def ImputeMissingDoBData(X):
    year=X.loc[:,'S020']
    age=X.loc[:,'X003']
    dob=X.loc[:,'X002']

    dob2=year-age
    dob[dob.isnull()]=dob2[dob.isnull()]

    X.loc[:,'X002'] = dob

    return X



