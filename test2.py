import tkinter as tk 
from tkinter import ttk
from tkcalendar import Calendar

from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.cm as cmd

import os
from Data import *
import datetime
import numpy as np
import apache_log_parser


my_data=load_mydata()
#-----------------------------------Def---------------------------------------------
def last_index(stop):
    day=stop.split('/')
    for i in range(len(my_data)):
        if int(my_data[i].Day)>int(day[0]):
            return i-1
    return len(my_data)-1
def frist_index(start):
    day=start.split('/')
    for i in range(len(my_data)):
        if int(my_data[i].Day)==int(day[0]):
            return i
def MonthToNum(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = string.strip()[:3].lower()
    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')
def all_date():
    mydate=[]
    for i in range(len(my_data)):
        month_num=MonthToNum(my_data[i].Month)
        date_comp="{0}/{1}/{2}".format(my_data[i].Day.strip(),month_num,my_data[i].Year.strip())
        if date_comp not in mydate:
            mydate.append(date_comp)
    return mydate
def dononthing():
    x=0


#-------------------------------Tk-----------------------------------------------------------------------------------------------------------
class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Log app")
        self.geometry('1280x660')
        container=tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (data_page,visual_page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(data_page)
        self.cla={}
        
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
    def access_class(self,clas):
        to_use = self.frames[clas]
        return to_use
 #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
class data_page(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        button = tk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(visual_page))
        button.place(x=0,y=200)
        self.treeview()
        self.calender()
        self.name = 'why'
        self.view_data()
    def treeview(self):
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        self.treeview=ttk.Treeview(self,style="mystyle.Treeview",height=15)
        self.treeview.place(x=430,y=300) 
        self.treeview["columns"]=()
        self.treeview.column("#0", width=650, minwidth=270, stretch=tk.NO)
        self.treeview.heading("#0",text="Date",anchor=tk.W)
    def view_data(self):
        btn_all=tk.Button(self,text='View all',command=self.insert_date_data)
        btn_all.place(x=400,y=270)
        en_search=tk.Entry(self,width=15)
        en_search.place(x=480,y=270)
        btn_search=tk.Button(self,text='Search')
        btn_search.place(x=630,y=270)
        # self.box_data=tk.Listbox(self,width=70,height=30)
        # self.box_data.place(x=430,y=100)
        frame = tk.Frame(self)
        frame.place(x = 1100, y = 300 ,height=300)
        scrollbar = tk.Scrollbar(frame, orient="vertical",command=dononthing)#command=self.box_data.yview
        scrollbar.pack(side="right", fill="y")
        # self.box_data.config(yscrollcommand=scrollbar.set)
    def view_all(self):
        self.box_data.delete(0,'end')
        start=frist_index(self.en_date1.get())
        stop=last_index(self.en_date2.get())
        for i in range(start,stop+1):
            self.box_data.insert('end','{0}  {1}/{2}/{3}  {4}  : {5}'.format(my_data[i].Ip,
                            my_data[i].Day,my_data[i].Month,my_data[i].Year,
                            my_data[i].Country,my_data[i].get,my_data[i].UserAgent))
    def calendar_start(self):
        def print_sel():
            self.en_date1.delete(0,'end')
            self.en_date1.insert(0,cal.get_date())
            top.destroy()
        top = tk.Toplevel(self)

        cal = Calendar(top,date_pattern='d/m/yyyy',showweeknumbers=False,showothermonthdays=False,disabledforeground =True,
                    font="Arial 14", selectmode='day',selectbackground='royal blue',selectforeground='white',
                        year=2015, month=5, day=17)
        for i in my_time:
            date=datetime.datetime.strptime(i,"%d/%m/%Y").date()
            cal.calevent_create(date, 'None', 'get')
        cal.tag_config('get', background='light green',foreground='black' )
        cal.pack(fill="both", expand=True)
        tk.Button(top, text="ok", command=print_sel).pack()
    def calendar_stop(self):
        def print_sel():
            self.en_date2.delete(0,'end')
            self.en_date2.insert(0,cal.get_date())
            top.destroy()

        top = tk.Toplevel(self)

        cal = Calendar(top,date_pattern='d/m/yyyy',showweeknumbers=False,showothermonthdays=False,disabledforeground =True,
                    font="Arial 14", selectmode='day',selectbackground='royal blue',selectforeground='white',
                        year=2015, month=5, day=20)
        for i in my_time:
            date=datetime.datetime.strptime(i,"%d/%m/%Y").date()
            cal.calevent_create(date, 'None', 'get')
        cal.tag_config('get', background='light green',foreground='black' )
        cal.pack(fill="both", expand=True)
        tk.Button(top, text="ok", command=print_sel).pack()
    def calender(self):
        self.label2=tk.Label(self,text='DATE')
        self.label2.place(x=0,y=0)
        self.label2=tk.Label(self,text='DATE')
        self.label2.place(x=0,y=0)

        self.label1=tk.Label(self,text='Start date')
        self.label1.place(x=0,y=20)
        self.en_date1=tk.Entry(self,width=10)
        self.en_date1.place(x=0,y=40)
        tk.Button(self, text='Calendar',command=self.calendar_start).place(x=100, y=40)

        self.label3=tk.Label(self,text='Stop date')
        self.label3.place(x=0,y=80)
        self.en_date2=tk.Entry(self,width=10)
        self.en_date2.place(x=0,y=100)
        tk.Button(self, text='Calendar',command=self.calendar_stop).place(x=100, y=100)
    def count_ip(self):
        start=frist_index(self.en_date1.get())
        stop=last_index(self.en_date2.get())
        dup={}
        for u in range(start,stop+1):
            if not(my_data[u].Ip in dup):
                dup[my_data[u].Ip] =1
            else:
                dup[my_data[u].Ip] +=1
        return dup 
    def insert_date_data(self):
        self.plot_date()
        for i in range(len(my_data)):
            l=[my_data[i].Ip,my_data[i].Country,my_data[i].get,my_data[i].Referer,my_data[i].UserAgent]
            item='item{0}'.format(i)
            date='{0}/{1}/{2} :{3}:{4}:{5}'.format(my_data[i].Day,my_data[i].Month,my_data[i].Year,
                                                    my_data[i].Hour,my_data[i].Min,my_data[i].Sec)
            self.treeview.insert('','end',item,text=date) 
            for m in range(5):
                uniq='{0}.{1}'.format(i,m)
                info=': {0}'.format(l[m])
                self.treeview.insert(item,'end',uniq,text=info)  
    
    def count_day_data(self):
        start=frist_index(self.en_date1.get())
        stop=last_index(self.en_date2.get())
        dup={}
        for u in range(start,stop+1):
            if not(my_data[u].Day in dup):
                dup[my_data[u].Day] =1
            else:
                dup[my_data[u].Day] +=1
        return dup
    def plot_date(self):
        count=self.count_day_data()
        x_pos=[i for i in count]
        x_p = np.arange(len(count))
        y=[count[i] for i in count]
        figure0 = Figure(figsize=(7,3), dpi=80)
        ax0 = figure0.add_subplot(111)
        bar0 = FigureCanvasTkAgg(figure0, self)
        bar0.get_tk_widget().place(x=350,y=0)
        ax0.bar(x_pos, y,align='center')
        ax0.set_ylabel('Fre')
        ax0.set_title('All Date')
        # ax0.set_xticks(x_p)
        # ax0.set_xticklabels(x[:10],rotation=45)
    def count_phone(self):
        start=frist_index(self.en_date1.get())
        stop=last_index(self.en_date2.get())
        line_parser = apache_log_parser.make_parser("\"%{User-Agent}i\"")
        dup={}
        for u in range(start,stop+1):
            os=line_parser('"{0}"'.format(my_data[u].UserAgent))
            if not(os['request_header_user_agent__is_mobile']in dup):
                dup[os['request_header_user_agent__is_mobile']] =1
            else:
                dup[os['request_header_user_agent__is_mobile']] +=1
        return dup 
    def count_os(self):
        start=frist_index(self.en_date1.get())
        stop=last_index(self.en_date2.get())
        line_parser = apache_log_parser.make_parser("\"%{User-Agent}i\"")
        dup={}
        for u in range(start,stop+1):
            os=line_parser('"{0}"'.format(my_data[u].UserAgent))
            if not(os['request_header_user_agent__os__family']in dup):
                dup[os['request_header_user_agent__os__family']] =1
            else:
                dup[os['request_header_user_agent__os__family']] +=1
        return dup 
    def count_get(self):
        start=frist_index(self.en_date1.get())
        stop=last_index(self.en_date2.get())
        line_parser = apache_log_parser.make_parser('%h \"%r\"')
        dup={}
        for u in range(start,stop+1):
            os=line_parser('{0} "{1}"'.format(my_data[u].Ip,my_data[u].get))
            if not(os['request_url']in dup):
                dup[os['request_url']] =1
            else:
                dup[os['request_url']] +=1
        return dup
 #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>               
class visual_page(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Visuial!!!", font=LARGE_FONT)
        label.place(x=1,y=1)
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(data_page))
        button1.place(x=0,y=50)
        self.use_data = controller.access_class(data_page)
        self.box_grap=tk.Listbox(self,width=30,height=12)
        self.box_grap.place(x=40,y=400)
        # self.fig2 = plt.figure(figsize=(5, 3),dpi=120)
        # self.ax2 = self.fig2.add_subplot(111)
        # self.bar2 = FigureCanvasTkAgg(self.fig2, self)
        # self.bar2.get_tk_widget().place(x=700,y=0)
        # self.ax2.set_title('Country')
        # self.m=Basemap(llcrnrlon=-180, llcrnrlat=-65,urcrnrlon=180,urcrnrlat=80,ax=self.ax2)
        # self.m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
        # self.m.fillcontinents(color='grey', alpha=0.3)
        # self.m.drawcoastlines(linewidth=0.1, color="white")
        
        tk.Button(self, text='Analysis', command=self.plot_top10).place(x=0, y=100)

    def plot_top10(self):
        self.box_grap.delete(0,None)
        count=self.use_data.count_ip()
        top=sorted(count.items(), key = lambda x : x[1],reverse=True)
        x=[x for x,y in top]
        y=[y for x,y in top]
        text=['A','B','C','D','E','F','G','H','I','L']
        # figure1 = Figure(figsize=(5,4), dpi=80)
        # ax1 = figure1.add_subplot(111)
        # bar1 = FigureCanvasTkAgg(figure1, self)
        # bar1.get_tk_widget().place(x=600,y=350)
        # ax1.barh(text[::-1],y[9::-1])
        # ax1.set_title('Top 10')
        for i in range(10):
            self.box_grap.insert('end','{0}. {1}-----Hit-----> {2}'.format(text[i],x[i],y[i]))
        self.plot_map()
        self.plot_top_os()
        self.plot_phone()
        self.plot_get()
    def plot_map(self):
        c_country=self.use_data.count_ip()
        c1_max=max(c_country.values())
        c1_min=min(c_country.values())
        scheme=('green','orange','red')
        top=sorted(c_country.items(), key = lambda x : x[1],reverse=True)
        y=[y for x,y in top]
        x=[x for x,y in top]
        area=np.array(y)
        bins=np.linspace(y[-1],y[0],3)
        fig2 = plt.figure(figsize=(5, 3),dpi=120)
        ax2 = fig2.add_subplot(111)
        bar2 = FigureCanvasTkAgg(fig2, self)
        bar2.get_tk_widget().place(x=350,y=0)
        ax2.set_title('Top 10 ', fontsize=8)
        m=Basemap(llcrnrlon=-180, llcrnrlat=-65,urcrnrlon=180,urcrnrlat=80,ax=ax2)
        m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
        m.fillcontinents(color='grey', alpha=0.3)
        m.drawcoastlines(linewidth=0.1, color="white")
        c=0
        for i in x[:10]:
            Ip=self.index_ip(i)
            x, y = m(my_data[Ip].Longitude, my_data[Ip].Latitude)#m(long,lat)
            size=(np.digitize(area[c],bins))**4
            d=np.digitize(area[c],bins)
            colors=scheme[d-1]
            m.scatter(x, y,c=colors,zorder=10,alpha=0.6,s=size,cmap="Set1")
            c+=1
    def index_ip(self,ip):
        for i in range(len(my_data)):
            if ip == my_data[i].Ip:
                return i 
    def plot_top_os(self):
        count=self.use_data.count_os()
        top=sorted(count.items(), key = lambda x : x[1],reverse=True)
        x=[x for x,y in top]
        y=[y for x,y in top]
        explode = (0, 0, 0, 0,0.1)
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','lightgray']
        figure3 = Figure(figsize=(5,4), dpi=80)
        ax3 = figure3.add_subplot(111)
        bar3 = FigureCanvasTkAgg(figure3, self)
        bar3.get_tk_widget().place(x=900,y=0)
        ax3.pie(y[:5], explode=explode, labels=x[:5],autopct='%1.1f%%',colors=colors,
                    shadow=True, startangle=90)
        ax3.set_title('Top 5 OS')
    def plot_phone(self):
        count=self.use_data.count_phone()
        top=sorted(count.items(), key = lambda x : x[1],reverse=True)
        x=[x for x,y in top]
        y=[y for x,y in top]
        x_pos=np.arange(len(x))
        figure4 = Figure(figsize=(5,4), dpi=80)
        ax4 = figure4.add_subplot(111)
        bar4 = FigureCanvasTkAgg(figure4, self)
        bar4.get_tk_widget().place(x=900,y=300)
        ax4.pie(y,labels=x,autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax4.set_title('Phone', fontsize=10)
    def plot_get(self):
        count=self.use_data.count_get()
        top=sorted(count.items(), key = lambda x : x[1],reverse=True)
        x=[x for x,y in top]
        y=[y for x,y in top]
        x_pos=np.arange(len(x))
        explode = (0, 0, 0, 0,0.1)
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','lightgray']
        figure5 = Figure(figsize=(5,4), dpi=100)
        ax5 = figure5.add_subplot(222)
        bar5 = FigureCanvasTkAgg(figure5, self)
        bar5.get_tk_widget().place(x=320,y=300)
        for label in (ax5.get_xticklabels()):
            label.set_fontsize(7)
        ax5.bar(x_pos[:10],y[:10],align='center', alpha=1)
        ax5.set_xticks(x_pos[:10])
        ax5.set_xticklabels(x[:10],rotation=85)
        ax5.set_title('top get', fontsize=10)
    


                

  
 
LARGE_FONT= ("Verdana", 12)
window = Window()
s = ttk.Style(window)
s.theme_use('clam')
my_time=all_date()
window.mainloop()