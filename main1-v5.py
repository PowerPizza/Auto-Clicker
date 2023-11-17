"""
date : 08-03-2023
developer : scihack/powerpizza
description : I don't like to practice clicking so I use python for help!
"""
import time
import tkinter, json
from tkinter import *
import tkinter.messagebox as messagebox
from classes_and_functs import  *
from pynput.keyboard import Listener as KB_Listener
from pynput.keyboard import KeyCode, Key
from pynput.mouse import Listener as MOS_Listener
from pynput.mouse import Button as pynput_btn

default_settings = {
    "WINDOW": {
        "transparency_max": 1,
        "transparency_min": 0.4
    },

    "CLICKER": {
        "debounce": 100,
        "click_repeat": 1,
        "start_key": "q",
        "stop_key": "scroll"
    },

    "BUILDER": {
        "debounce": 300,
        "click_repeat": 1,
        "start_key": "r",
        "stop_key": "scroll"
    },
}

def load_settings_from_file():
    global default_settings
    try:
        with open(".configs.json", "r") as fp:
            default_settings = json.load(fp)
    except BaseException:
        with open(".configs.json", "w") as fp:
            json.dump(default_settings, fp)
load_settings_from_file()  # comment this line while testing.


ms_clickers = []
kb_ms_listners = []
# ------ end --------


root = tkinter.Tk()
root.attributes("-topmost", True)
root.title("HEX")
root.resizable(False, False)
root.bind("<Button-1>", lambda event: root.attributes("-alpha", 1))
root.bind("<Button-3>", lambda event: root.attributes("-alpha", default_settings["WINDOW"]["transparency_min"]))
icon_ = PhotoImage(file="fab_icon.png", master=root)
root.iconphoto(False, icon_)

lbl_tool = Label(root, text="Tools", font=("Calibri", 16, "bold"), bg="yellow", width=18)
lbl_tool.place(x=0, y=0)

under_line1 = Frame(root, width=200, height=6, bg="black")
under_line1.place(x=0, y=27)

under_line2 = Frame(root, width=200, height=6, bg="black")
under_line2.place(x=0, y=109)

# autoclicker work start
def change_btn_color(btn:Button, colors_:list):
    btn.config(bg=random.choice(colors_))

def on_click_ac():
    ms_clicker = MouseControl(debounce_=default_settings["CLICKER"]["debounce"],
                              func=lambda: change_btn_color(btn_auto_clc, ["red", "green", "blue", "gold"]))
    ms_clickers.append(ms_clicker)
    btn_auto_clc.config(state="disabled")

    def clicker_(*evs):
        if len(evs) == 1 and type(evs[0]) == KeyCode and str(evs[0]) == f"'{default_settings['CLICKER']['start_key']}'":
            ms_clicker.start_clicking(btn=pynput_btn.right, click_repeat=default_settings["CLICKER"]["click_repeat"])

        elif len(evs) > 1 and evs[2] == 0:
            ms_clicker.stop_clicking()
            btn_auto_clc.config(bg="blue")

        elif len(evs) == 1 and type(evs[0]) == KeyCode and str(evs[0]) == f"'{default_settings['BUILDER']['start_key']}'":
            ms_clicker.stop_clicking()
            btn_auto_clc.config(bg="blue")

        else:
            print(evs)
            return

    kb_eve = KB_Listener(on_press=clicker_)
    ms_eve = MOS_Listener(on_click=clicker_, on_scroll=clicker_)
    kb_eve.start()
    ms_eve.start()
    kb_ms_listners.append(kb_eve)
    kb_ms_listners.append(ms_eve)

btn_auto_clc = Button(root, text="Auto Clicker", bd=3, bg="blue", font=("Calibri", 12, "bold"), fg="yellow",
                      padx=20, width=6, command=on_click_ac)
btn_auto_clc.place(x=3, y=35)
# autoclicker work end

# Builder work start
def on_click_b():
    ms_clicker = MouseControl(debounce_=default_settings["BUILDER"]["debounce"], func=lambda: change_btn_color(btn_build, ["red", "green", "blue", "gold"]))
    ms_clickers.append(ms_clicker)
    start_permission = 0
    btn_build.config(state="disabled")

    def clicker_(*evs):
        if not evs[-1]:
            return

        nonlocal start_permission
        if len(evs) == 1 and type(evs[0]) == KeyCode and str(evs[0]) == f"'{default_settings['BUILDER']['start_key']}'":
            start_permission = 1
            btn_build.config(bg="yellow")
            print("its started")

        elif len(evs) > 1 and evs[2] == pynput_btn.right and start_permission and not ms_clicker.is_running():
            ms_clicker.start_clicking(btn=pynput_btn.left, click_repeat=default_settings["BUILDER"]["click_repeat"])

        elif len(evs) > 1 and evs[2] == pynput_btn.right and start_permission and ms_clicker.is_running():
            ms_clicker.stop_clicking()
            btn_build.config(bg="yellow")

        elif len(evs) > 1 and evs[2] == 0 and start_permission:
            ms_clicker.stop_clicking()
            btn_build.config(bg="yellow")

        elif len(evs) == 1 and type(evs[0]) == KeyCode and str(evs[0]) == f"'{default_settings['CLICKER']['start_key']}'":
            ms_clicker.stop_clicking()
            start_permission = 0
            btn_build.config(bg="blue")

        else:
            print(evs)
            return

    kb_eve = KB_Listener(on_press=clicker_)
    ms_eve = MOS_Listener(on_click=clicker_, on_scroll=clicker_)
    kb_eve.start()
    ms_eve.start()
    kb_ms_listners.append(kb_eve)
    kb_ms_listners.append(ms_eve)

btn_build = Button(root, text="Builder", bd=3, bg="blue", font=("Calibri", 12, "bold"), fg="yellow",
                   padx=20, width=6, command=on_click_b)
btn_build.place(x=3, y=72)
# Builder work end

# stop all work start
def on_stop_all():
    for itm in ms_clickers:
        itm.stop_clicking()
    ms_clickers.clear()
    for itm in kb_ms_listners:
        itm.stop()
    kb_ms_listners.clear()

    btn_build.config(bg="blue", state="normal")
    btn_auto_clc.config(bg="blue", state="normal")


stop_all = Button(root, text="Stop all", bd=3, bg="blue", font=("Calibri", 12, "bold"), fg="yellow",
                  command=on_stop_all)
stop_all.place(x=105, y=72)
# stop all work end


# Settings work start
def onClick_Settings():
    settings_btn.config(state="disabled")
    on_stop_all()

    settings_root = tkinter.Tk()
    settings_root.geometry("400x400")
    settings_root.title("Settings")
    settings_root.resizable(False, False)
    settings_root.attributes("-topmost", True)
    icon_3 = PhotoImage(file="fab_icon.png", master=settings_root)
    settings_root.iconphoto(False, icon_3)

    def on_win_destroy():
        global default_settings
        default_settings = old_settings
        settings_btn.config(state="normal")
        settings_root.destroy()
    settings_root.protocol("WM_DELETE_WINDOW", on_win_destroy)

    old_settings = default_settings

    options_canvas = Canvas(settings_root, bg="white")

    frame_opt_1 = Frame(options_canvas, bg="#FFFFFF")
    lbl_opt_1 = Label(frame_opt_1, text="Debounce (AutoClicker)", font=("Helvetica", 14), bg="#FFFFFF")
    lbl_opt_1.pack(side=LEFT)
    def on_scale_change1(chang):
        default_settings["CLICKER"]["debounce"] = int(chang)
        update_status()
    range_scale_1 = Scale(frame_opt_1, orient="horizontal", from_=1, to=5000, command=on_scale_change1)
    range_scale_1.set(default_settings["CLICKER"]["debounce"])
    range_scale_1.pack(side=LEFT)
    lbl_closing_1 = Label(frame_opt_1, text="ms", font=("Helvetica", 14), bg="#FFFFFF")
    lbl_closing_1.pack(side=LEFT)
    frame_opt_1.pack(fill=X)


    frame_opt_2 = Frame(options_canvas, bg="#FFFFFF")
    lbl_opt_2 = Label(frame_opt_2, text="Click Repeat (AutoClicker)", font=("Helvetica", 14), bg="#FFFFFF")
    lbl_opt_2.pack(side=LEFT)
    def on_scale_change2(chang):
        default_settings["CLICKER"]["click_repeat"] = int(chang)
        update_status()
    range_scale_2 = Scale(frame_opt_2, orient="horizontal", from_=1, to=10, command=on_scale_change2)
    range_scale_2.set(default_settings["CLICKER"]["click_repeat"])
    range_scale_2.pack(side=LEFT)
    frame_opt_2.pack(fill=X)


    frame_opt_3 = Frame(options_canvas, bg="#FFFFFF")
    lbl_opt_3 = Label(frame_opt_3, text="Debounce (Builder)", font=("Helvetica", 14), bg="#FFFFFF")
    lbl_opt_3.pack(side=LEFT)
    def on_scale_change3(db_):
        default_settings["BUILDER"]["debounce"] = int(db_)
        update_status()
    range_scale_3 = Scale(frame_opt_3, orient="horizontal", from_=1, to=5000, command=on_scale_change3)
    range_scale_3.set(default_settings["BUILDER"]["debounce"])
    range_scale_3.pack(side=LEFT)
    lbl_closing_3 = Label(frame_opt_3, text="ms", font=("Helvetica", 14), bg="#FFFFFF")
    lbl_closing_3.pack(side=LEFT)
    frame_opt_3.pack(fill=X)


    frame_opt_4 = Frame(options_canvas, bg="#FFFFFF")
    lbl_opt_4 = Label(frame_opt_4, text="Click Repeat (AutoClicker)", font=("Helvetica", 14), bg="#FFFFFF")
    lbl_opt_4.pack(side=LEFT)
    def on_scale_change4(chang):
        default_settings["BUILDER"]["click_repeat"] = int(chang)
        update_status()
    range_scale_4 = Scale(frame_opt_4, orient="horizontal", from_=1, to=10, command=on_scale_change4)
    range_scale_4.set(default_settings["BUILDER"]["click_repeat"])
    range_scale_4.pack(side=LEFT)
    frame_opt_4.pack(fill=X)

    def update_status():
        db_AC = default_settings["CLICKER"]["debounce"]
        cr_AC = default_settings["CLICKER"]["click_repeat"]
        approx_cps_AC = "%.1f" % ((999/(1.3*db_AC)+1)*cr_AC)
        lbl_status_AC.config(text=f"---- AutoClicker ----\ndebounce = {db_AC} ms\nclick repeat = {cr_AC}\nCPS (approx) = {approx_cps_AC}")

        db_BD = default_settings["BUILDER"]["debounce"]
        cr_BD = default_settings["BUILDER"]["click_repeat"]
        approx_cps_BD = "%.1f" % ((999/(1.3*db_BD)+1)*cr_BD)
        lbl_status_BD.config(text=f"---- Builder ----\ndebounce = {db_BD} ms\nclick repeat = {cr_BD}\nCPS (approx) = {approx_cps_BD}")

    frame_status_view = Frame(options_canvas, bg="#FFFFFF")
    lbl_status_AC = Label(frame_status_view, text="", bg="#FFFFFF", font=("Helvetica", 12))
    lbl_status_AC.pack(side=LEFT)

    lbl_status_BD = Label(frame_status_view, text="---- Builder ----\ndebounce = x\nclick repeat = c\nCPS (approx) = p", bg="#FFFFFF", font=("Helvetica", 12))
    lbl_status_BD.pack(side=RIGHT)
    frame_status_view.pack(fill=X, side=BOTTOM)
    update_status()

    options_canvas.pack(fill=BOTH, expand=True)

    def on_save_settings():
        with open(".configs.json", "w") as fp:
            json.dump(default_settings, fp)
        settings_root.destroy()
        settings_btn.config(state="normal")

    btn_save_settings = Button(settings_root, text="Save Settings", bg="green", fg="white", font=("Helvetica", 12), command=on_save_settings)
    btn_save_settings.pack()

    settings_root.mainloop()

settings_btn = Button(root, text="⚙", font=("Helvetica", 18, "bold"), bg="green", relief="ridge",
                      command=onClick_Settings)
settings_btn.place(x=0, y=148)
# Settings work end

root.mainloop()
