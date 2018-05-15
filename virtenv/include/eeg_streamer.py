import threading
from collections import OrderedDict
import virtenv.include.open_bci_v3 as bci
from pylsl import StreamInfo, StreamOutlet
import sys
import random
import atexit

class Eeg_Streamer():

    def __init__(self, port=None):
        self.default_settings = OrderedDict()
        self.current_settings = OrderedDict()
        if port is None:
            self.initialize_board(autodetect=True)
        else:
            self.initialize_board(port=port)
        self.init_board_settings()

    def initialize_board(self, autodetect=True, port=None):
        print("Initializing board\n")

        if autodetect and port is None:
            self.board = bci.OpenBCIBoard()
        else:
            self.board = bci.OpenBCIBoard(port=port)

        self.eeg_channels = self.board.getNbEEGChannels()
        self.aux_channels = self.board.getNbAUXChannels()
        self.sample_rate = self.board.getSampleRate()

    def init_board_settings(self):
        self.default_settings["Number_Channels"] = [b'C']
        for i in range(16):
            current = "channel{}".format(i + 1)
            self.default_settings[current] = []
            self.default_settings[current].append(b'x')
            self.default_settings[current].append(str(i + 1).encode())
            self.default_settings[current].append(b'0')
            self.default_settings[current].append(b'6')
            self.default_settings[current].append(b'0')
            self.default_settings[current].append(b'1')
            self.default_settings[current].append(b'1')
            self.default_settings[current].append(b'0')
            self.default_settings[current].append(b'X')
        self.default_settings["SD_Card"] = b" "
        self.current_settings = self.default_settings.copy()

    def set_board_settings(self):
      for item in self.current_settings:
        if self.current_settings[item] != self.default_settings[item]:
          for byte in self.current_settings[item]:
            self.board.ser.write(byte)

    #Qui succede la magia: questa è una funzione di callback! Questo significa che
    # quando si va a creare il thread di start_streaming, gli si da questa funzione
    # da chiamare nel caso succeda qualcosa (si hanno nuovi dati). Questi nuovi
    # dati sono salvati nei qui presenti outlet_eeg e outlet_aux
    def send(self, sample):
        try:
            self.outlet_eeg.push_sample(sample.channel_data)
            self.outlet_aux.push_sample(sample.aux_data)
        except:
            print("LSL Settings Error!\n")

    def create_lsl(self, ):
        random_id = random.randint(0,255)
        # default parameters
        eeg_name = 'openbci_eeg'
        eeg_type = 'EEG'
        eeg_chan = self.eeg_channels
        eeg_hz = self.sample_rate
        eeg_data = 'float32'
        eeg_id = 'openbci_eeg_id' + str(random_id)
        aux_name = 'openbci_aux'
        aux_type = 'AUX'
        aux_chan = self.aux_channels
        aux_hz = self.sample_rate
        aux_data = 'float32'
        aux_id = 'openbci_aux_id' + str(random_id)
        #create StreamInfo
        self.info_eeg = StreamInfo(eeg_name,eeg_type,eeg_chan,eeg_hz,eeg_data,eeg_id)
        self.info_aux = StreamInfo(aux_name,aux_type,aux_chan,aux_hz,aux_data,aux_id)

        chns = self.info_eeg.desc().append_child('channels')
        if self.eeg_channels == 16:
            labels = ['Fp1', 'Fp2', 'C3', 'C4', 'T5', 'T6', 'O1', 'O2', 'F7', 'F8', 'F3', 'F4', 'T3', 'T4', 'P3', 'P4']
        else:
            labels = ['Fp1', 'Fp2', 'C3', 'C4', 'T5', 'T6', 'O1', 'O2']
        for label in labels:
            ch = chns.append_child("channel")
            ch.append_child_value('label', label)
            ch.append_child_value('unit', 'microvolts')
            ch.append_child_value('type', 'EEG')

        # additional Meta Data
        self.info_eeg.desc().append_child_value('manufacturer', 'OpenBCI Inc.')
        self.info_aux.desc().append_child_value('manufacturer', 'OpenBCI Inc.')

        # create StreamOutlet
        self.outlet_eeg = StreamOutlet(self.info_eeg)
        self.outlet_aux = StreamOutlet(self.info_aux)

    def print_infos(self):
        temp="LSL Configuration: \n" + \
            "  Stream 1: \n" + \
            "      Name: " + self.eeg_name + " \n" + \
            "      Type: " + self.eeg_type + " \n" + \
            "      Channel Count: " + str(self.eeg_chan) + "\n" + \
            "      Sampling Rate: " + str(self.eeg_hz) + "\n" + \
            "      Channel Format: "+ self.eeg_data + " \n" + \
            "      Source Id: " + self.eeg_id + " \n" + \
            "  Stream 2: \n" + \
            "      Name: " + self.aux_name + " \n" + \
            "      Type: "+ self.aux_type + " \n" + \
            "      Channel Count: " + str(self.aux_chan) + "\n" + \
            "      Sampling Rate: " + str(self.aux_hz) + "\n" + \
            "      Channel Format: " + self.aux_data +" \n" + \
            "      Source Id: " + self.aux_id + " \n\n" + \
            "Electrode Location Montage:\n" + \
            str(self.labels)
        return temp

    def cleanUp(self):
        self.board.disconnect()
        print ("Disconnecting...")
        atexit.register(self.cleanUp)

    def start_streaming(self):
        boardThread = threading.Thread(target=self.board.start_streaming, args=(self.send, -1))
        boardThread.daemon = True  # will stop on exit
        boardThread.start()
        print("Current streaming: {} EEG channels and {} AUX channels at {} Hz\n".format(self.eeg_channels,
                                                                                         self.aux_channels,
                                                                                         self.sample_rate))
    def stop_streaming(self):
        self.board.stop()
        while self.board.ser.inWaiting():
            # print("doing this thing")
            c = self.board.ser.read().decode('utf-8', errors='replace')
            line += c
            if (c == '\n'):
                line = ''
        print("Streaming paused.\n")
