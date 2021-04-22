
def time_span_generator():
    """[generate dates from 2008-01-01 to 2021-04-22]
    """
    years = [year for year in range(2008,2022)]
    months = [month for month in range(1,13)]
    start_day = 1
    end_date = "2021-04-22"
    dates = [str(year)+"-"+str(month)+"-"+str(start_day) for year in years for month in months]
    del dates[-8:]
    dates.append(end_date)
    for i in range(len(dates)-1):
        yield (dates[i], dates[i+1])


time_span_generator = time_span_generator()


if __name__ == "__main__":
    for i in time_span_generator:
        print(i)
    
