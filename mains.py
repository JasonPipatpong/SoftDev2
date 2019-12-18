
import re
import json
class Info:
    def __init__(self,Ip,Hyphen,Request,Day,Month,Year,Hour,Min,Sec,Zone,get,Status,SizeResponse,Referer,UserAgent):
        self.Ip=Ip
        self.Hyphen=Hyphen
        self.Request=Request

        self.Day=Day
        self.Month=Month
        self.Year=Year
        self.Hour=Hour
        self.Min=Min
        self.Sec=Sec
        self.Zone=Zone

        self.get=str(get)
        self.Status=str(Status)
        self.SizeResponse=str(SizeResponse)
        self.Referer=str(Referer)
        self.UserAgent=str(UserAgent)
    def __str__(self):
        return self.Ip

class Storange_Logele:
    def __init__(self):
        self.storange=[]
    def Add_log(self,ip,hy,re,day,mon,year,hour,min,sec,zone,get,stat,size,ref,user):
        self.storange.append(Info(ip,hy,re,day,mon,year,hour,min,sec,zone,get,stat,size,ref,user))
    def save_file_json(self):
        data=json.dumps(self.storange,default=obj_to_dict,indent=4)
        with open('Log_data.json', 'w') as f:
            json.dump(data, f)
        # comming....
    #def read_json_file()

def ListToStr(l):
    str1=" "
    for i in l:
        str1+=i
    return str1
def obj_to_dict(obj): 
    my_dict={
        "__class__":obj.__class__.__name__,
        "__module__":obj.__module__
    }
    my_dict.update(obj.__dict__)
    return my_dict
def dict_to_obj(my_dict):
    if "__class__" in my_dict:
        class_name=my_dict.pop("__class__")
        module_name=my_dict.pop("__module__")
        module=__import__(module_name)
        class_=getattr(module,class_name)
        print(class_)
        obj= class_(**my_dict)
    else:
        obj=my_dict
    return obj
def countip():
    dup={}
    for u in range(len(st_log.storange)):
        if not(st_log.storange[u].Day+st_log.storange[i].Month+st_log.storange[i].Year in dup):
            dup[st_log.storange[u].Day+st_log.storange[i].Month+st_log.storange[i].Year] =1
        else:
            dup[st_log.storange[u].Day+st_log.storange[i].Month+st_log.storange[i].Year] +=1
    return dup 
        

#---------------- start working--------------------------------------------------------------
with open('Log-Analysis_apache_logs.txt','r') as f:
    file =f.readlines()
st_log=Storange_Logele()
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
  # Example of call data  
for i in range(10):
    print(st_log.storange[i].Day+st_log.storange[i].Month+st_log.storange[i].Year) 
# st_log.save_file_json()  # this is save log to json file 





# Update 6 Dec 2019 /  เขียน fn split  type str and list. Goal can restored to class 
# Update 18 Dec 2019 / done: -save json file  ,||, comming: -read json file. -pick file.
  
    



