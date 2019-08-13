#
# Adds historical stock price data to the database.
#
# Can either use all existing companies in the database, a specific company in the database, or a new company.

import argparse
import deepstocks.data

parser = argparse.ArgumentParser()
parser.add_argument('database', nargs=1)
parser.add_argument('--single', type=str) # SYMBOL
parser.add_argument('--new', type=str) # COMPANY\tSYMBOL\tINDUSTRY
args = parser.parse_args()

deepstocks.data.connectToDatabase(args.database[0])
session = deepstocks.data.createSession()

# Parse arguments to see which companies we want to grab stock data for.
if args.single is not None:
    companies = [session.query(deepstocks.data.Company).filter_by(symbol=args.single).one()]
elif args.new is not None:
    company, symbol, industry = deepstocks.data.readCompanyString(args.new)

    if not session.query(deepstocks.data.Industry).filter_by(name=industry).exists():
        session.add(deepstocks.data.Industry(name=industry))
        session.commit()

    companyQuery = session.query(deepstocks.data.Company).filter_by(symbol=symbol)
    if not companyQuery.exists():
        companies = [
            deepstocks.data.Company(
                name=company,
                symbol=symbol,
                industry=session.query(deepstocks.data.Industry).filter_by(name=industry).one())]
        session.add(companies[0])
        session.commit()
    else:
        companies = [companyQuery.one()]
else:
    companies = session.query(deepstocks.data.Company).all()

# Grab historical stock data from API
# Skip if company already has data in it.
for c in companies:
    print('STOCK DATA FOR {0}'.format(c.name))
    if c.equity:
        print('Skipping {0}'.format(c.name))
        continue

    stockPrices = deepstocks.data.getHistoricalStockPrice(c.symbol)
    for sDatum in stockPrices:
        newStock = deepstocks.data.Equity(
            dateTime=sDatum.dateTime,
            company=c,
            price=sDatum.price,
            volume=sDatum.volume)
        session.add(newStock)
    session.commit()
