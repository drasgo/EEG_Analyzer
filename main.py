from virtenv.include.appJar import gui
import virtenv.include.com_serial as ser
import virtenv.include.eeg_streamer as lsl_streamer
import virtenv.include.neural_network as neu_net
import webbrowser
import os
import pywt
import threading
import time
import json
import random
from pylsl import StreamInlet, resolve_stream
import numpy as np

__signalAcquisitionTime__ = 2


def page_0():
    # gui for first page
    port = ser.serial_ports()

    label1 = get_data("virtenv/resources/label1.json")
    label2 = get_data("virtenv/resources/label2.json")
    label3 = get_data("virtenv/resources/label3.json")

    app.addLabel("Port", "Selecting Ports", 0, 0)

    app.addLabelOptionBox("Ports:", ["Standard"]+port, 1, 0)
    app.setOptionBoxChangeFunction("Ports:", port_selected)

    app.addButton("R", reload_ports, 1, 1)

    app.addLabel("SelectedPort", "Port: Standard", 3, 0)

    app.addLabelEntry("Name: ", 4, 0)

    app.addButton("Type1", lambda: select(lb="Type1", nome=app.getEntry("Name: ")), 0, 3)
    app.setButton("Type1", "Mu Waves")
    app.addLabel("descr1", label1, 1, 3)

    app.addButton("Type2", do_nothing, 0, 5)
    app.setButtonState("Type2", "disabled")
    app.addLabel("descr2", label2, 1, 5)

    app.addButton("Type3", do_nothing, 0, 7)
    app.setButtonState("Type3", "disabled")
    app.addLabel("descr3", label3, 1, 7)

    app.addVerticalSeparator(0, 2, rowspan=5)
    app.addVerticalSeparator(0, 4, rowspan=5)
    app.addVerticalSeparator(0, 6, rowspan=5)
    app.addVerticalSeparator(0, 8, rowspan=5)

    app.setLabelRelief("descr1", app.SUNKEN)
    app.setLabelRelief("descr2", app.SUNKEN)
    app.setLabelRelief("descr3", app.SUNKEN)


def do_nothing():
    print("nothing done here")


def page_1(port=None, name="", eeg_chosen="Mu waves"):

    try:
        if port is None or port == "" or port == "Standard":
            lsl = lsl_streamer.Eeg_Streamer()
        else:
            lsl = lsl_streamer.Eeg_Streamer(port)
    except:
        shift_page(err_mess="LSL Error: Port not found")

    lsl.create_lsl()

    sub_eeg_settings()
    sub_eeg_infos(lsl)

    app.addButton("Indietro", shift_page, 0, 0)
    app.addButton("Settings", eeg_settings, 2, 0)
    app.addButton("Informations", eeg_infos, 4, 0)

    app.addLabel("lab11", eeg_chosen, 0, 4)
    app.addButton("?", external_link, 0, 6)

    app.addLabel("description", "ciao", 1, 3, 3, 2)
    app.setLabelRelief("description", app.SUNKEN)
    get_arrow("left")

    # app.addImage("left arrow", get_arrow("left"))

    app.addLabel("Teach", "Teach NN", 3, 3)
    app.addLabel("Teach_RR", "**", 3, 4)
    app.addButton("Start Teaching", lambda: start_teaching(lsl, name), 4, 3)
    app.addButton("Stop Teaching", lambda: stop_acq_data_teach_nn(lsl), 4, 4)
    app.addButton("Load NN", do_nothing, 5, 3)
    app.addButton("Save NN", do_nothing, 5, 4)

    app.addLabel("FireNN", "Fire up", 3, 6)
    app.addButton("Start NN", do_nothing, 4, 6)
    app.addButton("Stop NN", do_nothing, 5, 6)

    app.addVerticalSeparator(3, 5, rowspan=3)
    app.addVerticalSeparator(0, 2, rowspan=6)
    app.addVerticalSeparator(0, 7, rowspan=6)


def err_page(problem=""):
    app.addTextArea("Attenzione")
    app.setTextArea("Attenzione", problem)
    app.addButton("Indietro", shift_page)


def external_link():
    webbrowser.open("https://en.wikipedia.org/wiki/Mu_wave")


def get_arrow(oor):
    temp = "virtenv/resources/"
    app.addImage(oor+" arrow", os.path.abspath(temp+oor+"_arrow.gif"), 1, 6)


def shift_page(bt="", port=None, nome="", err_mess=""):
    if bt == "Type1":
        app.removeAllWidgets()
        page_1(port=port, name=nome)

    elif bt == "Type2":
        page_1(port=app.getLabel("SelectedPort"))

    elif bt == "Type3":
        page_1(port=app.getLabel("SelectedPort"))

    elif bt == "Indietro":
        try:
            app.destroySubWindow("settings")
        except:
            pass
        try:
            app.destroySubWindow("infos")
        except:
            pass
        app.removeAllWidgets()
        page_0()
    else:
        if err_mess != "":
            app.removeAllWidgets()
            err_page(problem=err_mess)


def eeg_infos():
    app.showSubWindow("infos")


def sub_eeg_infos(lsl):
    app.startSubWindow("infos", "Informations")
    app.addTextArea("eeg_infos")
    app.setTextArea("eeg_infos", lsl.print_infos())
    app.stopSubWindow()


def eeg_settings():
    app.showSubWindow("settings")


def sub_eeg_settings(lsl):
    app.startSubWindow("settings", "Settings")
    app.addLabel("lb1", "EEG Channels Setting")
    app.stopSubWindow()


def get_data(path=""):
    with open(os.path.abspath(path)) as op:
        data = json.load(op)
    return data


def select(lb, nome=""):
    shift_page(lb, port=app.getLabel("SelectedPort")[6:], nome=nome)


def port_selected():
    print("Porta: " + app.getOptionBox("Ports:"))
    app.setLabel("SelectedPort", "Porta: " + app.getOptionBox("Ports"))


def reload_ports():
    new_ser = ser.serial_ports()

    if new_ser.__len__()>0:
        app.changeOptionBox("Ports:", new_ser)


def start_teaching(lsl, name):
    global stop_teaching
    stop_teaching = False
    board_thread = threading.Thread(target=teach_nn(lsl, name))
    board_thread.daemon = True
    board_thread.start()


def timer(sec):
    t = threading.Timer(sec)
    t.start()
    t.join()


def init_arrow(text):
    ran_choice = random.choice(["right", "left"])
    direction = text.replace("_direction_", ran_choice)
    app.setTextArea("description", direction)
    get_arrow(ran_choice)
    return ran_choice


def show_progress_train(var=None):
    if var is None:
        temp = get_data("/virtenv/resources/mu_waves_descr.txt")
    else:
        temp = app.getTextArea("description") + "\n" + var
    app.setTextArea("description", temp)


def teach_nn(lsl, name):
    show_progress_train("Starting Signal acquisition ...")
    count = 0
    try:
        while stop_teaching is False:
            count += 1
            show_progress_train()
            arrow = init_arrow("Sample N° " + str(count) + "\n")
            show_progress_train("Adjusting ...")

            lsl.start_streaming()

            stream = resolve_stream("name", "openbci_eeg")
            inlet = StreamInlet(stream[0])

            data = []
            show_progress_train("Acquiring Data ...")
            with time.time() as t1:
                while (time.time() - t1) <= __signalAcquisitionTime__:
                    if (time.time() - t1).is_integer():
                        show_progress_train(str(time.time() - t1) + " ...")
                        data.append(inlet.pull_sample())
            lsl.stop_streaming()
            show_progress_train("Done!")
            finaldata = data[0:lsl.sample_rate*__signalAcquisitionTime__]
            show_progress_train("Saving current sample ...")
            nome_file = save_samples(finaldata, name, arrow)
    except:
        err_page("Error acquiring EEG data!")

    show_progress_train("Finishing Signal acquisition ...")
    stop_acq_data_teach_nn(lsl)
    train_nn(nome_file, lsl.sample_rate)


def save_samples(data, name, arrow):
    path_name = "virtenv/resources/"+name+"_data.json"

    if os.path.exists(os.path.abspath(path_name)):
        temp_dict = json.load(open(os.path.abspath(path_name)))
        temp = {}
        o = 0
        for x in temp_dict:  ##acquisizione
            count_temp = []
            for k in x:  ## arrow + dati
                count_temp.append(k)
            temp[str(o)] = count_temp
            o += 1
        count = len(temp) + 1
    else:
        temp_dict = {}
        count = 0

    temp_ch = []
    temp_glob = []

    temp_glob.append(arrow)

    for chan in data:
        temp_ch.append(chan)

    temp_glob.append(temp_ch)

    ttemp = []
    ttemp.append(temp_glob)

    temp_dict[str(count)] = ttemp

    with open(os.path.abspath(path_name), 'w') as op:
        json.dump(temp_dict, op, indent=4)

    return path_name


def get_samples(name):
    return get_data(name)


def wavelet_analysis(data, sample_rate):
    coef = []
    freq = []

    for sampl in data:
        part_coef=[]
        part_freq=[]

        for chan in sampl:
            scale = np.arange(1, 15)
            temp_coef, temp_freq = pywt.cwt(chan, scale, "morl", sample_rate)
            threshold = signal_to_noise_ratio(temp_coef)

            for j in temp_coef:
                for k in temp_coef[j]:
                    if temp_coef[j][k] < threshold:
                        temp_coef[j][k] = 0

            part_coef.append(temp_coef)
            part_freq.append(temp_freq)

        coef.append(part_coef)
        freq.append(part_freq)

    return coef, freq


def signal_to_noise_ratio(data):
    max_val = 0
    sum = 0
    count = 0
    for i in data:
        for j in data[i]:
            if max_val < data[i][j]:
                max_val = data[i][j]
            sum += data[i][j]
            count += 1
    return max_val/(sum/count)


def train_nn(path, arrow, sample_rate):
    show_progress_train("Passing through Wavelet Analisys ...")
    coef, freq = wavelet_analysis(get_data(path), sample_rate)
    show_progress_train("Done!")
    nn = neu_net.NeuralNetwork(coef, freq, arrow)

    return nn


def stop_acq_data_teach_nn(lsl):
    global stop_teaching
    stop_teaching = True
    lsl.cleanUp()


def start_nn():
    print("Start NN..\n")


def stop_nn():
    global stop_working
    stop_working = True


stop_teaching = False
stop_working = False
app = gui("Pagina Principale", "1000x550")
app.setResizable(False)
page_0()
app.go()
