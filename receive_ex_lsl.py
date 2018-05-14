import threading
from pylsl import StreamInfo, StreamOutlet, StreamInlet, resolve_stream
import example_lsl as ex
import time
def receive():
    print("looking for an EEG stream...")
    streams = resolve_stream("type ", "EEG")

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample = inlet.pull_sample()
        print( str(sample) +" c \n")


th1=threading.Thread(target=ex.send, args=())
th1.start()
time.sleep(0.01)
receive()