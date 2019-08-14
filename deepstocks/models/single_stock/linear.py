from deepstocks.data import Equity, Company
import math
import torch

#
# Input: N days of price data
# Output: M days of future price data
#

class LinearSingleStockConfig(object):
    def __init__(self, inputN, outputM):
        self.inputN = inputN
        self.outputM = outputM

    @classmethod
    def loadFromDisk(cls, fname):
        import json 

        with open(fname, 'r') as f:
            data = json.load(f)
        return cls(int(data['inputN']), int(data['outputM']))

class LinearSingleStockDataset(torch.utils.data.Dataset):
    def __init__(self, session, symbol, config):

        self._symbol = symbol
        self._config = config
        self._baseQuery = session.query(Equity).join(Equity.company).filter_by(symbol=self._symbol)
        self._ascQuery = self._baseQuery.order_by(Equity.dateTime.asc())
        self._descQuery = self._baseQuery.order_by(Equity.dateTime.desc())

        # Determine how many pieces of data we have after
        # accounting for the fact that we need N days of
        # pre-data and M days of post-data. ASSUME DATA
        # IS CONTIGUOUS IN DAYS.
        self._totalDataCount = int(self._baseQuery.count())
        self._totalSampleCount = self._totalDataCount - self._config.inputN - self._config.outputM

        self._ascCached = self._ascQuery.all()

    def __getitem__(self, idx):
        # Input goes from idx to idx + inputN
        # Output goes from idx + inputN to indx + inputN + outputM
        inputStock = self._ascCached[idx:idx + self._config.inputN]
        targetStock = self._ascCached[idx + self._config.inputN:idx + self._config.inputN + self._config.outputM]

        inputTensor = torch.FloatTensor([x.price for x in inputStock])
        targetTensor = torch.FloatTensor([x.price for x in targetStock])
        return inputTensor, targetTensor

    def __len__(self):
        return self._totalSampleCount

    def getInputForDate(self, date):
        stocks = list(reversed(self._descQuery.filter(Equity.dateTime < date).limit(self._config.inputN).all()))
        assert(len(stocks) == self._config.inputN)
        return torch.FloatTensor([s.price for s in stocks]), [s.dateTime for s in stocks]

    def getTargetForDate(self, date):
        stocks = self._ascQuery.filter(Equity.dateTime >= date).limit(self._config.outputM).all()
        assert(len(stocks) == self._config.outputM)
        return torch.FloatTensor([s.price for s in stocks]), [s.dateTime for s in stocks]

class LinearSingleStock(torch.nn.Module):
    ConfigType = LinearSingleStockConfig
    Dataset = LinearSingleStockDataset

    def __init__(self, config):
        assert isinstance(config, LinearSingleStockConfig)
        super(LinearSingleStock, self).__init__()
        self._config = config
        self._linearLayer = torch.nn.Linear(config.inputN, config.outputM)

    def forward(self, x):
        return self._linearLayer(x)

    def modelName(self):
        return 'LinearSingleStock_Input{N}_Output{M}'.format(N=self._config.inputN, M=self._config.outputM)
