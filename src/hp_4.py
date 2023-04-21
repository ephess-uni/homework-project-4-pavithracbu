# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    result = []
    for i in old_dates:
        reformatted_date = datetime.strptime(i, '%Y-%m-%d').strftime('%d %b %Y')
        result.append(reformatted_date)
    return result

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if isinstance(start, str) is False:
        raise TypeError("Start must be a string")
    if isinstance(n, int) is False:
        raise TypeError(" n must be in an integer")

    reformatted_date = datetime.strptime(start, '%Y-%m-%d')
    result = [reformatted_date]
    for i in range(n-1):
        reformatted_date += timedelta(days=1)
        result.append(reformatted_date)
    return result 


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    d_list = date_range(start_date, len(values))
    result = list(zip(d_list, values))
    return result


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    patron_id=[]
    date_due=[]
    date_returned=[]
    with open(infile) as f:
        reader=DictReader(f)
        for col in reader:
            patron_id.append(col["patron_id"])
            date_due.append(col["date_due"])
            date_returned.append(col["date_returned"])

    result_dict=defaultdict()
    for (a, b, c) in zip(patron_id,date_returned,date_due):
        numdays=(datetime.strptime(b, '%m/%d/%Y')-datetime.strptime(c, '%m/%d/%Y')).days
        if numdays<0:
            latefee=0.0
        else:
            latefee = round(numdays*0.25,2)
        if a in result_dict:
            result_dict[a] += latefee
        else:
            result_dict[a] = latefee

    result = [[key,val] for key, val in result_dict.items()]

    with open(outfile,'w') as f:
        outfile = DictWriter(f)
        outfile.writerow(["patron_id","late_fees"])
        outfile.writerows(result)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())

