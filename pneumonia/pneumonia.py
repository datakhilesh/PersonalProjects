# -*- coding: utf-8 -*-
"""pneumonia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xXa0XdUbrHNdPZHWTyCZHXfOOXTXAv3I
"""

import warnings
warnings.filterwarnings('ignore')

from tensorflow import keras

from keras.layers import Input, Lambda, Dense, Flatten

from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt

!pip install kaggle

import os

# Replace 'your_username' and 'your_key' with your actual Kaggle username and key
os.environ['KAGGLE_USERNAME'] = 'dataatmarama'
os.environ['KAGGLE_KEY'] = 'a63b4f852ab19fad1b594e7bee4391e8'

# Download the dataset files
!kaggle datasets download -d paultimothymooney/chest-xray-pneumonia

# Unzip the downloaded files
!unzip chest-xray-pneumonia.zip

IMAGE_SIZE = [224, 224]

train_path = '/content/chest_xray/chest_xray/train'
valid_path = '/content/chest_xray/chest_xray/test'

vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

for layer in vgg.layers:
    layer.trainable = False

folders = glob('/content/chest_xray/chest_xray/train*')
x = Flatten()(vgg.output)

prediction = Dense(len(folders), activation='softmax')(x)
# create a model object
model = Model(inputs=vgg.input, outputs=prediction)
# view the structure of the model
model.summary()

model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)




# Make sure you provide the same target size as initialied for the image size
training_set = train_datagen.flow_from_directory('/content/chest_xray/chest_xray/train',
                                                 target_size = (224, 224),
                                                 batch_size = 10,
                                                 class_mode = 'categorical')




test_set = test_datagen.flow_from_directory('/content/chest_xray/chest_xray/test',
                                            target_size = (224, 224),
                                            batch_size = 10,
                                            class_mode = 'categorical')

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

import warnings
warnings.filterwarnings('ignore')

from tensorflow import keras
from keras.models import Model , load_model
from keras.applications.vgg16 import VGG16
from keras.layers import  Dense, Flatten
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import cv2

IMAGE_SIZE = [224, 224]

path_train = '/content/chest_xray/chest_xray/train'
path_validation = '/content/chest_xray/chest_xray/val'

vgg_model = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

for layer in vgg_model.layers:
    layer.trainable = False

folders = glob('/content/chest_xray/chest_xray/train/*')
x = Flatten()(vgg_model.output)

prediction = Dense(len(folders), activation='softmax')(x)
model = Model(inputs=vgg_model.input, outputs=prediction)
model.summary()

model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)





training_data = train_datagen.flow_from_directory('/content/chest_xray/chest_xray/train',
                                                 target_size = (224, 224),
                                                 batch_size = 10,
                                                 class_mode = 'categorical')




testing_data = test_datagen.flow_from_directory('/content/chest_xray/chest_xray/test',
                                            target_size = (224, 224),
                                            batch_size = 10,
                                            class_mode = 'categorical')

history = model.fit_generator(
  training_data,
  validation_data=testing_data,
  epochs=1,
  steps_per_epoch=len(training_data),
  validation_steps=len(testing_data),
)

model.save('chest_xray.h5')

model=load_model('chest_xray.h5')

img=image.load_img('/content/chest_xray/chest_xray/val/NORMAL/NORMAL2-IM-1431-0001.jpeg')
resized_img = cv2.resize(np.array(img), (224, 224))

i = image.img_to_array(resized_img)

i = np.expand_dims(i, axis=0)

img_data = preprocess_input(i)

classes = model.predict(img_data)

result=int(classes[0][0])

if result == 0:
    print("Person is Affected By PNEUMONIA")
else:
    print("Result is Normal")

