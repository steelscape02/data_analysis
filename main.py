import tkinter as tk
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.axes as ax
import requests
from datetime import datetime, timedelta
from weather import Root


def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)  # Set initial placeholder text
    entry.config(fg='grey')  # Set text color to grey
    
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)  # Remove placeholder text
            entry.config(fg='black',bg="white")  # Change text color to black

    def on_focus_out(event):
        if not entry.get():  # If entry is empty, restore placeholder
            entry.insert(0, placeholder_text)
            entry.config(fg='grey',bg="white")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def GetGraph(stationId : str = "",locationId : str = ""):
    locationEntry.config(bg="white")
    stationEntry.config(bg="white")
    #access API
    key = "oWSsVrjJsxktqHKyoGbSlpwZhoAKlHzL"
    #Get US States -> locations?locationcategoryid=ST&limit=52
    endpoint = "data"

    #Idaho -> FIPS:16
    #Sugar city station -> GHCND:USC00108818
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=5*365)  # Approx. 5 years
    url = f"https://www.ncei.noaa.gov/cdo-web/api/v2/{endpoint}"
    params = {
        "datasetid" : "GSOM", #retrieve all datasets by calling datasets w no params
        "stationid" : stationId,
        "datatypeid" : ["TAVG","TMAX","TMIN"],
        #"locationid": locationId,
        "startdate" : start_date.strftime("%Y-%m-%d"),
        "enddate" : end_date.strftime("%Y-%m-%d"),
        "limit" : "100" #25 is default
    }
    headers = {
        "token" : key
    }
    try:
        res = requests.get(url, headers = headers, params = params,timeout=10)
    except requests.exceptions.ReadTimeout:
        locationEntry.config(bg="#ffcccc")
        stationEntry.config(bg="#ffcccc")
        return
    
    data = res.json()
    if str(data) == "{}":  #empty res
        locationEntry.config(bg="#ffcccc")
        stationEntry.config(bg="#ffcccc")
        return
    root = Root.from_dict(data)
    
    
    #create pandas sheet
    results = root.results
    df = pd.DataFrame(results)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    # Plot Data
    fig = Figure(figsize = (7,6.25),
                 dpi = 100)

    #TODO: create 3 plots using the sub DF's (split as AVG, MIN, and MAX (see ~48))
    tavg = df[df["datatype"] == "TAVG"]
    tmin = df[df["datatype"] == "TMIN"]
    tmax = df[df["datatype"] == "TMAX"]

    plt1 = fig.add_subplot(111)
    plt1.plot(tavg['date'], (tavg["value"] * 9/5)+32, label="Avg Temperature", color="#cc8c48", marker="v")
    plt1.plot(tmin['date'], (tmin["value"] * 9/5)+32, label="Min Temperature", color="#01a6ae", marker=".")
    plt1.plot(tmax['date'], (tmax["value"] * 9/5)+32, label="Max Temperature", color="#d10000", marker=".")
    # plt.axhline(y=25, color="#00df14", linestyle="--")
    # plt.axhline(y=20, color="#00a10f", linestyle="--")
    y_top = plt1.get_ylim()[1]
    y_bott = plt1.get_ylim()[0]

    #set zones
    plt1.fill_between(df['date'],90,y_top,color = "#fd2f2f",alpha=0.5) #heatstroke warning
    plt1.fill_between(df['date'],80,y_top,color = "#ff5b5b",alpha=0.5) #mild heat warning
    plt1.fill_between(df['date'],5,80,color = "#d9ffdc",alpha=0.5) #Larger safe
    plt1.fill_between(df['date'], 68, 77, color='#7cda85', alpha=0.5) #optimal
    plt1.fill_between(df['date'],y_bott,5,color = "#5badff",alpha=0.5) #cold
    

    plt1.set_xlabel("Date")
    plt1.set_ylabel("Average Temperature")
    plt1.set_title("Temp by month")
    plt1.tick_params(axis = "x",rotation=30)
    canvas =  FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().pack() 
  
    # creating the Matplotlib toolbar 
    toolbar = NavigationToolbar2Tk(canvas, 
                                   window) 
    toolbar.update() 
  
    # placing the toolbar on the Tkinter window 
    canvas.get_tk_widget().pack() 
    


window = tk.Tk()
window.title("LT Weather Predictions")
window.geometry("900x700")
#add stationId textBox (or location box w conv to stationId)
plot_button = tk.Button(master = window,
                        command = lambda: GetGraph(stationEntry.get(),locationEntry.get()),
                        height = 2,
                        width = 10,
                        text = "Plot")
plot_button.pack(side = tk.TOP,padx=5,pady=5)

stationEntry = tk.Entry(master = window,
                        width = 20)
stationEntry.pack(side = tk.TOP,padx=5,pady=5)
add_placeholder(stationEntry,"Station ID")

locationEntry = tk.Entry(master = window,
                         width = 20,
                         text = "Plot")
locationEntry.pack(side = tk.TOP,padx=5,pady=5)
add_placeholder(locationEntry,"Location ID")

window.mainloop()

#GHCND:USC00107644
#FIPS:16
