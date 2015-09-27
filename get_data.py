import requests, datetime, os, json, time, csv, sys, re

URL = "http://real-chart.finance.yahoo.com/table.csv"

NOW = datetime.datetime.now()

WORKDIR = os.path.abspath(os.path.dirname(__file__))

LOGFILE = os.path.join(WORKDIR, "logs", NOW.strftime("%Y-%m-%d %H:%M:%S")+'.txt')

RAWDATAFILE = os.path.join(WORKDIR, "data/historical_data.csv")

CLEANDATAFILE = os.path.join(WORKDIR, "data/historical_data_clean.csv")

TMPDATAFILE = os.path.join(WORKDIR, "data/tmpfile.csv")

FOO = "http://real-chart.finance.yahoo.com/table.csv?s=YHOO&a=08&b=23&c=2014&d=08&e=23&f=2015&g=d&ignore=.csv"

def main():

    # Track number of errors that result from request errors
    errors = 0
    # Get a list of tickers that we want to retrieve
    tickers = get_tickers()
    # iterate through a list of tickers and retrieve historical data
    for i, ticker in enumerate(tickers[:3], start=0):
        # abort if we encounter more than 10 errors
        if errors > 10:
            sys.exit("get_data.py exceeded error threshold")
        print "Retrieving data for ticker %s" % ticker
        # params are set to retrieve daily close data for S&P 500 stocks over
        # the past year
        params= {
            's':ticker,
            'a': '08',
            'b': '23',
            'c': NOW.year-1,
            'd': '08',
            'e': NOW.day,
            'f': NOW.year,
            'g': 'd',
            'ignore': '.csv',
        }

        # wrap the request in a try clause in case we receive an error
        try:
            with open(TMPDATAFILE, 'w+') as tmp:
                tmp.write(requests.get(URL, params=params).text)
        # if any error occurs in retrieving the data, log the ticker that we
        # didn't retrieve so we can grab it later. Also, in the event the Error
        # is the result of request throttling, the system sleeps for over 1 minute
        except Exception as e:
            print e
            errors += 1
            with open(LOGFILE, 'a+') as log:
                log.write(ticker + '\n')
            time.sleep(65)
            continue

        with open(TMPDATAFILE, 'r') as tmp:
            for j, line in enumerate(tmp.readlines(), start=0):
                if j == 0 and i == 0:
                    line = "%s,%s" % ("ticker", line)
                elif j == 0 and i != 0:
                    continue
                else:
                    line = "%s,%s" % (ticker, line)
                with open(RAWDATAFILE, 'a+') as f:
                    f.write(line)

        time.sleep(20)

def get_tickers():

    with open(os.path.join(WORKDIR,"data/members.json")) as f:
        members = json.loads(f.read())

    return [stock['Symbol'] for stock in members]

if __name__ == '__main__':

    main()
