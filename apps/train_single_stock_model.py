#
# Train any of the models found in deepstocks.models.single_stock.
# Assumes that we only try to predict one stick's price from its past historical data.
#

import argparse
import deepstocks.data
import importlib
import matplotlib.pyplot as plt
import os
import torch
import torch.optim

parser = argparse.ArgumentParser()
parser.add_argument('model', nargs=1)
parser.add_argument('--modelConfig', required=True)
parser.add_argument('--database', required=True)
parser.add_argument('--outputDir', required=True)
parser.add_argument('--symbol', required=True)
parser.add_argument('--epochs', type=int, default=100)
parser.add_argument('--learningRate', type=float, default=1e-5)
parser.add_argument('--momentum', type=float, default=0.9)

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

criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=args.learningRate, momentum=args.momentum)

allTrainingLoss = []
allValidationLoss = []

def doGraph(fname, trainingLosses, validationLosses):
    numEpochs = len(trainingLosses)
    assert(len(validationLosses) == numEpochs)

    plt.clf()
    plt.plot(range(numEpochs), trainingLosses, label='Train', color='red')
    plt.plot(range(numEpochs), validationLosses, label='Validation', color='cyan')
    plt.legend(loc='best')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.savefig(fname)

lrScheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.98)
for epoch in range(args.epochs):
    print('====== EPOCH {0} ====='.format(epoch))
    # Training loss averaged over the entire training datatset.
    trainingLoss = 0.0
    for i, data in enumerate(torch.utils.data.DataLoader(trainDataset, batch_size=4, shuffle=True)):
        inputTensor, targetTensor = data
        inputTensor = inputTensor.cuda()
        targetTensor = targetTensor.cuda()

        outputTensor = model(inputTensor)
        optimizer.zero_grad()

        loss = criterion(outputTensor, targetTensor)
        trainingLoss += loss.item()
        loss.backward()

        optimizer.step()
    trainingLoss /= len(trainDataset)
    lrScheduler.step()

    # Validation loss averaged over the entire validation dataset.
    validationLoss = 0.0
    for i, data in enumerate(torch.utils.data.DataLoader(validationDataset, batch_size=4, shuffle=True)):
        inputTensor, targetTensor = data
        inputTensor = inputTensor.cuda()
        targetTensor = targetTensor.cuda()

        outputTensor = model(inputTensor)
        loss = criterion(outputTensor, targetTensor)
        validationLoss += loss.item()
    validationLoss /= len(validationDataset)

    # Output graphs to disk and losses to CLI.
    # Also output model.
    print('Training Loss: {0:06f}'.format(trainingLoss))
    print('Validation Loss: {0:06f}'.format(validationLoss))
    allTrainingLoss.append(trainingLoss)
    allValidationLoss.append(validationLoss)

    doGraph(os.path.join(modelDir, 'lossGraph_{0:04d}.png'.format(epoch)), allTrainingLoss, allValidationLoss)

    torch.save(model.state_dict(), os.path.join(modelDir, 'model_{0:04d}.pth'.format(epoch)))

# Final evaluation of test loss
testLoss = 0.0
for i, data in enumerate(torch.utils.data.DataLoader(testDataset, batch_size=4, shuffle=True)):
    inputTensor, targetTensor = data
    inputTensor = inputTensor.cuda()
    targetTensor = targetTensor.cuda()

    outputTensor = model(inputTensor)
    loss = criterion(outputTensor, targetTensor)
    testLoss += loss.item()
testLoss /= len(testDataset)

print('Final Training Loss: {0:06f}'.format(allTrainingLoss[-1]))
print('Final Validation Loss: {0:06f}'.format(allValidationLoss[-1]))
print('Final Test Loss: {0:06f}'.format(testLoss))
