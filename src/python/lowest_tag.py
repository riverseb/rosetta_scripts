import os 
import argparse
def low_tag_parse(silent_file):
    scores_tags = []
    with open(silent_file, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith("SCORE: ") and not line.startswith("SCORE:     score"):
            split_line = line.split()
            score = split_line[1]
            # print(score)
            tag_line_split = lines[i + 1].split()
            tag = tag_line_split[-1]
            # print(tag)
            scores_tags.append([float(score), tag])
        else:
            continue
    scores_tags.sort(key=lambda x: float(x[0]))
    # print(scores_tags)
    return scores_tags[0][1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("silent_file", type=str, help="silent file")
    args= parser.parse_args()
    low_tag = low_tag_parse(**vars(args))
    print(low_tag)
