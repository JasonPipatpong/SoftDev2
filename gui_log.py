
from tkinter import *
#import tkinter as tk
#from tkinter.ttk import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg") 
from matplotlib.figure import Figure
from tkcalendar import Calendar
from Data import *
from tkinter import filedialog
from tkinter import font
import datetime
import numpy as np
import pycountry
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cmd
import os

my_data=load_mydata()

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
def view_all():
    box_data.delete(0,END)
    start=frist_index(en_date1.get())
    stop=last_index(en_date2.get())
    for i in range(start,stop+1):
      box_data.insert(END,'{0}  {1}/{2}/{3}  {4}'.format(my_data[i].Ip,
                        my_data[i].Day,my_data[i].Month,my_data[i].Year,my_data[i].Country))
                        
def donothing():
   x = 0
def open_file():
    file=filedialog.askopenfilename()
    return file
def count_ip():
    start=frist_index(en_date1.get())
    stop=last_index(en_date2.get())
    dup={}
    for u in range(start,stop+1):
        if not(my_data[u].Ip in dup):
            dup[my_data[u].Ip] =1
        else:
            dup[my_data[u].Ip] +=1
    return dup 
def count_country_code():
    start=frist_index(en_date1.get())
    stop=last_index(en_date2.get())
    dup={}
    for u in range(start,stop+1):
        if not(my_data[u].Country_code in dup):
            dup[my_data[u].Country_code] =1
        else:
            dup[my_data[u].Country_code] +=1
    return dup 
def get_iso2(iso_3):
    iso=pycountry.countries.get(alpha_3=str(iso_3))
    if iso != None:
        return iso.alpha_2
def plot_top10():
    box_grap.delete(0,END)
    count=count_ip()
    top=sorted(count.items(), key = lambda x : x[1],reverse=True)
    x=[x for x,y in top]
    y=[y for x,y in top]
    text=['A','B','C','D','E','F','G','H','I','L']
    figure1 = Figure(figsize=(5,4), dpi=80)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, window)
    bar1.get_tk_widget().place(x=350,y=0)
    ax1.barh(text[::-1],y[9::-1])
    ax1.set_title('Top 10')
    for i in range(10):
        box_grap.insert(END,'{0}. {1}-----Hit-----> {2}'.format(text[i],x[i],y[i]))
    plot_map()
def plot_map():
    box_country.delete(0,END)
    count=count_country_code()
    c1_max=max(count.values())
    c1_min=min(count.values())
    cm = plt.get_cmap('Greens')
    scheme = [cm(i / 2560) for i in range(2560)]
    bins=np.linspace(c1_min,c1_max,2560)

    figure2 = Figure(figsize=(5,3), dpi=120)
    ax2 = figure2.add_subplot(111)
    bar2 = FigureCanvasTkAgg(figure2, window)
    bar2.get_tk_widget().place(x=730,y=0)
    ax2.set_title('Country')
    m = Basemap(projection='mill',llcrnrlat=-60,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c',ax=ax2)
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents()
    m.drawmapboundary(fill_color='lightskyblue')
    path=os.getcwd()
    shapfile='{0}/ne_50m_admin_0_countries/ne_50m_admin_0_countries'.format(path)
    m.readshapefile(shapfile,'unit', drawbounds = False)
    for info, shape in zip(m.unit_info, m.unit):
        iso=info['ADM0_A3']
        iso_2=get_iso2(iso)
        if not iso_2  in count:
            color='#dddddd'
        else:
            d=np.digitize(count[str(iso_2)],bins)
            color=scheme[d-1]
        patches = [Polygon(np.array(shape), True)]
        pc = PatchCollection(patches,edgecolor='k', linewidths=1., zorder=2)
        pc.set_facecolor(color)
        ax2.add_collection(pc)
    cmap = mpl.colors.ListedColormap(scheme)
    sm=cmd.ScalarMappable(cmap=cmap)
    cl=m.colorbar(sm,location='bottom',size='3%',boundaries=bins,fig=figure2)
    cl.ax.tick_params(labelsize=6) 
    top=sorted(count.items(), key = lambda x : x[1],reverse=True)
    x=[x for x,y in top]
    y=[y for x,y in top]
    c=0
    for i in range(len(top)):
        c +=1 
        iso=pycountry.countries.get(alpha_2=str(x[i]))
        if iso != None:
            iso_country=iso.name
            box_country.insert(END,'{2}. {0} = {1} (Hit)'.format(iso_country,y[i],c))
    


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



# Buil window 
window = Tk()
window.title("Log Analysis")
window.geometry('1280x660')
s = ttk.Style(window)
s.theme_use('clam')
#btn_add = Button(window, text="Date" )
#btn_add.place(x=10,y=10)
#entry.grid(row=1,column=0,pady=2)
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=open_file)
#filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
def _quit():
    window.quit()
    window.destroy()
filemenu.add_command(label="Exit", command=_quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)
window.config(menu=menubar)




def calendar_start():
    def print_sel():
        en_date1.delete(0,END)
        en_date1.insert(0,cal.get_date())
        top.destroy()

    top = Toplevel(window)

    cal = Calendar(top,date_pattern='d/m/yyyy',showweeknumbers=FALSE,showothermonthdays=FALSE,disabledforeground =TRUE,
                   font="Arial 14", selectmode='day',selectbackground='royal blue',selectforeground='white',
                    year=2015, month=5, day=17)
    for i in my_date:
        date=datetime.datetime.strptime(i,"%d/%m/%Y").date()
        cal.calevent_create(date, 'None', 'get')
    cal.tag_config('get', background='light green',foreground='black' )
    cal.pack(fill="both", expand=True)
    Button(top, text="ok", command=print_sel).pack()


def calendar_stop():
    def print_sel():
        en_date2.delete(0,END)
        en_date2.insert(0,cal.get_date())
        top.destroy()

    top = Toplevel(window)

    cal = Calendar(top,date_pattern='d/m/yyyy',showweeknumbers=FALSE,showothermonthdays=FALSE,disabledforeground =TRUE,
                   font="Arial 14", selectmode='day',selectbackground='royal blue',selectforeground='white',
                    year=2015, month=5, day=20)
    for i in my_date:
        date=datetime.datetime.strptime(i,"%d/%m/%Y").date()
        cal.calevent_create(date, 'None', 'get')
    cal.tag_config('get', background='light green',foreground='black' )
    cal.pack(fill="both", expand=True)
    Button(top, text="ok", command=print_sel).pack()

my_date=all_date()
label2=Label(window,text='DATE')
label2.place(x=0,y=0)

label1=Label(window,text='Start date')
label1.place(x=0,y=20)
en_date1=Entry(window,width=10)
en_date1.place(x=0,y=40)
Button(window, text='Calendar', command=calendar_start).place(x=100, y=40)

label3=Label(window,text='Stop date')
label3.place(x=0,y=80)
en_date2=Entry(window,width=10)
en_date2.place(x=0,y=100)
Button(window, text='Calendar', command=calendar_stop).place(x=100, y=100)

btn_all=Button(window,text='View all',command=view_all)
btn_all.place(x=0,y=270)
en_search=Entry(window,width=15)
en_search.place(x=80,y=270)
btn_search=Button(window,text='Search')
btn_search.place(x=230,y=270)

frame = Frame(window)
box_data=Listbox(window,width=30,height=20)
box_data.place(x=30,y=300)
frame.place(x = 310, y = 300 ,height=340)
scrollbar = Scrollbar(frame, orient="vertical",command=box_data.yview)
scrollbar.pack(side="right", fill="y")
box_data.config(yscrollcommand=scrollbar.set)


Button(window, text='Analysis', command=plot_top10).place(x=50, y=150)
small=font.Font(size=10)
box_grap=Listbox(window,width=30,height=12)
box_grap.place(x=410,y=380)

box_country=Listbox(window,width=25,height=12)
box_country.place(x=870,y=380)

window.mainloop()