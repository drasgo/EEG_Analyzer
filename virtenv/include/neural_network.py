import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class NeuralNetwork(object):

    def __init__(self, arrow, user, coef, freq):
        self.coef = coef
        self.freq = freq
        self.arrow = arrow
        self.path_name = "NN/nn_" + user
        self.sess = tf.Session()

        self.data, self.dim_channels, self.dim_freq, self.dim_samples = self.prepare_data(coef, freq)
        self.labels = self.prepare_labels(arrow)

        print("In nn constructor")

        self.data_test = self.data[round(0.7 * len(self.data)):]
        self.labels_test = self.labels[round(0.7*len(self.data)):]

    def setup_nn(self):

        if os.path.isdir(os.path.abspath(self.path_name)) and os.path.isfile(os.path.isfile(self.path_name + "model.meta")):
            load_nn()
        else:
            print("In nn setup")
            hl1 = 500
            self.input = tf.placeholder(tf.float32, [None, self.dim_channels, self.dim_samples, self.dim_freq, 2], name="input")
            self.label = tf.placeholder(tf.int32, name="label")

            l1 = tf.layers.dense(inputs=self.input, units=hl1, activation=tf.nn.relu)

            self.output = tf.layers.dense(inputs=l1, units=1, activation=tf.nn.relu)

            self.loss = tf.losses.mean_squared_error(labels=self.label, predictions=self.output)

            self.train_opt = tf.train.GradientDescentOptimizer(learning_rate=0.5).minimize(self.loss)

            #self.correct_pred = tf.argmax(self.output, 1)

            self.accuracy = tf.reduce_mean(tf.cast(self.output, tf.int32))

            #self.loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=self.label, logits=self.output))

            #self.train_opt = tf.train.AdamOptimizer(0.01).minimize(self.loss)
            print("finished nn setup")


#from [acquisitions[channels[frequencies[values]]] = coef and [acquisitions[channels[values]]] = freq
#to [acquisitions[channels[values[freqencies[f0, x0/0][f1, x1/0]..]]]]
    def prepare_data(self, coef, freq):
        print("preparing data")
        acquisition_feed = []
        dim_channels = 0
        dim_samples = 0
        dim_freq = 0
        for i in range(len(coef)):#n acq--> 1 acq
            chan_feed = []
            single_acq_data = coef[i]
            single_acq_freq = freq[i]
            dim_channels = len(single_acq_data)
            for j in range(len(single_acq_data)):# m chan --> 1 chan
                camp_feed = []
                single_chan_data = single_acq_data[j]
                single_chan_freq = single_acq_freq[j]
                dim_freq = len(single_chan_data)

                for k in range(len(single_chan_data[0])):# dimension of number of periods
                    freq_feed = []

                    for (single_value_freq, single_freq_data) in zip(single_chan_freq, single_chan_data):
                        single_feed = []
                        single_feed.append(single_value_freq)
                        single_feed.append(single_freq_data[k])
                        freq_feed.append(single_feed)

                    camp_feed.append(freq_feed)
                    dim_freq = len(freq_feed)

                chan_feed.append(camp_feed)
                dim_samples = len(camp_feed)

            acquisition_feed.append(chan_feed)
            dim_channels = len(chan_feed)
            print("Acquisition "+str(i)+" ready! "+str(len(coef)-i)+" to go!")
        print("dim_channels: "+str(dim_channels)+", dim_freq: "+str(dim_freq)+", dim_samples: "+str(dim_samples))
        return acquisition_feed, dim_channels, dim_freq, dim_samples

# if "right"-->1, if "left"-->0
    def prepare_labels(self, arrow):
        print("preparing labels")
        prep_labels = []
        for acquisition in arrow:
            if acquisition == "right":
                prep_labels.append(1)
            else:
                prep_labels.append(0)

        return prep_labels

    def train(self, num_epochs, batch_size):
        while len(self.data) % batch_size != 0:
            batch_size += 1
        with tf.Session() as ses:
            ses.run(tf.global_variables_initializer())
            print("starting train")
            for epoch in range(num_epochs):
                epoch_total_loss = 0
                i = 0
                while i<len(self.data):
                    start = i
                    end = i + batch_size

                    batch_x = self.data[start:end]
                    batch_y = self.labels[start:end]
                    _, epoch_loss = ses.run([self.train_opt, self.loss], feed_dict={self.input: batch_x,
                                                                                     self.label: batch_y})
                    epoch_total_loss += epoch_loss
                    i += batch_size
                print("Epoch " + str(epoch) + " of " + str(num_epochs) + ". Loss " + str(epoch_total_loss))
            print("train over")

            predicted = ses.run([self.output], feed_dict={self.input: self.data_test})

            correct = 0
            for i in range(len(self.data_test)):
                a = predicted[i]
                b = self.labels_test[i]
                print("predicted: "+ str(a))
                print("expected: "+ str(b))
                if a == b:
                    correct += 1
            return correct/len(self.data_test)


    def load_nn(self):
        saver = tf.train.import_meta_graph(os.path.abspath(self.path_name + "model.meta"))
        saver.restore(self.sess, tf.train.latest_checkpoint("./"))

    def save_nn(self):
        saver = tf.train.Saver()
        saver.save(sess, self.path_name)
        print()

    def setup_run_nn(self):
        if os.path.isdir(os.path.abspath(self.path_name)) and os.path.isfile(os.path.isfile(self.path_name + "model.meta")):
            load_nn()
            return ""
        else:
            return "No preexisting trained Neural Network fir this user. Needs training first!"
