## Authors: @riverseb
import pandas as pd
import matplotlib.pyplot as plt
from PNear import main as pnear_main
def clean_and_read_score_file(file_path):
    """
    Clean and read Rosetta score file.

    :param file_path: The file path to the score file.
    :return: The dataframe containing scores and model names.
    """
    
    # Read the file into a pandas dataframe
    df = pd.read_csv(file_path, sep='\s+', header=0)
    
    # Remove the first column and row
    if df.iloc[0,0] == "SCORE:":
        df = df.iloc[:, 1:]
    elif df.iloc[0,0] == "SEQUENCE:":
        df = df.iloc[1:, 1:]
    scores_descriptions = df[['total_score', 'description']]
    return scores_descriptions


def join_rmsd_scores(rmsd_path, scores_descriptions):
    """
    Join RMSD scores with Rosetta energy scores by model name.

    :param rmsd_path: The file path to the RMSD scores.
    :param scores_descriptions: The dataframe containing scores and model names.
    :return: The merged dataframe containing RMSD scores and energy scores and model names.
    """
    rmsd_df = pd.read_csv(rmsd_path, delimiter='\t', header=0)
    rmsd_and_scores = rmsd_df.merge(scores_descriptions, on='description')
    with open('rmsd_and_scores.csv', 'w') as f:
        f.seek(0)
        rmsd_and_scores.to_csv(f, index=False, sep='\t', mode="w")
        f.truncate()
    # rmsd_and_scores.to_csv('rmsd_and_scores.csv', index=False, sep='\t', mode="w")
    return rmsd_and_scores
def rmsd_vs_score_plot(rmsd_and_scores, ref_name):
    """
    Generate rmsd vs score plot using matplotlib. Also calculates PNear and confidence interval
    and includes it as an inset on the plot.

    :param rmsd_and_scores: The merged dataframe containing RMSD scores and energy scores and model names.
    :param ref_name: The reference pdb name.
    """
    fig, ax = plt.subplots(figsize=(6.5, 4.1))
    # Plot rmsd vs total score
    rmsd_and_scores.plot.scatter(x='rmsd', y='total_score', ax=ax)
    
    y_min, y_max = ax.get_ylim()
    x_position = 9.9
    y_position = y_min + 1
    bbox_props = dict(boxstyle="round,pad=0.3", fc="w", ec="r", lw=2)
    pnear, CI = pnear_main(rmsd_and_scores, bootstrap_n=750, lambda_val=2)
    ax.text(x_position, y_position, f"PNear: {pnear:.2f} (CI 95%:[{CI[0]:.3f} - {CI[1]:.3f}])", 
            fontsize=13, ha="right", va="bottom", bbox=bbox_props, transform=ax.transData)
    ax.set_xlabel('RMSD ($\AA$)', fontsize=20, labelpad=10)
    ax.set_ylabel('Total Score (REU)', fontsize=20, labelpad=10)
    ax.set_xlim(0, 10)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.set_title('Total Score vs RMSD', fontsize=20)
    plt.tight_layout()
    plt.savefig(f'rmsd_vs_score_{ref_name}.png', dpi=300)
    best_model = rmsd_and_scores.iloc[0]
    return pnear, CI, best_model

def main(rmsd_path, ref_name, score_path='scores/fullscore_sorted.sc', outfile=None):
    scores_descriptions = clean_and_read_score_file(score_path)
    rmsd_and_scores = join_rmsd_scores(rmsd_path, scores_descriptions)
    pnear, CI, best_model = rmsd_vs_score_plot(rmsd_and_scores, ref_name)
    if outfile:
        with open(outfile, 'w') as f:
            f.seek(0)
            f.write(f'pnear\tCI_lower\tCI_upper\tlowest rmsd model\tscore\trmsd\n')
            f.write(f'{pnear}\t{CI[0]}\t{CI[1]}\t{best_model["description"]}\t' +
                    f'{best_model["total_score"]}\t{best_model["rmsd"]}\n')
            f.truncate()
    return pnear, CI, best_model
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(usage='python rmsd-vs-score.py <path_to_score_file>')
    
    parser.add_argument('rmsd_path', help='Path to rmsd file')
    parser.add_argument('ref_name', help='Reference pdb name')
    parser.add_argument('--score_path', help='Path to score file', default='scores/fullscore_sorted.sc')
    args = parser.parse_args()
    
    main(**vars(args))
