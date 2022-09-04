# This will import all the widgets 
# and modules which are available in 
# tkinter and ttk module 

import time
import tkinter as tk
from datetime import datetime

#import webbrowser
#webbrowser.open("https://youtu.be/c1x-k1JlFnw")

def printTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


class MyDialog:
    def __init__(self, parent):

        self.top = tk.Toplevel(parent)
        self.top.geometry("300x150+" + str(int(parent.winfo_screenwidth()/2 - parent.winfo_reqwidth()/2) - 150) + "+" + str(int(parent.winfo_screenheight()/2 - parent.winfo_reqheight()/2) - 75))

        tk.Label(self.top, text="\n \nHow are you feeling (from 1 to 5)?").pack()

        self.e = tk.Entry(self.top)
        self.e.pack(padx=5,pady=5)
        
        a = tk.Button(self.top, text="Enter", command=self.ok)
        a.pack(pady=5)

    def ok(self):
        print("Level of Comfort is: " + str(self.e.get()))
        self.top.destroy()
        self.top.quit()


# ============================================================================

total = int(input("What's your time recording duration (in minutes): ")) 
remind = int(input("How often you want to be reminded (every __ seconds): "))
print("\n")

repeat = int((60*total) / remind)    

for i in range(repeat):    
    root = tk.Tk()
    root.title("Question")
    tk.Button(root, text="Hello!").pack()
    root.withdraw()
    root.update()
    
    start = time.time()
    printTime()
    d = MyDialog(root)
    root.wait_window(d.to10p)
    
    while(time.time() - start <= remind):
        duration = time.time() - start
        if (i == repeat-1):
            break
        if(duration % 1 == 0):
            print(duration)
    
