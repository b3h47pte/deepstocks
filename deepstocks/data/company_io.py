#
# Utilities for reading in information of a company off the disk.
#


def readCompanyList(fname):
    from .company import Company

    companies = []
    with open(fname, 'r') as f:
        for line in f:
            data = line.split('\t')
            if len(data) == 2:
                companies.append(Company(data[0], data[1]))
    return companies
