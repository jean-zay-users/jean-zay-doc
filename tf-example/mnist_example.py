# all taken from https://www.tensorflow.org/guide/keras/functional
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# model building
tf.keras.backend.clear_session()  # For easy reset of notebook state.

inputs = keras.Input(shape=(784,), name='img')
x = layers.Dense(64, activation='relu')(inputs)
x = layers.Dense(64, activation='relu')(x)
outputs = layers.Dense(10)(x)

model = keras.Model(inputs=inputs, outputs=outputs, name='mnist_model')

# training and inference
# network is not reachable, so we use random data
x_train = tf.random.normal((60000, 784), dtype='float32')
x_test = tf.random.normal((10000, 784), dtype='float32')
y_train = tf.random.uniform((60000,), minval=0, maxval=10, dtype='int32')
y_test = tf.random.uniform((10000,), minval=0, maxval=10, dtype='int32')


model.compile(loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              optimizer=keras.optimizers.RMSprop(),
              metrics=['accuracy'])
history = model.fit(x_train, y_train,
                    batch_size=64,
                    epochs=5,
                    validation_split=0.2)
test_scores = model.evaluate(x_test, y_test, verbose=2)
print('Test loss:', test_scores[0])
print('Test accuracy:', test_scores[1])

# saving
model.save(os.environ['SCRATCH'])
