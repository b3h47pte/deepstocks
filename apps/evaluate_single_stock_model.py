#
# Evaluate a single stock model. Given a date, obtain the stock information and predict the future.
#

import argparse
import datetime
import deepstocks.data
import importlib
import torch
import matplotlib

parser = argparse.ArgumentParser()
parser.add_argument('model', nargs=1)
parser.add_argument('--modelConfig', required=True)
parser.add_argument('--database', required=True)
parser.add_argument('--symbol', required=True)
parser.add_argument('--parameters', required=True)
parser.add_argument('--date')
parser.add_argument('--groundtruth', action='store_true')

args = parser.parse_args()

deepstocks.data.connectToDatabase(args.database)
session = deepstocks.data.createSession()

modelClsName = args.model[0]
print('Evaluating Model {0}'.format(modelClsName))
splitName = modelClsName.split('.')
fullModuleName = 'deepstocks.models.single_stock.' + '.'.join(splitName[:-1])
pyModule = importlib.import_module(fullModuleName)
modelCls = getattr(pyModule, splitName[-1])

config = modelCls.ConfigType.loadFromDisk(args.modelConfig)

model = modelCls(config=config)
model.cuda()

model.load_state_dict(torch.load(args.parameters))
model.eval()

# Load data from database. Assume we have all the relevant data for now.
dataset = modelCls.Dataset(session=session, symbol=args.symbol, config=config)

date = datetime.datetime.strptime(args.date, '%Y-%m-%d') if args.date is not None else datetime.datetime.now()
inputTensor, inputDates = dataset.getInputForDate(date)
outputTensor = model(inputTensor.cuda())

if args.groundtruth:
    targetTensor, targetDates = dataset.getTargetForDate(date)

    criterion = torch.nn.MSELoss()
    loss = criterion(outputTensor.cuda(), targetTensor.cuda())
else:
    targetDates = [date]
    startDate = date
    for i in range(outputTensor.size()[0] - 1):
        startDate += datetime.timedelta(days=1)
        targetDates.append(startDate)
assert(len(targetDates) == outputTensor.size()[0])

print('PREDICTING PRICES FOR {0}'.format(args.symbol))
for idx, dt in enumerate(targetDates):
    print('{0}: {1:.03f}'.format(dt.strftime('%Y-%m-%d'), outputTensor[idx].item()))
    if args.groundtruth:
        print('  Truth: {0:.03f}'.format(targetTensor[idx].item()))
