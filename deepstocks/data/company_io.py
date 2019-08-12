#
# Utilities for reading in information of a company off the disk.
#

# Returns 3 lists (companies, symbols, industries)
def readCompanyList(fname):
    from .company_db import Company

    companies = []
    symbols = []
    industries = []
    with open(fname, 'r') as f:
        for line in f:
            data = line.split('\t')
            if len(data) == 3:
                companies.append(data[0])

                sym = data[1]
                symSplit = sym.split(':')
                if len(symSplit) == 2:
                    symbols.append(symSplit[1])
                else:
                    symbols.append(sym)
                industries.append(data[2])
    return companies, symbols, industries
