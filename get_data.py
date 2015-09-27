import requests, datetime, os, json, time, csv, sys, re

URL = "http://real-chart.finance.yahoo.com/table.csv"

NOW = datetime.datetime.now()

WORKDIR = os.path.abspath(os.path.dirname(__file__))

LOGFILE = os.path.join(WORKDIR, "logs", NOW.strftime("%Y-%m-%d %H:%M:%S")+'.json')

RAWDATAFILE = os.path.join(WORKDIR, "data/historical_data.csv")

CLEANDATAFILE = os.path.join(WORKDIR, "data/historical_data_clean.csv")

FOO = "http://real-chart.finance.yahoo.com/table.csv?s=YHOO&a=08&b=23&c=2014&d=08&e=23&f=2015&g=d&ignore=.csv"

def main():
    errors = 0
    tickers = get_tickers()

    if errors > 10:
        sys.exit("get_data.py exceeded error threshold")

    with open(RAWDATAFILE, 'a+') as f:
        for i, ticker in enumerate(tickers[:3]):
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

            try:
                r = requests.get(URL, params=params)
                f.write(r.text + '\n')
            except Error as e:
                errors += 1
                with open(LOGFILE, 'a+') as log:
                    log.write(ticker + '\n')
                time.sleep(65)
            time.sleep(10)

def get_tickers():

    with open(os.path.join(WORKDIR,"data/members.json")) as f:
        members = json.loads(f.read())

    return [stock['Symbol'] for stock in members]

def clean_data():

    regex = re.compile('Date,Open,High,Low,Close,Volume,Adj Close', re.I)

    with open(RAWDATAFILE, 'r') as raw:
        with open(CLEANDATAFILE, 'a+') as clean:
            for i, line in enumerate(raw.readlines(), start=0):
                if i == 0:
                    clean.write(line)
                elif re.match(regex, line) or len(line) < 5:
                    continue
                else:
                    clean.write(line)


if __name__ == '__main__':

    #main()
    clean_data()
