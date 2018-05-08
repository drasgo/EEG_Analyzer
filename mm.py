



for port in serial_ports():
    with serial.Serial(port, 9600) as port_open:
        if port_open.is_open:
            print("Porta "+ port +" + aperta")


print(str(serial_ports())+" s")