"""
date : 08-03-2023
developer : scihack/powerpizza
description : I don't like to practice clicking so I use python for help!
"""

import tkinter, json
from tkinter import *
import tkinter.messagebox as messagebox
from classes_and_functs import  *
from pynput.keyboard import Listener as KB_Listener
from pynput.keyboard import KeyCode, Key
from pynput.mouse import Listener as MOS_Listener
from pynput.mouse import Button as pynput_btn

# Constants and variables
# 14 DB - 45 cps max, 15 DB - 30 cps max
default_settings = {
    "WINDOW": {
        "transparency_max": 1,
        "transparency_min": 0.4
    },

    "CLICKER": {
        "debounce_min": 14,
        "debounce_max": 28,
        "debounce_segments": 10,
        "cps_change_in": 2,
        "click_repeat": 1,
        "start_event": {"triggers": ["q"]},
        "stop_event": {"triggers": ["scroll"]}
    },

    "BUILDER": {
        "debounce_min": 5,
        "debounce_max": 5,
        "debounce_segments": 1,
        "cps_change_in": 3,
        "click_repeat": 1,
        "readyAt_event": {"triggers": ["r"]},
        "start_event": {"triggers": ["Button.right"]},
        "stop_event": {"triggers": ["Button.right"]}
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

settings_desc = {
    "WINDOW": "gui window settings.",
    "transparency_max": "max opacity of window. It is constant [1].",
    "transparency_min": "min opacity of window. It must be in range 0 to 1 decimal value.",
    "CLICKER": "auto clicker settings. it press right button of mouse.",
    "debounce_min": "minimum debounce in milli-seconds. It must be integer.",
    "debounce_max": "maximum debounce in milli-seconds. It must be integer and greater then or equal to minimum debounce.",
    "debounce_segments": "possibilities of cps change after 1 click. It help to bypass anti-cheat. It must be integer and less then maximum debounce.",
    "click_repeat": "number of clicks trigger at once. It must be integer.",
    "readyAt_event": "it ready builder for start clicking if the listed key is pressed.",
    "start_event": "it start the tool if the listed key is pressed.",
    "stop_event": "it stop the tool if the listed key is pressed.",
    "triggers": "click the record button then press mouse or keyboard buttons.",
    "cps_change_in": "it change cps after given seconds automatically between the range of debounce_min to debounce_max. It must be in seconds and integer."
}

int_type_settings = ["transparency_min", "debounce_min", "debounce_max", "debounce_segments", "click_repeat", "cps_change_in"]
key_type = ["triggers"]
const_settings = ["transparency_max"]

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
    ms_clicker = MouseControl(debounce_min=default_settings["CLICKER"]["debounce_min"],
                               debounce_max=default_settings["CLICKER"]["debounce_max"],
                               debounce_segment=default_settings["CLICKER"]["debounce_segments"],
                              change_after=default_settings["CLICKER"]["cps_change_in"],
                              func=lambda: change_btn_color(btn_auto_clc, ["red", "green", "blue", "gold"]))
    ms_clickers.append(ms_clicker)
    btn_auto_clc.config(state="disabled")

    def clicker_(*evs):
        # cur_event = None
        if len(evs) == 1 and type(evs[0]) == KeyCode:
            cur_event = evs[0].char
        elif len(evs) > 1 and evs[2] == 0:
            cur_event = "scroll"
        elif len(evs) > 1:
            cur_event = str(evs[2])
        else:
            print(evs)
            return

        if cur_event in default_settings["CLICKER"]["start_event"]["triggers"]:
            ms_clicker.start_clicking(btn=pynput_btn.right,
                               click_repeat=default_settings["CLICKER"]["click_repeat"])
        elif cur_event in default_settings["CLICKER"]["stop_event"]["triggers"]+default_settings["BUILDER"]["readyAt_event"]["triggers"]:
            ms_clicker.stop_clicking()
            btn_auto_clc.config(bg="blue")

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
    ms_clicker = MouseControl(debounce_min=default_settings["BUILDER"]["debounce_min"],
                              debounce_max=default_settings["BUILDER"]["debounce_max"],
                              debounce_segment=default_settings["BUILDER"]["debounce_segments"],
                              change_after=default_settings["BUILDER"]["cps_change_in"],
                              func=lambda: change_btn_color(btn_build, ["red", "green", "blue", "gold"]))
    ms_clickers.append(ms_clicker)
    start_permission = 0
    btn_build.config(state="disabled")

    def clicker_(*evs):
        if not evs[-1]:
            return

        nonlocal start_permission
        # cur_event = None
        if len(evs) == 1 and type(evs[0]) == KeyCode:
            cur_event = evs[0].char
        elif len(evs) > 1 and evs[2] == 0:
            cur_event = "scroll"
        elif len(evs) > 1:
            cur_event = str(evs[2])
        else:
            print(evs)
            return

        if cur_event in default_settings["BUILDER"]["readyAt_event"]["triggers"]:
            start_permission = 1
            btn_build.config(bg="yellow")

        elif cur_event in default_settings["BUILDER"]["start_event"]["triggers"] and start_permission and not ms_clicker.is_running():
            ms_clicker.start_clicking(btn=pynput_btn.left,
                               click_repeat=default_settings["BUILDER"]["click_repeat"])
        elif cur_event in default_settings["CLICKER"]["start_event"]["triggers"]:
            ms_clicker.stop_clicking()
            start_permission = 0
            btn_build.config(bg="blue")

        elif cur_event in default_settings["BUILDER"]["stop_event"]["triggers"] and start_permission:
            ms_clicker.stop_clicking()
            btn_build.config(bg="yellow")

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


# help work start
def on_click_help():
    help_win = tkinter.Tk()
    help_win.geometry("500x500")
    help_win.attributes("-topmost", True)
    help_win.title("help")
    help_win.config(bg="white")
    help_win.resizable(False, False)
    icon_2 = PhotoImage(file="fab_icon.png", master=help_win)
    help_win.iconphoto(False, icon_2)

    scrolled = 0
    def on_scroll(*x):
        nonlocal scrolled
        scroll_speed_ = 100
        if -1*(x[0].delta/120) > 0 and canvas_content.winfo_y()+scroll_speed_ <= 0:
            scrolled += scroll_speed_ # down scroll
        elif -1*(x[0].delta/120) < 0 and canvas_content.winfo_height() + scrolled - scroll_speed_ >= help_win.winfo_height():
            scrolled -= scroll_speed_ # up scroll
        canvas_content.place(y=scrolled)

    help_win.bind("<MouseWheel>", on_scroll)

    def create_subheading(text, font_size, ul="bold", fg="black"):
        fr_ = Frame(canvas_content, bg="white")
        lb_ = Label(fr_, text=text, font=("Helvetica", font_size, "bold", ul), bg="white", fg=fg, wraplength=480)
        lb_.pack(side=LEFT, pady=2, anchor="nw")
        fr_.pack(fill="x")

    def create_paragraph(text, font_size, fg="black"):
        fr_ = Frame(canvas_content, bg="white")
        lb_ = Label(fr_, text=text, font=("Helvetica", font_size), bg="white", wraplength=480, fg=fg)
        lb_.pack(pady=2, side=LEFT, ipadx=5)
        fr_.pack(fill="x")

    canvas_content = Canvas(help_win, bg="white")
    heading = Label(canvas_content, text="HELP", font=("Helvetica", 24, "bold"), bg="white")
    heading.pack(pady=2)

    create_subheading("How to use provided options :-", 18, ul="underline")
    create_subheading("OPT-1. Auto Clicker :-", 16, ul="underline")
    para_1 = f"""Click on auto clicker button to start the tool then trigger any of `{default_settings['CLICKER']['start_event']['triggers']}` for start clicking this tool will automatically press right mouse button of mouse. For stop clicking trigger any of `{default_settings['CLICKER']['stop_event']['triggers']}`."""
    create_paragraph(para_1, 16)

    create_subheading("OPT-2. Builder :-", 16, ul="underline")
    para_2 = f"""Click on builder button to start the tool then trigger any of `{default_settings['BUILDER']['readyAt_event']['triggers']}` by which tool will ready for clicking then trigger any of `{default_settings['BUILDER']['start_event']['triggers']}` for start clicking this tool will automatically press left mouse button of mouse. For temporary stop clicking trigger any of `{default_settings['BUILDER']['stop_event']['triggers']}` it will stop clicking temporally to stop this tool permanent trigger any of `{default_settings['CLICKER']['start_event']['triggers']}`."""
    create_paragraph(para_2, 16)

    create_subheading("OPT-3. Stop all :-", 16, ul="underline")
    para_3 = f"""This button stop all the running tools permanently and they will not start till you not press the tool buttons again."""
    create_paragraph(para_3, 16)

    create_subheading("OPT-4. Settings [⚙] :-", 16, ul="underline")
    para_4 = f"""This button help to change and save the settings of tools. You can open settings window by clicking this button and from settings window you can change the setting like debounce, click repeat etc. Descriptions of all settings are given in settings window just click the setting you want to change then you see a description box appear follow the instructions given in description box. After changing the settings carefully save them by clicking 'save & load settings' button in settings window."""
    create_paragraph(para_4, 16)

    create_subheading("CAUTIONS :-", 18, ul="underline")
    para_5 = """Please be careful while changing the settings there are some sensitive values if they were putted wrong so the software may be crash. Carefully give triggers of keyboard and mouse in settings while changing if these values are not given in correct syntax so it may cause trouble to your device. Avoid giving same triggers in start_event and stop_event it may cause non-stop clicking."""
    create_paragraph(para_5, 16)

    create_subheading("DEBUG :-", 18, ul="underline")
    para_6 = """If you done some changes in settings and they cause software crashing continuously so you just have to open this pc search for .configs.json file and delete it. It is the config file it can restored by software as you run it again."""
    create_paragraph(para_6, 16)

    create_subheading("DEVELOPER'S CONTACT :-", 18, ul="underline", fg="green")
    my_info = Text(canvas_content, width=0, height=6, font=("Helvetica", 14), bd=0, highlightcolor="black", highlightbackground="black", highlightthickness=1)
    my_info.insert(END, "Name : Scihack or PowerPizza\n")
    my_info.insert(END, "Github : https://github.com/powerpizza\n")
    my_info.insert(END, "Discord : scihack223 #4934\n")
    my_info.insert(END, "Youtube : https://www.youtube.com/channel/UCFHxcui4fu2Sxf3RFj03h_Q\n")
    my_info.pack(fill="x", padx=2)
    my_info.config(state="disabled")
    create_paragraph("Note : Kindly report this software's bug. Contacts are given above.", 16)

    canvas_content.pack(fill="both", expand=True, anchor="nw")
    # canvas_content.place(x=0, y=0)
    help_win.mainloop()

btn_help = Button(root, text="?", bd=3, bg="blue", font=("Calibri", 12, "bold"),fg="yellow", padx=2, pady=1,
                  command=on_click_help)
btn_help.place(x=175, y=72)
# help work end


# Settings work start
def onClick_Settings():
    on_stop_all()

    settings_root = tkinter.Tk()
    settings_root.geometry("400x400")
    settings_root.title("Settings")
    settings_root.resizable(False, False)
    settings_root.attributes("-topmost", True)
    icon_3 = PhotoImage(file="fab_icon.png", master=settings_root)
    settings_root.iconphoto(False, icon_3)

    options_canvas = Canvas(settings_root, bg="white")
    options_list = Listbox(options_canvas, font=("Helvetica", 12))
    options_list.insert(0, "⬆ Back")
    for itm in default_settings:
        options_list.insert(END, itm)

    # options_list.pack(pady=2, side=LEFT, fill="both", anchor="n")
    options_list.pack(fill="both", expand=True, anchor="n")
    options_canvas.pack(pady=2, side=LEFT, fill="both", anchor="n")

    load_from = default_settings
    selected_key = None
    last_visited = []
    def onSelectOption(*eve):
        nonlocal load_from, last_visited, selected_key
        value_ = options_list.get(ANCHOR)
        desc_label.pack_forget()

        if not value_:
            return 0

        elif "Back" in value_:
            if not len(last_visited):
                return
            options_list.delete(1, END)
            for itm2 in last_visited[-1]:
                options_list.insert(END, itm2)
            load_from = last_visited[-1]
            last_visited.remove(last_visited[-1])

            modified_text = label_path["text"].split("/")
            modified_text.remove(modified_text[-1])
            label_path.config(text="/".join(modified_text))

        elif type(load_from[value_]) == dict:
            options_list.delete(1, END)
            for itm2 in load_from[value_]:
                options_list.insert(END, itm2)
            last_visited.append(load_from)
            load_from = load_from[value_]
            if value_ not in label_path["text"]:
                label_path.config(text=label_path["text"] + "/" + value_)

        else:
            selected_key = value_
            label_value.config(text=f"Value : {load_from[selected_key]}")

            record_button.pack_forget()
            event_list.pack_forget()
            clear_prev_events.pack_forget()
            frame_entry.pack_forget()
            entry_value.config(state="normal")
            apply_button.config(state="normal")

            if selected_key in int_type_settings:
                frame_entry.pack(pady=2, padx=2, fill=X)
                val_ue.set(load_from[selected_key])

            elif selected_key in key_type:
                label_value.config(text=f"Value :-")
                event_list.delete(0, END)
                for itm3 in load_from[selected_key]:
                    event_list.insert(END, itm3)
                event_list.pack(padx=2, fill="x")
                record_button.pack(padx=2, fill="x")
                clear_prev_events.pack(padx=2, pady=2, fill="x")

            elif selected_key in const_settings:
                frame_entry.pack(pady=2, padx=2, fill=X)
                entry_value.config(state="disabled")
                apply_button.config(state="disabled")
                val_ue.set(load_from[selected_key])

        if value_ in settings_desc:
            desc_label.config(text="Description : "+settings_desc[value_])
            desc_label.pack(fill="x", pady=2, expand=True)


    options_list.bind("<<ListboxSelect>>", onSelectOption)

    # External Gui
    editing_canvas = Canvas(settings_root, width=100, height=100, bg="white")

    label_value = Label(editing_canvas, text="Value : None", bg="yellow", font=("Helvetica", 12), wraplength=200)
    label_value.pack(fill="x", padx=2)
    label_path = Label(editing_canvas, text="settings", bg="gold", font=("Helvetica", 12), wraplength=200)
    label_path.pack(fill="x", padx=2)

    # ----- For int type inputs ------
    val_ue = DoubleVar(editing_canvas)

    frame_entry = Frame(editing_canvas, background="white")
    entry_value = Entry(frame_entry, textvariable=val_ue, highlightbackground="blue", highlightcolor="blue",
                        highlightthickness=2, bg="white", relief="solid", font=("Helvetica", 12), width=5)
    def on_apply():
        try:
            load_from[selected_key] = val_ue.get()
            print(default_settings)
        except BaseException:
            messagebox.showerror("error", "unable to set value!")

    apply_button = Button(frame_entry, text="✔", font=("Helvetica", 11), fg="green", command=on_apply)

    entry_value.pack(side=LEFT, fill="x", expand=True)
    apply_button.pack(side=RIGHT, fill="x", padx=2)
    # ------ END ------

    # ------ For key and mouse type inputs -----
    def on_record_button():
        def stopper():
            keyboard_eve.stop()
            mos_eve.stop()
            record_button.config(text="Record Event ⏺", command=on_record_button)

        record_button.config(text="Stop ▶", command=stopper)

        def get_keys(*k):
            if type(k[0]) == KeyCode:
                load_from["triggers"].append(k[0].char)
                print(default_settings)

            elif k[0] == Key.esc:
                stopper()

            load_from["triggers"] = list(set(load_from["triggers"]))

            event_list.delete(0, END)
            for itm3 in load_from["triggers"]:
                print(itm3)
                event_list.insert(END, itm3)

        keyboard_eve = KB_Listener(on_press=get_keys)
        keyboard_eve.start()

        def get_btns(*b):
            if b[2] == 0:
                load_from["triggers"].append("scroll")
            else:
                load_from["triggers"].append(str(b[2]))
            load_from["triggers"] = list(set(load_from["triggers"]))

            event_list.delete(0, END)
            for itm3 in load_from["triggers"]:
                event_list.insert(END, itm3)

        mos_eve = MOS_Listener(on_click=get_btns, on_scroll=get_btns)
        mos_eve.start()

    def on_clearing_old_events():
        load_from["triggers"].clear()
        event_list.delete(0, END)
        for itm3 in load_from["triggers"]:
            event_list.insert(END, itm3)

    event_list = Listbox(editing_canvas, font=("Helvetica", 11))
    record_button = Button(editing_canvas, text="Record Event ⏺", font=("Helvetica", 11), command=on_record_button)
    clear_prev_events = Button(editing_canvas, text="Clear List", font=("Helvetica", 11), command=on_clearing_old_events)
    # ----- END ------

    # ----- Description Label -------
    desc_label = Label(editing_canvas, text="", bg="yellow", font=("Helvetica", 12), wraplength=200)
    # ----- END ------
    editing_canvas.pack(padx=1, pady=2, anchor="nw", fill="both", expand=True)
    # ------ END -----

    def save_n_load():
        with open(".configs.json", "w") as fp:
            json.dump(default_settings, fp)

    save_settings_btn = Button(options_canvas, text="Save & Load Settings", bg="green", fg="yellow", command=save_n_load)
    save_settings_btn.pack(pady=2, padx=2)

    settings_root.mainloop()

settings_btn = Button(root, text="⚙", font=("Helvetica", 18, "bold"), bg="green", relief="ridge",
                      command=onClick_Settings)
settings_btn.place(x=0, y=148)
# Settings work end

root.mainloop()
