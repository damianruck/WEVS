import pandas as pd
import os
import numpy as np

from WEVS.load_Data.load_values_and_demographics_dataframes import FilterForCommonQuestions

def GenerateAndSaveRucketalCulturalVariables(df_evs, df_wvs, values_questions, dems_questions, start_wave = 'wv1'):

    e_w_overlap = np.intersect1d(df_evs.columns, df_wvs.columns)
    dem_ques, vals_ques = FilterForCommonQuestions(values_questions, dems_questions, e_w_overlap, start_wave = start_wave)

    vals_ques_with_weight = np.append(vals_ques,'S017') #add the country weight in time for the EFA (THIS IS NOT REQUIRED, I DON"T THINK)
    df = pd.concat([df_wvs,df_evs])[vals_ques_with_weight]

    df.to_csv('raw_survey_data/df_vals_for_compression.csv',index=False)

    # run the exploratory factor analysis in R
    os.system('RScript WEVS/Ruck_etal/compress_with_R.R')

    loadings = pd.read_csv('Ruck_etal/Rucketal_loadings.csv',index_col=0)
    old_cols = loadings.columns.values

    ### rename the factors according to the highly correalted survey questions
    new_cols = ['indv_rights','inst_conf','secular','politic_engage','prosocial','wellbeing','racism']
    print('proposed varaibles labels',new_cols)

    for c,n in zip(old_cols,new_cols):
        c_q = loadings[loadings[c].abs() > 0.3].index.values
        nn='Common Dictionary: Variable name\n\n[Orange cells= variables included in JOINT EVS/WVS\n'
        qq = values_questions[values_questions[nn].isin(c_q)]['Common Dictionary: Variable label\n'].values

        print(n,c)
        top = loadings.loc[c_q,c]
        top.index = qq
        print(top)

        #print(qq)
        print('------------------------')

    # rename factors and normalize the index numbers
    vals = pd.read_csv('Ruck_etal/Rucketal_variables.csv',index_col=0)
    vals = vals.rename(columns = dict(zip(old_cols, new_cols)))

    '''
    We orientate the 7 variables in an intuative way using the loadings are their correlations wioth the original survey questions
    e.g. high numbers for Justifiable: Homosexuality  question corresponds to high tolerance, so high respect for indivual rights
    '''

    orientate_rucketal_d = {'indv_rights':1,'inst_conf':-1,'secular':1,'politic_engage':-1,'prosocial':-1,'wellbeing':1,'racism':1}

    for v in orientate_rucketal_d.keys():
        vals[v] = vals[v]*orientate_rucketal_d[v]

    vals.index = range(vals.shape[0])
    vals.to_csv('Ruck_etal/Rucketal_variables.csv')