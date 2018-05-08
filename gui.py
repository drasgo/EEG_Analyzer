from appJar import gui

class GUI():
    
    def __init__(self):
        self.app = gui("EEG - Brain Waves Actuator", "500x700")
        self.app.setResizable(False)
        self.initial_page()
        
    def initial_page(self):
        self.app.removeAllWidgets()

        label1 = "description 1\n\n\n\n"
        label2 = "description 2\n\n\n\n"
        label3 = "description 3\n\n\n\n"

        self.app.addLabel("Port", "Selecting Ports")

        self.app.addLabelOptionBox("Ports:", ["Standard"] + port)
        self.app.setOptionBoxChangeFunction("Ports:", port_selected)

        self.app.addButton("reloadPorts", reload_ports)

        self.app.addLabel("SelectedPort", "Port: #")

        self.app.addVerticalSeparator(0, 2, rowspan=5)

        self.app.addButton("Type1", select, 0, 3)
        self.app.addLabel("descr1", label1, 1, 3)

        self.app.addVerticalSeparator(0, 4, rowspan=5)

        self.app.addButton("Type2", select, 0, 5)
        self.app.addLabel("descr2", label2, 1, 5)

        self.app.addVerticalSeparator(0, 6, rowspan=5)

        self.app.addButton("Type3", select, 0, 7)
        self.app.addLabel("descr3", label3, 1, 7)

        self.app.setLabelRelief("descr1", self.app.SUNKEN)
        self.app.setLabelRelief("descr2", self.app.SUNKEN)
        self.app.setLabelRelief("descr3", self.app.SUNKEN)
    
    def select(self, button):
        if button is self.app.getButton("Type2"):
            print()
        
        