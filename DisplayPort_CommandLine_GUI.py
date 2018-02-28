from tkinter import N, E, S, W, filedialog, OptionMenu, Button, Label, StringVar, Tk
import subprocess
import logging

class DP_GUI:
    output_txt = ""
    def __init__(self, master):
        self.master = master
        master.minsize(width=750, height=200)
        master.title("DisplayPort Signal Control")

        logging.info("Initial height: {}\nInitial Width: {}".format(master.winfo_height(), master.winfo_width()))

        # Create string varaibles to show hold current selections
        DP_GUI.output_txt = StringVar()
        DP_GUI.sink, DP_GUI.pat, DP_GUI.bit, DP_GUI.pre, DP_GUI.vol = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()

        # Create stationary labels to show category for each choice & set them on the grid
        sink0 = Label(master, text = "Port:").grid(row = 1, column = 4, sticky = E)
        pat0 = Label(master, text="Pattern:").grid(row=2, column=4, sticky=E)
        bit0 = Label(master, text="Data Rate:").grid(row=3, column=4, sticky=E)
        pre0 = Label(master, text="Pre-emphasis:").grid(row=4, column=4, sticky=E)
        vol0 = Label(master, text="Voltage Swing:").grid(row=5, column=4, sticky=E)

        # Create labels for each variable
        self.output_display = Label(master, textvariable=DP_GUI.output_txt)
        self.sinktxt = Label(master, textvariable=DP_GUI.sink)
        self.pattxt = Label(master, textvariable = DP_GUI.pat)
        self.bittxt = Label(master, textvariable=DP_GUI.bit)
        self.pretxt = Label(master, textvariable=DP_GUI.pre)
        self.voltxt = Label(master, textvariable=DP_GUI.vol)

        # set variable values to their default outputs
        DP_GUI.output_txt.set("Your current command is: \nHost_DP_Tx_AR")
        DP_GUI.sink.set("")
        DP_GUI.pat.set("")
        DP_GUI.bit.set("")
        DP_GUI.pre.set("")
        DP_GUI.vol.set("")

        self.output_display.grid(row=6, column = 2, sticky=W + E)
        self.sinktxt.grid(row = 1, column = 5, sticky = E)
        self.pattxt.grid(row=2, column=5, sticky=E)
        self.bittxt.grid(row=3, column=5, sticky=E)
        self.pretxt.grid(row=4, column=5, sticky=E)
        self.voltxt.grid(row=5, column=5, sticky=E)

        self.bit_var = StringVar(master)
        self.pat_var = StringVar(master)
        self.volt_var = StringVar(master)
        self.preemp_var = StringVar(master)
        self.sink_var = StringVar(master)

        self.setDefaultVals()

        self.bitrate = OptionMenu(master, self.bit_var, "HBR2", "HBR", "RBR", command = lambda x: self.updateOutputTxt())  # HBR2 = 5.4, HBR = 2.7, RBR = 1.62
        self.pattern = OptionMenu(master, self.pat_var, "D10.2", "PRBS7", "PLTPAT", "HBR2CPAT", command = lambda x: self.updateOutputTxt())
        self.voltage_swing = OptionMenu(master, self.volt_var, "400mV", "600mV", "800mV",  command = lambda x: self.updateOutputTxt()) # 400mV = 0, 600mV = 1, 800mV = 2"
        self.pre_emphasis = OptionMenu(master, self.preemp_var, "0dB", "3.5dB", "6dB",  command = lambda x: self.updateOutputTxt()) # 0dB = 0, 3.5dB = 1, 6dB = 2
        self.sink = OptionMenu(master, self.sink_var, "Port A (top)", "Port B (bottom)", command = lambda x: self.updateOutputTxt()) # Port A = sink1, PA, Port B = sink2, PB;

        b_label = Label(master, text = "Data Rate: ").grid(row = 3, column = 0, sticky = W)
        p_label = Label(master, text = "Pattern: ").grid(row = 2, column = 0, sticky = W)
        v_label = Label(master, text = "Voltage Swing").grid(row = 5, column = 0, sticky = W)
        pr_label = Label(master, text="Pre-Emphasis: ").grid(row=4, column=0, sticky=W)
        s_label = Label(master, text = "Sink and Port: ").grid(row = 1, column = 0, sticky = W)

        self.bitrate.grid(row = 3, column = 1, sticky = W)
        self.pattern.grid(row = 2, column = 1, sticky = W)
        self.voltage_swing.grid(row = 5, column = 1, sticky = W)
        self.pre_emphasis.grid(row=4, column=1, sticky=W)
        self.sink.grid(row = 1, column = 1, sticky = W)

        send_command = Button(master, text = "Send Command", command = lambda: self.sendCommand(), bg = "salmon")
        send_command.grid(row = 7, column = 2, sticky = W + E)

        master.grid_columnconfigure(2, minsize = 350)

    def updateOutputTxt(self):
        DP_GUI.output_txt.set("Your current command is: \n"
                              "Host_DP_Tx_AR {} {} {} {} {} {}".format(*self.parseCommand()))
        logging.info("Current height: {}\nCurrent Width: {}".format(self.master.winfo_height(), self.master.winfo_width()))

        DP_GUI.sink.set(self.sink_var.get())
        DP_GUI.pat.set(self.pat_var.get())
        DP_GUI.bit.set(self.bit_var.get())
        DP_GUI.pre.set(self.preemp_var.get())
        DP_GUI.vol.set(self.volt_var.get())


    def parseCommand(self):
        val_dict = {
            "HBR2": "5.4",
            "HBR": "2.7",
            "RBR": "1.62",
            "400mV": '0',
            "600mV": "1",
            "800mV": "2",
            "0dB": "0",
            "3.5dB": "1",
            "6dB": "2",
            "Port A (top)": ["sink1", "PA"],
            "Port B (bottom)": ["sink2", "PB"]
        }

        try:
            cmd_list = [val_dict[self.bit_var.get()], self.pat_var.get(), val_dict[self.volt_var.get()],
                        val_dict[self.preemp_var.get()], val_dict[self.sink_var.get()][0], val_dict[self.sink_var.get()][1]]
            print(cmd_list)
            return cmd_list

        except KeyError as e:
            print("Error: All values must be selected before sending command")
            raise KeyError

    def sendCommand(self):

       command = "cmd /c Host_DP_Tx_AR {} {} {} {} {} {}".format(*self.parseCommand())
       logging.info(command)
       subprocess.call(command.split(), shell=False)


    def setDefaultVals(self):
        self.bit_var.set("HBR2")
        self.pat_var.set("HBR2CPAT")
        self.volt_var.set("400mV")
        self.preemp_var.set("0dB")
        self.sink_var.set("Port A (top)")

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    # logger = logging.getLogger("GUI")
    # logger.setLevel(logging.INFO)
    root = Tk()
    my_gui = DP_GUI(root)
    root.mainloop()