import pandas as pd
import numpy as np

def LoadValuesAndDemographicsDataFrames():
    '''
    we reclassify these as sociodemographic variables

    'S002': 'Wave',
    'S003': 'Country (ISO 3166-1 Numeric code)',
    'S017': 'Weight',
    'S020': 'Year survey',
    'E033': 'Self positioning in political scale',
    'F025': 'Religious denomination (major groups)'
    '''

    cols = ['Common Dictionary: Thematic category\n',
          'Common Dictionary: Variable name\n\n[Orange cells= variables included in JOINT EVS/WVS\n',
          'Common Dictionary: Variable label\n', 'WVS 1: Variable name',
          'WVS 2: Variable name', 'WVS 3: Variable name', 'WVS 4: Variable name',
          'WVS 5: Variable name', 'WVS 6: Variable name', 'WVS 7: Variable name',
            'EVS 1981: Variable name', 'EVS 1990: Variable name',
          'EVS 1999: Variable name', 'EVS 2008: Variable name',
          'EVS 2017: Variable name'
      ]

    # load the question-wave data
    questions = pd.read_excel('data/F00011424-Common_EVS_WVS_Dictionary_IVS.xlsx', sheet_name=2,index_col=0)

    #change religious and political affiliation (plus a few others) to socidemographics variables
    ii = questions[questions['Common Dictionary: Variable name\n\n[Orange cells= variables included in JOINT EVS/WVS\n'].isin(
        ['E033','F025', 'S020', 'S003', 'S017','S002'])].index

    questions['Common Dictionary: Thematic category\n'].loc[ii] = 'Socio demographics'

    # new_socio_ques = questions[questions.iloc[:,1].isin(['E033','F025', 'S020', 'S003', 'S017','S002'])]
    # new_socio_ques.index = new_socio_ques.iloc[:,1].values
    # new_socio_ques.iloc[:,2].to_dict()

    questionsF = questions[cols]
    print('themes in the data...')
    print(questionsF['Common Dictionary: Thematic category\n'].unique())

    # sort the values categories from the socioeconomic variables 
    values_ques = ['Perceptions of life', 'Environment', 'Work ',
    'Family ', 'Politics and Society', 'Religion and Morale',
    'National Identity', 'Security ', 'Science ']# , "Respondent's parents (EVS) ", "Respondent's partner (EVS) "]

    demographics = ['Socio demographics']#,'Admin/protocol variables']
    #demographics = ['Admin/protocol variables']

    #seperate values and demogrpahics df. Essential for Ruck et al variable extraction
    values_questions = questionsF[questionsF['Common Dictionary: Thematic category\n'].isin(values_ques)]

    dems_questions = questionsF[questionsF['Common Dictionary: Thematic category\n'].isin(demographics)]
    dems_questions.loc[7,['EVS 1981: Variable name', 'EVS 1990: Variable name',
          'EVS 1999: Variable name', 'EVS 2008: Variable name',
          'EVS 2017: Variable name']] = 'djub'

    return values_questions, dems_questions

def FilterForCommonQuestions(values_questions, dems_questions, start_wave = 'wv1'):

    '''
    start_wave = 'wv1' or 'wv2'
    '''

    order_ques = ['EVS 1981: Variable name','WVS 1: Variable name', 
        'EVS 1990: Variable name','WVS 2: Variable name', 
    'WVS 3: Variable name', 
    'EVS 1999: Variable name', 'WVS 4: Variable name',
        'EVS 2008: Variable name','WVS 5: Variable name', 
    'WVS 6: Variable name', 
            'EVS 2017: Variable name','WVS 7: Variable name',
        ]

    e_w_overlap = pd.read_csv('data/overlapping_questions_WVS_and_EVS.csv').iloc[:,0].values

    if start_wave=='wv1':
        missing_num = 0
    if start_wave=='wv2':
        missing_num = 2

    values_questions2 = values_questions[values_questions.columns[values_questions.columns.isin(order_ques[missing_num:])]]
    ii = values_questions[values_questions2.isnull().sum(1) <= 0]
    print('number of values_questions: ',ii['Common Dictionary: Variable label\n'].shape[0])

    dems_questions2 = dems_questions[dems_questions.columns[dems_questions.columns.isin(order_ques[missing_num:])]]
    ii_dem = dems_questions[dems_questions2.isnull().sum(1) <= 4]
    print("the demographic variables in the data ...")
    print(ii_dem['Common Dictionary: Variable label\n'].values)

    vals_ques = ii["Common Dictionary: Variable name\n\n[Orange cells= variables included in JOINT EVS/WVS\n"]
    dem_ques = ii_dem["Common Dictionary: Variable name\n\n[Orange cells= variables included in JOINT EVS/WVS\n"]

    dem_ques = np.intersect1d(e_w_overlap, dem_ques)
    vals_ques = np.intersect1d(e_w_overlap, vals_ques)

    return dem_ques, vals_ques