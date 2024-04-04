#Authors: @riverseb
import pandas as pd
from numpy import array
from numpy import exp
import sklearn.utils as sk
from scipy import stats
import argparse
# calculate funnel-likeness of rmsd vs score plots using PNear calculation
def calculate_pnear( scores, rmsds, lambda_val=2.0, kbt=0.62 ) :                                                                                                                                            
    nscores = len(scores)                                                                                                                                                                                   
    assert nscores == len(rmsds), "Error in calculate_pnear(): The scores and rmsds lists must be of the same length."                                                                                      
    assert nscores > 0, "Error in calculate_pnear(): At least one score/rmsd pair must be provided."                                                                                                        
    assert kbt > 1e-15, "Error in calculate_pnear(): kbt must be greater than zero!"                                                                                                                        
    assert lambda_val > 1e-15, "Error in calculate_pnear(): lambda must be greater than zero!"                                                                                                              
    minscore = min( scores )                                                                                                                                                                                
    weighted_sum = 0.0                                                                                                                                                                                      
    Z = 0.0                                                                                                                                                                                                 
    lambdasq = lambda_val * lambda_val                                                                                                                                                                      
    for i in range( nscores ) :                                                                                                                                                                             
        val1 = exp( -( rmsds[i] * rmsds[i] ) / lambdasq )                                                                                                                                                   
        val2 = exp( -( scores[i] - minscore ) / kbt )                                                                                                                                                       
        weighted_sum += val1*val2                                                                                                                                                                           
        Z += val2                                                                                                                                                                                           
    assert Z > 1e-15, "Math error in calculate_pnear()!  This shouldn't happen."                                                                                                                            
    pnear = weighted_sum/Z
    rounded_float = float(f"{round(pnear, 2):.2f}")  
    return rounded_float  
                                      
# bootstrap resample and calculate PNear for each resample
def bootstrap_pnear_peptide(data_frame, x_column, y_column, bootstrap_n=1000, lambda_val=2.0, kbt=0.62):                                                                                                                                                    
                                                                                                                                                                                                            
    bootstrap_vals = []                                                                                                                                                                                     
    # Extract data from DataFrame
    x_data = data_frame[x_column].astype(float)
    y_data = data_frame[y_column].astype(float)

    # Find the minimum value in the y column
    # min_y = min(y_data)
    min_x = min(x_data)
    ref_energy = data_frame.loc[data_frame[x_column] == min_x, y_column].values[0]
    
    
    # filtered_data = data_frame[data_frame[y_column] >= ref_energy]
    # filtered_data.reset_index(drop=True, inplace=True)
    #filtered_data = data_frame                                            
    landscape_df = data_frame.loc[:, [x_column, y_column]]
    landscape_df.reset_index(drop=True, inplace=True)
    #need to find ref RMSD and put it back in the resample...                                                                                                                                               
    landscape_df = landscape_df.sort_values([x_column],                                                                                                                                                      
                                            ascending=True)                                                                                                                                                 
    reference_ligand = landscape_df.iloc[0:1]                                                                                                                                                               
    landscape_df = landscape_df.iloc[1: , :]                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                   
    for x in range(bootstrap_n + 1):                                                                                                                                                                        
        if x % 150 == 0:                                                                                                                                                                                    
            print("now on bootstrap step: " + str(x))                                                                                                                                   
                                                                                                                                                                                                            
        boot_df = sk.resample(landscape_df,                                                                                                                                                                
                              replace=True,                                                                                                                                                                
                              n_samples=None,                                                                                                                                                             
                              random_state=None,                                                                                                                                                           
                              stratify=None)                                                                                                                                                                
        boot_w_ref = [boot_df, reference_ligand]                                                                                                                                                            
        bootref_df = pd.concat(boot_w_ref)
        bootref_df = bootref_df.sort_values([x_column], ascending=True)                                                                                                                                             
        # print(bootref_df.iloc[0:1])                                                                                                                                                             
                                                                                                                                                                                                            
        bootref_df = bootref_df.reset_index()
        pnear = calculate_pnear(bootref_df[y_column].astype(float),                                                                                                                                     
                                bootref_df[x_column].astype(float), lambda_val=lambda_val, kbt=kbt)                                                                                                                                           
                                                                                                                                                                                                            
        bootstrap_vals.append(pnear)                                                                                                                                                                        
                                                                                                                                                                                                            
    bootstraped_pnears_df = pd.DataFrame(bootstrap_vals, columns=["pnear_vals"])                                                                                                                            
    print(bootstraped_pnears_df)                                                                                                                                                                                                        
    return bootstraped_pnears_df    
def subsample_pnear(rmsd_vs_score, n_samples=100, cycles=100, lambda_val=2.0, kbt=0.62):
    with open("pnear_subsampling.csv", "w") as f:
        f.write("index,pnear\n")
        for i in range(cycles):
            if i % 10 == 0: print("now on subsample step: " + str(i))
            rmsd_score_subsample = rmsd_vs_score.sample(n=n_samples)
            rmsd_score_subsample.reset_index(drop=True, inplace=True)
            pnear = calculate_pnear(rmsd_score_subsample['total_score'].astype(float), 
                                    rmsd_score_subsample['rmsd'].astype(float), 
                                    lambda_val=lambda_val, kbt=kbt)
            f.write(f"{i},{pnear}\n")
            
# calculate confidence interval of PNear using bootstrap resampled data
def calc_PNear_CI(df, confidence=0.95):
    mean = df['pnear_vals'].mean()
    sem = df['pnear_vals'].sem()
    confintv = stats.t.interval(confidence, df=len(df)-1, loc=mean, scale=sem)
    return confintv

def main(rmsd_vs_score, bootstrap_n=1000, confidence=0.95, lambda_val=2, kbt=0.62, subsample=False):
    pnear = calculate_pnear(rmsd_vs_score['total_score'].astype(float), rmsd_vs_score['rmsd'].astype(float), lambda_val=lambda_val, kbt=kbt)
    if subsample:
        subsample_pnear(rmsd_vs_score, n_samples=100, cycles=100, lambda_val=lambda_val, kbt=kbt)
    else:
        bootstraped_pnears_df = bootstrap_pnear_peptide(rmsd_vs_score, 'rmsd', 'total_score', bootstrap_n=bootstrap_n, lambda_val=lambda_val, kbt=kbt)
        confintv = calc_PNear_CI(bootstraped_pnears_df, confidence)
        return pnear, confintv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--rmsd_path', type=str, required=True)
    parser.add_argument('--bootstrap_n', type=int, default=1000)
    parser.add_argument('--confidence', type=float, default=0.95)
    parser.add_argument('--lambda_val', type=float, default=2)
    parser.add_argument('--kbt', type=float, default=0.62)
    parser.add_argument('--subsample', action="store_true", default=False)
    args = parser.parse_args()
    rmsd_vs_score = pd.read_csv(args.rmsd_path, header=0, sep='\t')
    if args.subsample:
        main(rmsd_vs_score, args.bootstrap_n, args.confidence, args.lambda_val, args.kbt, args.subsample)
    else:
        pnear, CI = main(rmsd_vs_score, args.bootstrap_n, args.confidence, args.lambda_val, args.kbt, args.subsample)









