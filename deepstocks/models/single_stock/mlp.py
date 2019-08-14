#
# Input: N days of price data
# Output: M days of future price data
#

import torch
from .linear import LinearSingleStock, LinearSingleStockConfig, LinearSingleStockDataset

class MLPSingleStockConfig(object):
    def __init__(self, inputOutput, hiddenLayers, hiddenLayerWidths, useReLU):
        self.inputOutput = inputOutput
        self.hiddenLayers = hiddenLayers
        assert len(hiddenLayerWidths) == self.hiddenLayers
        self.hiddenLayerWidths = hiddenLayerWidths
        self.useReLU = useReLU

    @classmethod
    def loadFromDisk(cls, fname):
        import json 

        with open(fname, 'r') as f:
            data = json.load(f)
        return cls.loadFromJson(data)

    @classmethod
    def loadFromJson(cls, data):
        return cls(
            inputOutput=LinearSingleStockConfig.loadFromJson(data['inputOutput']),
            hiddenLayers=data['hiddenLayers'],
            hiddenLayerWidths=data['hiddenLayerWidths'],
            useReLU=data['useReLU'])

class MLPSingleStockDataset(LinearSingleStockDataset):
    def __init__(self, session, symbol, config):
        super(MLPSingleStockDataset, self).__init__(session, symbol, config.inputOutput)

class MLPSingleStock(torch.nn.Module):
    ConfigType = MLPSingleStockConfig
    Dataset = MLPSingleStockDataset

    def __init__(self, config):
        assert isinstance(config, MLPSingleStock.ConfigType)
        super(MLPSingleStock, self).__init__()
        self._config = config
        self._layers = []

        if config.hiddenLayers == 0:
            self._layers.append(torch.nn.Linear(config.inputOutput.inputN, config.inputOutput.outputM))
        else:
            self._layers.append(torch.nn.Linear(config.inputOutput.inputN, config.hiddenLayerWidths[0]))
            if self._config.useReLU:
                self._layers.append(torch.nn.ReLU())

            for i in range(0, config.hiddenLayers - 1):
                self._layers.append(torch.nn.Linear(config.hiddenLayerWidths[i], config.hiddenLayerWidths[i+1]))
                if self._config.useReLU:
                    self._layers.append(torch.nn.ReLU())

            self._layers.append(torch.nn.Linear(config.hiddenLayerWidths[-1], config.inputOutput.outputM))
        
        self._model = torch.nn.Sequential(*self._layers)

    def forward(self, x):
        return self._model(x)

    def modelName(self):
        return 'MLP_Input{N}_H{H}_Output{M}'.format(N=self._config.inputOutput.inputN, H=self._config.hiddenLayers, M=self._config.inputOutput.outputM)

