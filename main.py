from functools import reduce
from subprocess import Popen, PIPE
import numpy as np
import os
import time
import binascii
import sys
# Trace Generator
SAMPLES = str(os.environ.get("TRACE_SAMPLES", 100))
SIZE = str(os.environ.get("TRACE_SIZE", 500))
INTER_ARRIVAL = str(os.environ.get("TRACE_INTER_ARRIVAL", 1))
READ_RATIO = str(os.environ.get("TRACE_READ_RATIO", 80))
SAS_SIZE = str(os.environ.get("TRACE_SAS_SIZE", 549093))
DISTRIBUTION = str(os.environ.get("TRACE_DISTRIBUTION", 1))
MEAN = str(os.environ.get("TRACE_MEAN", 0))
STD = str(os.environ.get("TRACE_STD", 1))
CONCURRENCY = str(os.environ.get("TRACE_CONCURRENCY", 1))
# Queue Simulator
QUEUE_SIMULATOR_AVG_SERVICE_TIME = str(
    os.environ.get("QUEUE_SIMULATOR_AVG_SERVICE_TIME", 1400))
QUEUE_SIMULATOR_NUM_DELAYS_REQUIRED = str(
    os.environ.get("QUEUE_SIMULATOR_NUM_DELAYS_REQUIRED", 242))
#


def getOutputFileName(x):
    return binascii.hexlify('{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}'.format(SAMPLES, SIZE, INTER_ARRIVAL, READ_RATIO, SAS_SIZE, DISTRIBUTION, MEAN, STD, CONCURRENCY, x, QUEUE_SIMULATOR_AVG_SERVICE_TIME, QUEUE_SIMULATOR_NUM_DELAYS_REQUIRED).encode("utf-8"))


OUTPUT_CSV = str(os.environ.get("OUTPUT_PATH", "./results/"))

# Utils


def getInterArrival(data):
    return list(map(lambda x: int(x[0]), data))


def getAvgInterArrival(data):
    return np.diff(np.array(data)).mean()


def removeWhiteSpaces(data):
    return list(filter(lambda x: not x == '', data))


def convertToCSVFormat(data):
    if(len(data) == 0):
        print("ERROR: {}".format(data))
        sys.exit(0)
    return reduce(lambda x, y: x+"\n"+y, data)


#
traceGenerator = Popen(["./bins/generator", SAMPLES, SIZE, INTER_ARRIVAL,
                        READ_RATIO, SAS_SIZE, DISTRIBUTION, MEAN, STD, CONCURRENCY], stdout=PIPE)
#x = Popen(["./generator","100","500","1","80","549093","1","0","1","1"],stdout=PIPE)


text = None
while traceGenerator.poll() is None:
    text = traceGenerator.stdout.read().decode('utf-8')
text = removeWhiteSpaces(text.split("\n"))
text2 = convertToCSVFormat(text)
data = list(map(lambda x: x.split(','), text))
data = getInterArrival(data)
avgia = str(getAvgInterArrival(data))
filename = OUTPUT_CSV+str(getOutputFileName(avgia), 'ascii')+'.csv'

with open(filename, "a") as traceFile:
    queueSimulator = Popen(["./bins/single", avgia, QUEUE_SIMULATOR_AVG_SERVICE_TIME,
                            QUEUE_SIMULATOR_NUM_DELAYS_REQUIRED], stdout=PIPE)
    text = ''
    while queueSimulator.poll() is None:
        text += queueSimulator.stdout.read().decode('utf-8')
    traceFile.write(text2+"\n"+text)
print("{} created".format(filename))
