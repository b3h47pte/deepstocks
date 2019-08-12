#
# Takes in company lists with format:
# 
# company1	symbol1	industry1
# company2	symbol2	industry2
# ...
# companyN	symbolN	industryN
#
# And takes in unique companies and outputs data in the database.

import argparse
import deepstocks.data
import sqlalchemy.ext

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--database', required=True)
args = parser.parse_args()

# Read in company data. companies/symbols/industries are not unique (yet).
companies = []
symbols = []
industries = []
for fname in args.files:
    lcompanies, lsymbols, lindustries = deepstocks.data.readCompanyList(fname)

    companies.extend(lcompanies)
    symbols.extend(lsymbols)
    industries.extend(lindustries)

# Add to database. Use the database to enforce uniqueness of the read in data.
deepstocks.data.connectToDatabase(args.database)
session = deepstocks.data.createSession()

# First add in industries.
industryMap = {}
for ind in set(industries):
    obj = deepstocks.data.Industry(name=ind)
    session.add(obj)

    # If we've seen the industry before we can just ignore it.
    # Assume no other error happened.
    try:
        session.commit()
    except:
        session.rollback()

# Next add in companies
for idx in range(len(companies)):
    comp = companies[idx]
    symb = symbols[idx]
    ind = industries[idx]

    with session.no_autoflush:
        obj = deepstocks.data.Company(
            name=comp,
            symbol=symb,
            industry=session.query(deepstocks.data.Industry).filter_by(name=ind).one())

    session.add(obj)

    try:
        session.commit()
    except:
        session.rollback()
