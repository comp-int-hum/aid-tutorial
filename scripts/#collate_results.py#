import argparse
import json
import re
import seaborn

parser = argparse.ArgumentParser()
parser.add_argument("--clusterings", dest="clusterings", nargs="+")
parser.add_argument("--figure", dest="figure")
args = parser.parse_args()

subfigures = []
for fname in args.clusterings:
    confusion = {}
    with open(fname, "rt") as ifd:
        clustering = json.loads(ifd.read())
    for cluster in clustering["clusters"]:
        pass
    conf = {}
    #seaborn.heatmap(conf)
