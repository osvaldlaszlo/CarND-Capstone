import cv2
import numpy as np
import tensorflow as tf
from keras.models import model_from_yaml
import rospy

from styx_msgs.msg import TrafficLight


CLASSIFIER_MODEL_WEIGHTS_FILE = 'light_classification/classifier_model_a01_weights.h5'
CLASSIFIER_MODEL_YAML_FILE = 'light_classification/classifier_model_a01.yaml'


class TLClassifier(object):
    def __init__(self):
        # Loading YAML and creating model
        classifier_yaml_file = open(CLASSIFIER_MODEL_YAML_FILE, 'r')
        loaded_classifier_model_yaml = classifier_yaml_file.read()
        classifier_yaml_file.close()
        self.classifier_model = model_from_yaml(loaded_classifier_model_yaml)
        # Loading weights into the model
        self.classifier_model.load_weights(CLASSIFIER_MODEL_WEIGHTS_FILE)
        self.graph = tf.get_default_graph()


    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        pred = -1

        # Using the classifier to predict the state of the traffic light
        with self.graph.as_default():
            pred = np.argmax(self.classifier_model.predict(cv2.resize(image, (224,224)).reshape(1,224,224,3))[0])

        if pred == 0:
            return TrafficLight.GREEN
        if pred == 1:
            return TrafficLight.YELLOW
        return TrafficLight.RED
