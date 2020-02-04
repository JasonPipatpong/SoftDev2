import re
import json
import request
class Info:
    def __init__(self,Ip,Hyphen,Request,Day,Month,Year,Hour,Min,Sec,Zone,get,Status,SizeResponse,Referer,UserAgent,
                    Country,Latitude,Longitude,Country_code):
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

        self.Country=Country
        self.Latitude=Latitude
        self.Longitude=Longitude
        self.Country_code=Country_code

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
    def Add_log(self,ip,hy,re,day,mon,year,hour,min,sec,zone,get,stat,size,ref,user,Country,Latitude,Longitude,Country_code):
        self.storange.append(Info(ip,hy,re,day,mon,year,hour,min,sec,zone,get,stat,size,ref,user,Country,Latitude,Longitude,Country_code))
    def save_file_json(self):
        data=json.dumps(self.storange,default=obj_to_dict,indent=4)
        with open('Log_data.json', 'w') as f:
            json.dump(data, f)
        
def load_mydata():
    with open('Log_data.json') as f:
        data=json.load(f)
    my_data=json.loads(data,object_hook=dict_to_obj)
    return my_data

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
        
