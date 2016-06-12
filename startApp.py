#!/usr/bin/env python

'''
README(PypeR): http://www.webarray.org/softwares/PypeR/
README(PypeR): http://www.jstatsoft.org/v35/c02/paper
'''

import json, time, threading, logging.config
import pandas as pd
import pyper as pr
from bottle import route, run, template, static_file, request, response


b_host = "0.0.0.0"
b_port = 4390

solar = {}
feature = {}
result = []
siIndex = 0
sema = False

cities = ["sapporo", "sendai", "tokyo", "nagoya", "toyama", "osaka", "hiroshima", "matsuyama", "fukuoka"]

# parameter
city = "tokyo"
field = 20
traintime = 30
timeseries = 1

set_url = ":4380/remote/set?"

# CREATE A R INSTANCE WITH PYPER
r = pr.R(use_pandas="True")


@route('/')
def index():
    #ipaddr = socket.gethostbyname(socket.gethostname())
    #global ems
    #ids = ems.keys()
    return template('index',
                    admintext="SI predictor",
                    title="SI predictor",
                    #ip= ipaddr,
                    #ids=sorted(ids)
                    )


@route('/restart')
def getInitFile():
    global sema
    while sema:
        time.sleep(1)
    sema = True

    global solar
    global feature
    global city
    global field

    # read file
    if field == 0:
        solar = pd.read_csv('../data/2012/'+city+'/1day_time_series_solar_'+city+'_2012_30.csv', header=None)
        feature = pd.read_csv('../data/2012/'+city+'/gpvmsm_2012_'+city+'.csv', header=None)
    else:
        solar = pd.read_csv('../data/area/area{field:02d}/solar_global_30_area{field:02d}_{city}.csv'.format(city=city, field=field), header=None, skiprows=4)
        feature = pd.read_csv('../data/area/area{field:02d}/gpvmsm_2012_area{field:02d}_{city}.csv'.format(city=city, field=field), header=None)
    # change columns name
    solar.columns = ['date', 'SI']
    feature.columns = ['date', 'pressure', 'wind_WE', 'wind_SN', 'temperature', 'humidity', 'precipitation', 'cloud_ALL', 'cloud_TOP', 'cloud_MIDDLE', 'cloud_DOWN']
    # change index name
    solar.index = solar.ix[:, 0]
    feature.index = feature.ix[:, 0]
    # debug
    logger.debug(solar)
    logger.debug(feature)

    sema = False
    return solar


@route('/get/log')
def getLog():
    response.content_type = 'application/json'
    logger.debug("log request received")
    while sema:
        time.sleep(1)
    return json.dumps(result)


@route('/get/last')
def getLastJsonFile():
    while sema:
        time.sleep(1)
    with open("lastSave.json") as json_last_file:
        global result
        result = json.load(json_last_file)
        logger.debug(result)
    return result


@route('/save')
def setJsonFile():
    with open("lastSave.json", 'w') as json_file:
        json.dump(result, json_file)
        logger.debug(result)
    return result


@route('/get/all')
def getAll():
    global siIndex
    siIndex = int(request.query.siIndex)
    logger.debug(siIndex)
    lasso()
    while sema:
        time.sleep(1)
    response.content_type = 'application/json'
    return json.dumps(result)


@route('/set/param')
def setParam():
    global city
    global traintime
    global timeseries
    city = request.query.city
    traintime = int(request.query.traintime)
    timeseries = int(request.query.timeseries)
    logger.debug(city)
    logger.debug(traintime)
    logger.debug(timeseries)
    getInitFile()
    return json.dumps(result)


def setInitFile():
    # initialize for result
    global result

    # PASS DATA FROM PYTHON TO R
    global solar
    global feature
    global r
    r.assign("data_si", solar)
    r.assign("data_feature", feature)
    r('data_feature <- as.matrix(data_feature)')

    # call the library
    r('library("glmnet")')

    # normalization
    r('scale(data_si)')
    r('scale(data_feature)')

    logger.debug("set init files to R...")
    return


def lasso():
    global sema
    while sema:
        time.sleep(1)
    sema = True

    global r
    global traintime
    global timeseries
    global siIndex

    r.assign("i", siIndex)
    r.assign("tt", traintime)
    r.assign("ts", timeseries)

    # set train/test time
    r('train_time <- c(1:(24*tt)+(24*i))')
    r('test_time <- c((24*tt+1):(24*(tt+1))+(24*i))')

    # generate train data
    r('train_cvlasso <- cbind(data_si[train_time,2], data_si[train_time+1,2], data_si[train_time+2,2], data_si[train_time+3,2], data_feature[train_time+3,])')
    r('for (si in 1:4) { colnames(train_cvlasso)[si] <- paste("SI", si, sep="") }')
    r('train_cvlasso <- subset(train_cvlasso, complete.cases(train_cvlasso))')
    r('train_cvlasso <- subset(train_cvlasso, train_cvlasso[,4]>0)')

    # generate test data
    r('test_cvlasso <- cbind(data_si[test_time,2], data_si[test_time+1,2], data_si[test_time+2,2], data_si[test_time+3,2], data_feature[test_time+3,])')
    r('for (si in 1:4) { colnames(test_cvlasso)[si] <- paste("SI", si, sep="") }')
    r('test_cvlasso <- subset(test_cvlasso, complete.cases(test_cvlasso))')
    r('test_cvlasso <- subset(test_cvlasso, test_cvlasso[,4]>0)')

    # model
    r('set.seed(0)')
    r('if (ts==0) {fit <- cv.glmnet(train_cvlasso[,-c(1,2,3,4)], train_cvlasso[,4])}')
    r('if (ts==1) {fit <- cv.glmnet(train_cvlasso[,-c(1,2,4)], train_cvlasso[,4])}')
    r('if (ts==2) {fit <- cv.glmnet(train_cvlasso[,-c(1,4)], train_cvlasso[,4])}')
    r('if (ts==3) {fit <- cv.glmnet(x=train_cvlasso[,-4], y=train_cvlasso[,4])}')
    # r("summary(cv.glmnet(x=train_cvlasso[,-c(1,4)], y=train_cvlasso[,4]))")

    # prediction
    r('if (ts==0) {SI.cvlasso.pre <- predict(fit, newx=test_cvlasso[,-c(1,2,3,4)])}')
    r('if (ts==1) {SI.cvlasso.pre <- predict(fit, newx=test_cvlasso[,-c(1,2,4)])}')
    r('if (ts==2) {SI.cvlasso.pre <- predict(fit, newx=test_cvlasso[,-c(1,4)])}')
    r('if (ts==3) {SI.cvlasso.pre <- predict(fit, newx=test_cvlasso[,-4])}')

    # set result
    timestamp = r.get("list(rownames(test_cvlasso))")[0]
    real = r.get("list(test_cvlasso[,4])")[0]
    lasso = r.get("list(SI.cvlasso.pre[,1])")[0]

    logger.debug(timestamp)
    logger.debug(real)
    logger.debug(lasso)

    global result
    tmp = []

    for i, v in enumerate(timestamp):
        tmp.append({"timestamp": v[0:4]+"-"+v[4:6]+"-"+v[6:8]+" "+v[8:10]+":30",
                    "real": real[i],
                    "lasso": lasso[i]})

    # update
    result = tmp
    sema = False
    return

#####
# resources
#####


@route('/js/<filename>')
def js_static(filename):
    return static_file(filename, root='./js')


@route('/img/<filename>')
def img_static(filename):
    return static_file(filename, root='./img')


@route('/css/<filename>')
def img_static_css(filename):
    return static_file(filename, root='./css')


#Static Files
@route('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root="./static")


if __name__ == "__main__":
    logging.config.fileConfig("config/logger.conf", disable_existing_loggers=0)
    logger = logging.getLogger(__name__)
    logger.debug('starting...')
    #t = threading.Thread(target=setInitFile, name="setInitFile")
    try:
        getInitFile()
        setInitFile()
        #t.daemon = True
        #t.start()
        #time.sleep(1)
        run(server="tornado", host=b_host, port=b_port, quiet=False, reloader=False)
    except KeyboardInterrupt:
        logger.info("Ctrl-c received! Sending kill to threads...")
        t.kill_received = True
        raise
