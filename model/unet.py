import keras
from cfg import *

def conv(input,features,kernel_size=3,strides = 1,padding='same',is_relu=True,is_bn=True):
  x = keras.layers.Conv2D(features,kernel_size,strides,padding,kernel_initializer='he_normal')(input)
  if is_bn:
    x = keras.layers.BatchNormalization()(x)

  if is_relu:
    x = keras.activations.relu(x)

  return x

def unet(n_levels, initial_features=32, n_blocks=2, kernel_size=3, pooling_size=2, in_channels=3, out_channels=num_classes):
  inputs = keras.layers.Input(shape=(IMAGE_HEIGHT, IMAGE_WIDTH, in_channels))
  x = inputs
  
  #인코더부분
  skips = []
  for level in range(n_levels):
    if level != 0 :
      x = keras.layers.MaxPool2D(pooling_size)(x)
    for _ in range(n_blocks):
      x = conv(x,initial_features * 2 ** level,kernel_size,1,'same')
    skips.append(x)

  # 디코더 부분
  for level in reversed(range(n_levels-1)):
    x = keras.layers.UpSampling2D(pooling_size, interpolation='bilinear')(x) 
    x = conv(x,initial_features * 2 ** level,2,1,'same')

    x = keras.layers.Concatenate()([x, skips[level]])
    for _ in range(n_blocks):
      x = conv(x,initial_features * 2 ** level,kernel_size,1,'same')
          
  # 결과
  x = keras.layers.Conv2D(out_channels, kernel_size=1, padding='same')(x)

  if out_channels == 1:
    x = keras.activations.sigmoid(x)
  else:
    x = keras.activations.softmax(x)
  
  return keras.Model(inputs=[inputs], outputs=x, name=f'UNET-L{n_levels}-F{initial_features}')
