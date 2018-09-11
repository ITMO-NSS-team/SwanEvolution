import math
import random
import subprocess
from datetime import datetime

import Consts


class ModelDate:
    Year = 2014
    Month = 8
    Days = 14
    Hours = 12
    numOfIndividuals = 0
    numOfPopulation = 1


from src.evo_balt.files import ObservationFile


def getDate(y, m, d, h, delimiter):
    s = '{0:02d}{1:02d}{2:02d}{3:02d}'.format(y, m, d, h)  # str(y) + str(m) + str(d) + str(h) #'2013102000'
    if delimiter == 0:
        mytime = datetime.strptime(s, "%Y%m%d%H")
        return mytime.strftime("%Y%m%d%H")
    else:
        mytime = datetime.strptime(s, "%Y%m%d%H")  # 2013-10-20T12:00:00
        return mytime.strftime("%Y-%m-%dT%H") + ":00:00"


def getForecast(station, colNum):
    if Consts.Debug.debugMode:
        return [(random.random() * 5)] * 1000

    pathEst = Consts.Models.SWAN.pathToResults + station
    file = open(pathEst, 'r')
    content = [x for x in file.readlines() if x[0] != "%"]

    return [float(line.split()[colNum]) for line in content]


def getObservation(station, colNum):  # returnable value's length is equal to meteoForecastTime + 1 !!!

    pathObs = Consts.Models.Observations.pathToFolder + station

    obs_file = ObservationFile(path=pathObs)
    content = obs_file.time_series(
        from_date=Consts.Models.Observations.timePeriodsStartTimes[Consts.State.currentPeriodId],
        to_date=Consts.Models.Observations.timePeriodEndTimes[Consts.State.currentPeriodId])

    return [float(line.split()[colNum]) for line in content]


def parseDate(modelDate):  # 2013-10-20T12-00-00
    if ('-' in modelDate):
        date = modelDate.split('-')[:2]
        date.extend([modelDate.split('-')[2].split('T')[0], modelDate.split('-')[2].split('T')[1]])
        return map(lambda d: int(d), date)
    if ('.' in modelDate):
        date = modelDate
        return [int(date[0:4]), int(date[4:6]), int(date[6:8]), int(date[9:11])]


def runBatFile():
    p = subprocess.Popen('D:\\EvoBalt_v3.0-single\\runBatFile.exe')
    p.wait()


def getMultidimDistance(dims1, dims2):
    result = 0
    for i in range(0, len(dims1)):
        diffItem = (float(dims1[i]) - float(dims2[i])) ** 2
        result += diffItem
    return math.sqrt(result)


def errorFunction(item):
    return getMultidimDistance(item.errors, [0] * len(item.errors))


def fullErrorFunction(item):
    return getMultidimDistance(item.fullErrors, [0] * len(item.fullErrors))
