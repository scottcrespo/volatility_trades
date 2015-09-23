import requests, datetime, os, json, time, csv, sys

URL = "http://real-chart.finance.yahoo.com/table.csv"
NOW = datetime.datetime.now()
WORKDIR = os.path.abspath(os.path.dirname(__file__))
LOGFILE = os.path.join(WORKDIR, "logs", NOW.strftime("%Y-%m-%d %H:%M:%S")+'.json')
FOO = "http://real-chart.finance.yahoo.com/table.csv?s=YHOO&a=08&b=23&c=2014&d=08&e=23&f=2015&g=d&ignore=.csv"

def main():
    errors = 0
    tickers = get_tickers()

    if errors > 10:
        sys.exit("get_data.py exceeded error threshold")

    with open(os.path.join(WORKDIR, "data/historical_data.csv"), 'a+') as f:
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

if __name__ == '__main__':

    main()
