import datetime

date_input = "2021/08/12"
year = 2021
month = 8
day = 12
time = "10:00"
str_time = date_input+" "+time

time_conv = datetime.datetime.strptime(str_time,'%Y/%m/%d %H:%M')

#date = datetime.datetime(year,month,day,time_conv)

print (time_conv)