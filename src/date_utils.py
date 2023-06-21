import datetime as dt

def one_week_ago():
    today = dt.date.today()
    return today - dt.timedelta(days=7)
    
def one_work_week_ago():
    today = dt.date.today()
    return today - dt.timedelta(days=5)

def one_month_ago():
    today = dt.date.today()
    return today - dt.timedelta(days=30)

def one_year_ago():
    today = dt.date.today()
    return today - dt.timedelta(days=365)

def five_years_ago():
    today = dt.date.today()
    return today - dt.timedelta(days=365 * 5)

def default_start_end(start_date, end_date, interval):
    start_date_functions = {"1m": one_work_week_ago, "1h": one_month_ago, "1d": five_years_ago, "1wk": five_years_ago}
    #Handling default start and end dates with looking up interval in start_date_functions dict instead of keyword args
    if start_date == None:
        start_date = start_date_functions[interval]()
    if end_date == None:    
        end_date = dt.date.today()

    return start_date, end_date

def make_date(str):
    return dt.datetime.strptime(str, "%Y-%m-%d").date()