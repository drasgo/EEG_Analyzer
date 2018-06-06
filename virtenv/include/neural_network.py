import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class NeuralNetwork(object):

    def __init__(self, user, coef=None, freq=None, arrow=None, train=True):

        print("In nn constructor")
        self.path_name = "NN/nn_" + user

        if train is True:
            self.data = self.prepare_data(coef, freq)
            self.labels = self.prepare_labels(arrow)
            self.data_test = self.data[round(0.7 * len(self.data)):]
            self.labels_test = self.labels[round(0.7*len(self.data)):]
        else:

            self.sess = tf.Session()
            new_saver = tf.train.import_meta_graph(os.path.abspath(self.path_name + "/model.meta"))
            new_saver.restore(self.sess, tf.train.latest_checkpoint(os.path.abspath(self.path_name)))

#from [acquisitions[channels[frequencies[values]]] = coef and [acquisitions[channels[values]]] = freq
#to [fo, x00, f1, x01, ...] ... one long ass vector!
    def prepare_data(self, coef, freq):
        print("preparing data")
        acquisition_feed = []

        for i in range(len(coef)):#n acq--> 1 acq
            chan_feed = []
            single_acq_data = coef[i]
            single_acq_freq = freq[i]

            for j in range(len(single_acq_data)):# m chan --> 1 chan
                single_chan_data = single_acq_data[j]
                single_chan_freq = single_acq_freq[j]

                for k in range(len(single_chan_data[0])):# dimension of number of periods

                    for (single_value_freq, single_freq_data) in zip(single_chan_freq, single_chan_data):
                        chan_feed.append(single_value_freq)
                        chan_feed.append(single_freq_data[k])

            acquisition_feed.append(chan_feed)
            print("Acquisition "+str(i)+" ready! "+str(len(coef)-i)+" to go!")
        return acquisition_feed

# if "right"-->[1,0], if "left"-->[0,1]
    def prepare_labels(self, arrow):
        print("preparing labels")
        prep_labels = []
        for acquisition in arrow:
            if acquisition == "right":
                prep_labels.append([1, 0])
            else:
                prep_labels.append([0, 1])
        return prep_labels

    def train(self, num_epochs, batch_size):

        prediction = self.setup_nn()

        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=prediction, labels=self.label))
        optimizer = tf.train.AdamOptimizer().minimize(cost)

        while len(self.data) % batch_size != 0:#batch_size of correct size to cut without problems input data
            batch_size += 1

        with tf.Session() as ses:
            ses.run(tf.global_variables_initializer())
            print("starting train")

            for epoch in range(num_epochs):#divide the input data in len(self.data)/batch_size different input
                epoch_total_loss = 0
                i = 0

                while i < len(self.data):
                    start = i
                    end = i + batch_size

                    batch_x = self.data[start:end]
                    batch_y = self.labels[start:end]
                    _, epoch_loss = ses.run([optimizer, cost], feed_dict={self.input: batch_x,
                                                                                     self.label: batch_y})
                    epoch_total_loss += epoch_loss
                    i += batch_size

                print("Epoch " + str(epoch) + " of " + str(num_epochs) + ". Loss " + str(epoch_total_loss))
            writer = tf.summary.FileWriter(os.path.abspath("NN"), ses.graph)
            writer.close()
            print("train over")
            correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(self.label, 1))
            accuracy = tf.reduce_mean(tf.cast(correct, "float"))
            res = accuracy.eval({self.input: self.data_test, self.label: self.labels_test})

            self.create_file()

            saver = tf.train.Saver()
            saver.save(ses, os.path.abspath(self.path_name+"/model"))

        return res

    def setup_nn(self):
        print("In nn setup")
        ### NN structure
        hl1 = 500
        hl2 = 500
        oL = 2

        self.input = tf.placeholder('float', [None, len(self.data[0])], name="input")
        self.label = tf.placeholder('float', name="label")

        print("Data dimension: "+str(len(self.data[0])))

        hidden_l_1 = {'weights': tf.Variable(tf.random_normal([len(self.data[0]), hl1])),
                      'biases': tf.Variable(tf.random_normal([hl1]))}

        hidden_l_2 = {'weights': tf.Variable(tf.random_normal([hl1, hl2])),
                      'biases': tf.Variable(tf.random_normal([hl2]))}

        output_l = {'weights': tf.Variable(tf.random_normal([hl2, oL])),
                    'biases': tf.Variable(tf.random_normal([oL]))}

        l1 = tf.add(tf.matmul(self.input, hidden_l_1['weights']), hidden_l_1['biases'])
        l1 = tf.nn.relu(l1)

        l2 = tf.add(tf.matmul(l1, hidden_l_2['weights']), hidden_l_2['biases'])
        l2 = tf.nn.relu(l2)

        output_l = tf.add(tf.matmul(l2, output_l['weights']), output_l['biases'], name='output')
        ###
        print("finished nn setup")

        return output_l

    def create_file(self):
        if self.check_existing_nn() is False:
            os.makedirs(self.path_name)

    def check_existing_nn(self):
        if os.path.isdir(os.path.abspath(self.path_name)):
            return True
        else:
            return False

    def get_result(self, output):
        if output[0] > output[1]:
            return "right"
        else:
            return "left"

    def run(self, coef, freq):
        data = self.prepare_data(coef, freq)
        new_input = tf.get_default_graph().get_tensor_by_name('input:0')
        new_output = tf.get_default_graph().get_tensor_by_name('output:0')
        output = [0, 1]
        i = 0
        while i < len(data):
            start = i
            end = i+1
            batch_x = data[start:end]
            output = self.sess.run(new_output, feed_dict={new_input: batch_x})[0]
            i += 1
        return self.get_result(output)
