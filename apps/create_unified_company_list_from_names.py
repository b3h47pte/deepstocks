#
# Takes in company lists with format:
# 
# company1	symbol1
# company2	symbol2
# ...
# companyN	symbolN
#
# And takes in unique companies and outputs data in a binary pickle format.

import argparse
import deepstocks.data
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--output', required=True)
args = parser.parse_args()

companies = set()
for fname in args.files:
    companies.update(deepstocks.data.readCompanyList(fname))

with open(args.output, 'wb') as f:
    pickle.dump(companies, f)
