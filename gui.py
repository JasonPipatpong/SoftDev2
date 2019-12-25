
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg") 
from matplotlib.figure import Figure
from tkcalendar import Calendar, DateEntry
from Data import *
from tkinter import filedialog
from tkinter import font

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
      box_data.insert(END,my_data[i].Ip+'    '+my_data[i].Day+'/'
                        +my_data[i].Month+'/'+my_data[i].Year)
def donothing():
   x = 0
def open_file():
    file=filedialog.askopenfilename()
    return file
def countip():
    start=frist_index(en_date1.get())
    stop=last_index(en_date2.get())
    dup={}
    for u in range(start,stop+1):
        if not(my_data[u].Ip in dup):
            dup[my_data[u].Ip] =1
        else:
            dup[my_data[u].Ip] +=1
    return dup 
def plot_top10():
    box_grap.delete(0,END)
    count=countip()
    top=sorted(count.items(), key = lambda x : x[1],reverse=True)
    x=[x for x,y in top]
    y=[y for x,y in top]
    text=['A','B','C','D','E','F','G','H','I','L']
    figure1 = Figure(figsize=(6.5,6), dpi=70)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, window)
    bar1.get_tk_widget().place(x=1000,y=0)
    ax1.barh(text[::-1],y[9::-1])
    ax1.set_title('Top 10')
    for i in range(10):
        box_grap.insert(END,'{0}. {1}-----Hit-----> {2}'.format(text[i],x[i],y[i]))


# Buil window 
window = Tk()
window.title("Log Analysis")
window.geometry('1920x700')
s = ttk.Style(window)
s.theme_use('clam')
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
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
    cal = Calendar(top,date_pattern='d/m/yy',showweeknumbers=FALSE,showothermonthdays=FALSE,
                   font="Arial 14", selectmode='day',
                    year=2015, month=5, day=17)
    cal.pack(fill="both", expand=True)
    Button(top, text="ok", command=print_sel).pack()
def calendar_stop():
    def print_sel():
        en_date2.delete(0,END)
        en_date2.insert(0,cal.get_date())
        top.destroy()
    top = Toplevel(window)
    cal = Calendar(top,date_pattern='d/m/yy',showweeknumbers=FALSE,showothermonthdays=FALSE,
                   font="Arial 14", selectmode='day',
                    year=2015, month=5, day=20)
    cal.pack(fill="both", expand=True)
    Button(top, text="ok", command=print_sel).pack()
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
box_data=Listbox(window,width=50,height=20)
box_data.place(x=30,y=300)
frame.place(x = 490, y = 300 ,height=340)
scrollbar = Scrollbar(frame, orient="vertical",command=box_data.yview)
scrollbar.pack(side="right", fill="y")
box_data.config(yscrollcommand=scrollbar.set)
Button(window, text='Analysis', command=plot_top10).place(x=50, y=150)
small=font.Font(size=10)
box_grap=Listbox(window,width=30,height=12)
box_grap.place(x=1100,y=430)
window.mainloop()
