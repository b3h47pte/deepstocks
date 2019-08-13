#
# Train any of the models found in deepstocks.models.single_stock.
# Assumes that we only try to predict one stick's price from its past historical data.
#

import argparse
import deepstocks.data
import importlib
import os
import torch

parser = argparse.ArgumentParser()
parser.add_argument('model', nargs=1)
parser.add_argument('--modelConfig', required=True)
parser.add_argument('--database', required=True)
parser.add_argument('--outputDir', required=True)
parser.add_argument('--symbol', required=True)

args = parser.parse_args()

deepstocks.data.connectToDatabase(args.database)
session = deepstocks.data.createSession()

os.makedirs(args.outputDir, exist_ok=True)

# Determine which model we should import and use.
modelClsName = args.model[0]
print('Training Model {0}'.format(modelClsName))
splitName = modelClsName.split('.')
fullModuleName = 'deepstocks.models.single_stock.' + '.'.join(splitName[:-1])
pyModule = importlib.import_module(fullModuleName)
modelCls = getattr(pyModule, splitName[-1])

# Load model configuration from disk.
# Assume all models have a 'ConfigType' class attribute which
# in turn has a class function that loads itself from disk.
config = modelCls.ConfigType.loadFromDisk(args.modelConfig)

model = modelCls(config=config)
model.cuda()

# Create appropriately named output directory.
modelDir = os.path.join(args.outputDir, model.modelName())
os.makedirs(modelDir, exist_ok=True)

# Create datasetwhich will handle loading in the data from the database
# and creating the train/validation/test sets.
dataset = modelCls.Dataset(session=session, symbol=args.symbol, config=config)

trainLength = int(len(dataset) * 0.6)
validationLength = int(len(dataset) * 0.2)
testLength = len(dataset) - trainLength - validationLength

trainDataset, validationDataset, testDataset = torch.utils.data.random_split(dataset, lengths=[trainLength, validationLength, testLength])
