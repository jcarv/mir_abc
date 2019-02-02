import tensorflow as tf
from Helpers import abc_helper

hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()

print(sess.run(hello))

print(abc_helper.my_function())