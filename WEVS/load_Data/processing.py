import pandas as pd
def BinDateOfBirth(df, bin_edges):
    labels = [ "{bel}-{beh}".format( bel=str(bin_edges[jj]), beh=str(bin_edges[jj+1])) for jj in range(len(bin_edges)-1)]
    df["X002"] = pd.cut(df["X002"], bins = bin_edges, labels = labels)

    return df

def ExtractDemogrpahicVariablesForStudy(df_wvs,df_evs, dem_ques_spec):
    df_dem = pd.concat([df_wvs,df_evs])
    df_dem.index = range(df_dem.shape[0])
    df_dem = df_dem[dem_ques_spec]

    return df_dem