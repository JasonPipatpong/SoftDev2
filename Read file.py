import re
def ListToStr(l):
    str1=" "
    for i in l:
        str1+=i
    return str1


with open('Log-Analysis_apache_logs.txt','r') as f:
    file =f.readlines()

class Info:
    def __init__(self,ip,hy,re,day,mon,year,hour,min,sec,zone,get,stat,size,ref,user):
        self.Ip=ip
        self.Hyphen=hy
        self.Request=re

        self.Day=day
        self.Month=mon
        self.Year=year
        self.Hour=hour
        self.Min=min
        self.Sec=sec
        self.Zone=zone

        self.get=str(get)
        self.Status=str(stat)
        self.SizeResponse=str(size)
        self.Referer=str(ref)
        self.UserAgent=str(user)

        self.Country=None
        self.Latitude=None
        self.Longitude=None



class Storange_Logele:
    def __init__(self):
        self.storange=[]
    def Add_log(self,ip,hy,re,day,mon,year,hour,min,sec,zone,get,stat,size,ref,user):
        self.storange.append(Info(ip,hy,re,day,mon,year,hour,min,sec,zone,get,stat,size,ref,user))

st_log=Storange_Logele()
count=0
for ele in file:
    f=ele.split(" ")
    ip=f[0]
    hyp=f[1]
    req=f[2]
    day=re.findall(r"\[(.\d)/",ele)
    month=re.search(r"([a-zA-Z]+)",ele) # this using re.search
    year=re.findall(r"\/(\d+)\:",ele)
    time=re.findall(r"\:(\d+)",ele)
    zone=re.findall(r"(\055\d+|\053\d+)]",ele)

    info=re.findall(r"\"(.*?)\"",ele) # spilt data 

    #----------------------------------------------------
    ip=f[0]
    hyp=f[1]
    req=f[2]
    day1=ListToStr(day)
    month1=ListToStr(month.group()) # re search. Dont forget to group for using it.
    year1=ListToStr(year)

    hour1=ListToStr(time[0])
    min1=ListToStr(time[1])
    sec1=ListToStr(time[2])

    zone1=ListToStr(zone)

    get=ListToStr(info[0])
    status=f[8]
    size_response=f[9]
    referer=ListToStr(info[1])
    try:
        user_agent=ListToStr(info[2])
    except IndexError:
        user_agent='-'
    #--------------------------------------------------------
    st_log.Add_log(ip,hyp,req,day1,month1,year1,hour1,min1,sec1,zone1,get,status,size_response,referer,user_agent)
for i in range(10):
    print(st_log.storange[i].Day+st_log.storange[i].Month+st_log.storange[i].Year)
def countip():
    dup={}
    for u in range(len(st_log.storange)):
        if not(st_log.storange[u].Day+st_log.storange[i].Month+st_log.storange[i].Year in dup):
            dup[st_log.storange[u].Day+st_log.storange[i].Month+st_log.storange[i].Year] =1
        else:
            dup[st_log.storange[u].Day+st_log.storange[i].Month+st_log.storange[i].Year] +=1
    return dup 





# Update 6 Dec 2019 /  เขียน fn split  type str and list. Goal can restored to class 
  
    



