from virtenv.include.appJar import gui
import virtenv.include.com_serial as ser
import webbrowser
import os
import virtenv.include.eeg_streamer as lsl_streamer
import json


def page_0(app):
    # gui for first page
    port = ser.serial_ports()

    label1, label2, label3=get_description()
    app.addLabel("Port", "Selecting Ports")

    app.addLabelOptionBox("Ports:", ["Standard"]+port)
    app.setOptionBoxChangeFunction("Ports:", port_selected)

    app.addButton("reloadPorts", reload_ports)

    app.addLabel("SelectedPort", "Port: Standard")

    app.addButton("Type1", select, 0, 3)
    app.addLabel("descr1", label1, 1, 3)

    app.addButton("Type2", do_nothing, 0, 5)
    app.setButtonState("Type2", "disabled")
    app.addLabel("descr2", label2, 1, 5)

    app.addButton("Type3",do_nothing, 0, 7)
    app.setButtonState("Type3", "disabled")
    app.addLabel("descr3", label3, 1, 7)

    app.addVerticalSeparator(0, 2, rowspan=5)
    app.addVerticalSeparator(0, 4, rowspan=5)
    app.addVerticalSeparator(0, 6, rowspan=5)

    app.setLabelRelief("descr1", app.SUNKEN)
    app.setLabelRelief("descr2", app.SUNKEN)
    app.setLabelRelief("descr3", app.SUNKEN)


def do_nothing():
    print("nothing done here")


def page_1(app, port=None, eeg_chosen="Mu waves"):
    #lsl=streamerlsl.StreamerLSL(port)
    sub_eeg_settings()

    app.addButton("Indietro", back, 0, 0)
    app.addButton("Settings", eeg_settings, 2, 0)

    app.addLabel("lab11", eeg_chosen, 0, 4)
    app.addButton("?", external_link, 0, 6)

    app.addLabel("description", "ciao", 1, 3, 3, 2)
    app.setLabelRelief("description", app.SUNKEN)
    get_arrow("left")
    #app.addImage("left arrow", get_arrow("left"))

    app.addLabel("Teach", "Teach NN", 3, 3)
    app.addLabel("Teach_RR", "**", 3, 4)
    app.addButton("Start Teaching", do_nothing, 4, 3)
    app.addButton("Stop Teaching", do_nothing, 4, 4)
    app.addButton("Load NN", do_nothing, 5, 3)
    app.addButton("Save NN", do_nothing, 5, 4)

    app.addLabel("FireNN", "Fire up", 3, 6)
    app.addButton("Start NN", do_nothing, 4, 6)
    app.addButton("Stop NN", do_nothing, 5, 6)

    app.addVerticalSeparator(3, 5, rowspan=3)
    app.addVerticalSeparator(0, 2, rowspan=6)
    app.addVerticalSeparator(0, 7, rowspan=6)
    if port is None or port == "" or port == "Standard":
        start_eeg()
    else:
        start_eeg(port)


def external_link(bt):
    webbrowser.open("https://en.wikipedia.org/wiki/Mu_wave")


def get_arrow(oor):
    temp = "virtenv/resources/"
    app.addImage(oor+" arrow", os.path.abspath(temp+oor+"_arrow.gif"), 1, 6)


def back(bt):
    shift_page(bt, app)


def shift_page(bt, page, temp=None):
    if bt == "Type1":
        page.removeAllWidgets()
        page_1(page, port=temp)

    elif bt == "Type2":
        page_1(page, port=app.getLabel("SelectedPort"))

    elif bt == "Type3":
        page_1(page, port=app.getLabel("SelectedPort"))

    elif bt == "Indietro":
        page.destroySubWindow("one")
        page.removeAllWidgets()
        page_0(page)


def eeg_settings():
    app.showSubWindow("one")


def sub_eeg_settings(lsl=None):
    app.startSubWindow("one", "Settings")
    app.addLabel("lb1", "EEG Channels Setting")
    app.stopSubWindow()


def get_description():
    label1 = "description 1\n\n\n\n"
    label2 = "description 2\n\n\n\n"
    label3 = "description 3\n\n\n\n"
    return label1, label2, label3


def select(lb):
    shift_page(lb, app, temp=app.getLabel("SelectedPort")[6:])


def port_selected():
    print("Porta: " + app.getOptionBox("Ports:"))
    app.setLabel("SelectedPort", "Porta: " + app.getOptionBox("Ports"))


def reload_ports():
    new_ser = ser.serial_ports()

    if new_ser.__len__()>0:
        app.changeOptionBox("Ports:", new_ser)


def start_eeg(port=None):
    print(port)
    lsl= lsl_streamer.Eeg_Streamer(port=port)


def start_NN():
    print("Start NN..\n")


app=gui("Pagina Principale", "800x550")
app.setResizable(False)
page_0(app)
app.go()
