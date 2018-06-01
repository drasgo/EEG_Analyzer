import tensorflow as tf
import os


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
            self.input = tf.placeholder(tf.float32, [None, self.dim_channels, self.dim_freq, self.dim_samples, 2], name="input")
            self.label = tf.placeholder(tf.float32, name="label")

            l1 = tf.layers.dense(input, hl1, tf.nn.relu)

            self.output = tf.layers.dense(l1, 1)

            self.loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=label, logits=output))

            self.train_opt = tf.train.AdamOptimizer(0.01).minimize(loss)
            print("finished nn setup")


#from [acquisitions[channels[frequencies[values]]] = coef and [acquisitions[channels[values]]] = freq
#to [acquisitions[channels[values[freqencies[f0, x0/0][f1, x1/0]..]]]]
    def prepare_data(self, coef, freq):
        print("preparing data")
        acquisition_feed = []
        dim_channels = 0
        dim_samples = 0
        dim_freq = 0
        for i in range(len(coef)):
            single_acq_data = coef[i]
            single_acq_freq = freq[i]
            dim_channels = len(single_acq_data)
            for j in range(len(single_acq_data)):
                chan_feed = []
                single_chan_data = single_acq_data[j]
                single_chan_freq = single_acq_freq[j]
                dim_freq = len(single_chan_data)
                for single_freq_data in single_chan_data:
                    camp_feed = []
                    dim_samples = len(single_freq_data)
                    for single_value_data in single_freq_data:
                        freq_feed = []
                        for single_value_freq in single_chan_freq:
                            print("in single feed")
                            single_feed = []
                            single_feed.append(single_value_freq)
                            single_feed.append(single_value_data)
                            freq_feed.append(single_feed)
                        print("in camp feed")
                        camp_feed.append(freq_feed)
                    print("in chan feed")
                    chan_feed.append(camp_feed)
                print("in acquisition feed")
                acquisition_feed.append(chan_feed)

        return data, dim_channels, dim_freq, dim_samples

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

    def train(self, num_epochs):
        self.sess.run(tf.initialize_all_variables())
        print("starting train")
        for acquisition_train, label_train in zip(self.data, self.labels):
            for epoch in range(num_epochs):
                epoch_total_loss = 0
                _, epoch_loss = sess.run([self.train_opt, self.loss], feed_dict={self.input: acquisition_train,
                                                                                 self.label: label_train})
                epoch_total_loss += epoch_loss

                print("Epoch " + epoch + " of " + num_epochs + ". Loss " + epoch_total_loss)
        print("train over")
        correct = tf.equal(tf.argmax(self.output, 1), tf.argmax(self.label, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
        return accuracy.eval({self.input:self.data_test, self.label: self.labels_test})


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
