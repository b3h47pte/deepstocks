#
# Utilities for reading in information of a company off the disk.
#

def readCompanyString(line):
    data = line.split('\t')

    if len(data) != 3:
        return None, None, None
    company = data[0]

    sym = data[1]
    symSplit = sym.split(':')
    if len(symSplit) == 2:
        symbol = symSplit[1]
    else:
        symbol = sym

    industry = data[2]
    return company, symbol, industry

# Returns 3 lists (companies, symbols, industries)
def readCompanyList(fname):
    from .company_db import Company

    companies = []
    symbols = []
    industries = []
    with open(fname, 'r') as f:
        for line in f:
            c, s, i = readCompanyString(line)
            if c is None:
                continue
            companies.append(c)
            symbols.append(s)
            industries.append(i)
    return companies, symbols, industries

# Searches for the company name(s)/symbol(s) that best matches the input
# Returns a list of dicts with the form {name: 'NAME', symbol: 'SYMBOL'}.
def findClosestNameSymbolMatch(session, inp, limit=10):
    from .company_db import Company
    from sqlalchemy import or_

    match = '%{0}%'.format(inp)
    results = session.query(Company) \
        .filter(
            or_(
                Company.name.ilike(match),
                Company.symbol.ilike(match))) \
        .limit(limit) \
        .all()

    return [{'name': c.name, 'symbol': c.symbol} for c in results]
