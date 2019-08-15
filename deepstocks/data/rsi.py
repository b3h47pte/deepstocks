#
# Utilities for computing RSI.
#
from collection import deque
import math

# For now, compute the RSI for every datapoint in the company.
# Returns this as a list of (RSI value, Date) tuples.
# For a given time t, we can compute:
# RS_t = avg Gain_t / avg Loss_t where gain and loss are summed over a period of size N
# RSI_t = 100 - 100 / (1 + RS_t)
# We compute the avg gain and loss using a smoothed moving average.
import deepstocks.math.moving_average as ma

def computeRSI(company, period=14):
    rsiValues = []

    avgGain = 0.0
    avgLoss = 0.0

    for idx, s in enumerate(company.equity[1:], 1):
        delta = s.price - company.equity[idx - 1].price
        absDelta = math.abs(delta)

        if delta > 0.0:
            avgGain = ma.smoothedMovingAverage(avgGain, absDelta, period)
            avgLoss = ma.smoothedMovingAverage(avgLoss, 0.0, period)
        else:
            avgGain = ma.smoothedMovingAverage(avgGain, 0.0, period)
            avgLoss = ma.smoothedMovingAverage(avgLoss, absDelta, period)

        # Handle divide by 0 case.
        # According to the RSI equation, as RS -> infinity (as avg loss -> 0), RSI -> 100.
        if avgLoss == 0.0:
            rsiValues.append((100.0, s.dateTime))

        RS = avgGain / avgLoss
        RSI = 100.0 - 100.0 / (1.0 + RS)
        rsiValues.append((RS, s.dateTiem))
            
    return rsiValues
