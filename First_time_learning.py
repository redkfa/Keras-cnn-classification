#KERAS
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD,RMSprop,adam
from keras.utils import np_utils
from keras import backend as K

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from PIL import Image
from numpy import *
# SKLEARN
from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split


img_dim_ordering = 'tf'
K.set_image_dim_ordering(img_dim_ordering)


# 設定輸入影像參數

#長寬
img_height, img_width = 256, 256

# 色彩通道
img_channels = 3
# fix random seed for reproducibility
seed=7
np.random.seed(seed)
#%%
#  data

path1 = os.getcwd() + '\\process\\input_data'    #原始影像位置    
path2 = os.getcwd() + '\\process\\input_data_resized'  #前處理後影像位置   

listing = os.listdir(path1) 
num_samples=size(listing)
print('sample number=', num_samples)

for file in listing:
    im = Image.open(path1 + '\\' + file)   
    img = im.resize((img_height,img_width))
    gray = img.convert('L')
                #need to do some more processing here      
                
    gray.save(path2 +'\\' +  file, "JPEG")

imlist = os.listdir(path2) #set of all image file names

im1 = array(Image.open(path2 + '\\'+ imlist[0])) # open one image to get size
m,n = im1.shape[0:2] # get the size of the images, shape=array dimension
imnbr = len(imlist) # get the number of images

# create matrix to store all flattened images (one row per image)
immatrix = array([array(Image.open(path2+ '\\' + im2)).flatten()
              for im2 in imlist],'f') #flatten every image in imlist
    
    
#為影像貼上標籤                
label=np.ones((num_samples,),dtype = int)
label[0:1739]=0
label[1739:2718]=1
label[2718:4016]=2
label[4016:5553]=3
label[5553:6113]=4
label[6113:7603]=5
label[7603:]=6

data,Label = shuffle(immatrix,label, random_state=2)#
train_data = [data,Label] #train_data[0]=image, train_data[1]=label

#img=immatrix[167].reshape(img_rows,img_cols) #為了show image再將1-D轉為2-D
#plt.imshow(img)
#plt.imshow(img,cmap='gray')
print ('train_data[0].shape=',train_data[0].shape)
print ('train_data[1].shape=',train_data[1].shape)
print ('train_data[2].shape=',train_data[2].shape)
print ('train_data[3].shape=',train_data[3].shape)
print ('train_data[4].shape=',train_data[4].shape)
print ('train_data[5].shape=',train_data[5].shape)
print ('train_data[6].shape=',train_data[6].shape)

#%%
#設定 神經網路 相關參數
#batch_size to train
batch_size = 20
# number of output classes
nb_classes = 7
# number of epochs to train
nb_epoch = 2


# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling
nb_pool = 2
# convolution kernel size
nb_conv = 3

#%%
#將影像與標籤設定為X_train, X_test, y_train, y_test

(X, y) = (train_data[0],train_data[1])

# STEP 1: split X and y into training and testing sets

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)


X_train = X_train.reshape(X_train.shape[0], 1, img_height, img_width)
X_test = X_test.reshape(X_test.shape[0], 1, img_height, img_width)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

X_train /= 255
X_test /= 255

print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

#i = 100
#plt.imshow(X_train[i, 0], interpolation='nearest')
#print("label : ", Y_train[i,:])

#%%
#建立自訂義模型
model = Sequential()

model.add(Convolution2D(nb_filters, nb_conv, nb_conv,
                        border_mode='valid',
                        dim_ordering='th',
                        input_shape=(1, img_height, img_width)))
convout1 = Activation('relu')
model.add(convout1)
model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
convout2 = Activation('relu')
model.add(convout2)
model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
model.add(Dropout(0.3))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.3))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

#%%
#開始訓練
hist = model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
                 verbose=1, validation_data=(X_test, Y_test))
'''            
#另一種設定驗證資料的方式將validation_data=(X_test, Y_test)改為validation_split=0.2 
hist = model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
                 verbose=1, validation_split=0.2)
'''


#將訓練視覺化，以設定loss與accuracy為例
train_loss=hist.history['loss']
val_loss=hist.history['val_loss']
train_acc=hist.history['acc']
val_acc=hist.history['val_acc']
xc=range(nb_epoch)

plt.figure(1,figsize=(7,5))
plt.plot(xc,train_loss)
plt.plot(xc,val_loss)
plt.xlabel('num of Epochs')
plt.ylabel('loss')
plt.title('train_loss vs val_loss')
plt.grid(True)
plt.legend(['train','val'])
print(plt.style.available) # use bmh, classic,ggplot for big pictures
plt.style.use(['classic'])

plt.figure(2,figsize=(7,5))
plt.plot(xc,train_acc)
plt.plot(xc,val_acc)
plt.xlabel('num of Epochs')
plt.ylabel('accuracy')
plt.title('train_acc vs val_acc')
plt.grid(True)
plt.legend(['train','val'],loc=4)
#print plt.style.available # use bmh, classic,ggplot for big pictures
plt.style.use(['classic'])




#%%       
#評估模型
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])
print(model.predict_classes(X_test[1:5]))
print(Y_test[1:5])



#%%
#可視化中間影隱藏層
#output_layer = model.layers[1].output
output_fn = K.function([model.layers[0].input], [model.layers[1].output])
# the input image
input_image=X_train[0:1,:,:,:]
print(input_image.shape)

#plt.imshow(input_image[0,0,:,:],cmap ='gray')
#plt.imshow(input_image[0,0,:,:])

output_image = output_fn([input_image])
print(output_image[0].shape)
# Rearrange dimension so we can plot the result 
output_image = np.rollaxis(np.rollaxis(output_image[0], 3, 1), 3, 1)
print(output_image.shape)
fig=plt.figure(figsize=(8,8))
for i in range(32):
    ax = fig.add_subplot(6, 6, i+1)
    #ax.imshow(output_image[0,:,:,i],interpolation='nearest' ) #to see the first filter
    ax.imshow(output_image[0,:,:,i],cmap=matplotlib.cm.gray)
    plt.xticks(np.array([]))
    plt.yticks(np.array([]))
    plt.tight_layout()
plt


from sklearn.metrics import classification_report,confusion_matrix

#進行預測並製作混淆矩陣


Y_pred = model.predict(X_test)
print("Y_pred:",Y_pred)
y_pred = np.argmax(Y_pred, axis=1)
print("Y_pred:",y_pred)
''' 
                       # (or)

y_pred = model.predict_classes(X_test)
print("Y_pred:",y_pred)
'''
p=model.predict_proba(X_test) # to predict probability

target_names = ['class 0(Flowers)', 'class 1(Dogs)' ]
print(classification_report(np.argmax(Y_test,axis=1), y_pred,target_names=target_names))
print(confusion_matrix(np.argmax(Y_test,axis=1), y_pred))

# 儲存模型

fname = "weights-Test-CNN.hdf5"
model.save_model(fname,overwrite=True)

