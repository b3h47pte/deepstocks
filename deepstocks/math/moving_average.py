#
# Utiltiies for computing the moving average.
#

# newVal = [(N- 1) * previousAvg + newVal] / N
def smoothedMovingAverage(previousAvg, newVal, N):
    newVal = ((N-1) * previousAvg + newVal) / float(N)
    return newVal
