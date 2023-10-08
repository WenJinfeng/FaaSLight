import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy


class TensorFlowRegressionModel:
    
    def __init__(self, config, is_training=True):
        self.vars = self.set_vars()
        self.model = self.build_model(self.vars)
        if not is_training:
            self.sess = self.restore_model(config.get('model', 'LOCAL_MODEL_FOLDER'))
        return
    
    def set_vars(self):
        """
        Define the linear regression model through the variables
        """
        return {'X': tf.placeholder('float'), 'Y': tf.placeholder('float'), 'W': tf.Variable(numpy.random.randn(), name='weight'), 'b': tf.Variable(numpy.random.randn(), name='bias')}
    
    def build_model(self, vars):
        """
        Define the linear regression model through the variables
        """
        return tf.add(tf.multiply(vars['X'], vars['W']), vars['b'])
    
    def restore_model(self, model_dir):
        sess = tf.Session()
        saver = tf.train.Saver()
        ckpt = tf.train.get_checkpoint_state(model_dir)
        if (ckpt and ckpt.model_checkpoint_path):
            saver.restore(sess, ckpt.model_checkpoint_path)
        return sess
    
    def train(self, train_X, train_Y, learning_rate, training_epochs, model_output_dir=None):
        n_samples = train_X.shape[0]
        cost = tf.reduce_sum(tf.pow(self.model - self.vars['Y'], 2)) / (2 * n_samples)
        optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver = tf.train.Saver(tf.global_variables())
            for epoch in range(training_epochs):
                for (x, y) in zip(train_X, train_Y):
                    sess.run(optimizer, feed_dict={self.vars['X']: x, self.vars['Y']: y})
            saver.save(sess, model_output_dir + 'model.ckpt')
        return
    
    def predict(self, x_val):
        return self.sess.run(self.vars['W']) * x_val + self.sess.run(self.vars['b'])


