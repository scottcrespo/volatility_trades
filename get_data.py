import requests, datetime, os, json, time, csv, sys, re

URL = "http://real-chart.finance.yahoo.com/table.csv"

NOW = datetime.datetime.now()

WORKDIR = os.path.abspath(os.path.dirname(__file__))

LOGFILE = os.path.join(WORKDIR, "logs", NOW.strftime("%Y-%m-%d %H:%M:%S")+'.txt')

RAWDATAFILE = os.path.join(WORKDIR, "data/historical_data.csv")

TMPDATAFILE = os.path.join(WORKDIR, "data/tmpfile.csv")

FOO = "http://real-chart.finance.yahoo.com/table.csv?s=YHOO&a=08&b=23&c=2014&d=08&e=23&f=2015&g=d&ignore=.csv"

def main():
    """
    Retrieves daily closing prices, year-to-date for all members of the S&P 500, and write
    the data to file
    """
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

        # wrap the request in a try clause in case we receive an error. Write the Data
        # to a temporary file, because we will need to do some additional parsing before
        # appending to our primary data file.
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

        # if the data was successfully retrieved and written to the temoprary file, then
        # we load the data and add a ticker field to each line before writing to the main
        # data file
        with open(TMPDATAFILE, 'r') as tmp:
            for j, line in enumerate(tmp.readlines(), start=0):
                # if this is the first ticker we've scraped, then we need to add the new
                # 'ticker' field to the very top of the file
                if j == 0 and i == 0:
                    line = "%s,%s" % ("ticker", line)
                # We don't need the field names of every subsequent ticker we scrape, so
                # we continue
                elif j == 0 and i != 0:
                    continue
                # add the ticker symbol to the beginning of each data entry
                else:
                    line = "%s,%s" % (ticker, line)
                # append the entry to the main data file
                with open(RAWDATAFILE, 'a+') as f:
                    f.write(line)
        # sleep for a while before pulling another data set
        time.sleep(20)

def get_tickers():
    """
    Reads json data representing members of the S&P, and returns list of ticker symbols
    """
    
    with open(os.path.join(WORKDIR,"data/members.json")) as f:
        members = json.loads(f.read())

    return [stock['Symbol'] for stock in members]

if __name__ == '__main__':

    main()
