# all taken from https://www.tensorflow.org/guide/keras/functional
from pathlib import Path

import hydra
from omegaconf import OmegaConf
import wandb
from wandb.keras import WandbCallback


@hydra.main(config_path='../conf', config_name='config')
def train_dense_model_main(cfg):
    return train_dense_model(cfg)


def my_model(input_shape=784, output_num=10, activation='relu', hidden_size=64):
    inputs = keras.Input(shape=input_shape)
    x = layers.Dense(hidden_size, activation=activation)(inputs)
    x = layers.Dense(hidden_size, activation=activation)(x)
    outputs = layers.Dense(output_num)(x)
    return keras.Model(inputs=inputs, outputs=outputs, name='mnist_model')

def model_compile(model, loss='xent', optimizer='rmsprop'):
    if loss == 'xent':
        loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(loss=loss,
                  optimizer=optimizer,
                  metrics=['accuracy'])

def data(n_train=60_000, n_test=10_000, n_features=784, n_classes=10):
    # training and inference
    # network is not reachable, so we use random data
    x_train = tf.random.normal((n_train, n_features), dtype='float32')
    x_test = tf.random.normal((n_test, n_features), dtype='float32')
    y_train = tf.random.uniform((n_train,), minval=0, maxval=n_classes, dtype='int32')
    y_test = tf.random.uniform((n_test,), minval=0, maxval=n_classes, dtype='int32')
    return x_train, x_test, y_train, y_test


def train_dense_model(cfg):
    # limit imports oustide the call to the function, in order to launch quickly
    # when using dask
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers

    # wandb setup
    Path(cfg.wandb.dir).mkdir(exist_ok=True, parents=True)
    wandb.init(
        config=OmegaConf.to_container(cfg, resolve=True),
        **cfg.wandb,
    )
    callbacks = [
        WandbCallback(monitor='loss', save_weights_only=True),
    ]

    # model building
    tf.keras.backend.clear_session()
    model = my_model(**cfg.model)
    model_compile(model, **cfg.compile)
    x_train, x_test, y_train, y_test = data(**cfg.data)
    history = model.fit(x_train, y_train, **cfg.fit, callbacks=callbacks)
    test_scores = model.evaluate(x_test, y_test, verbose=2)
    print('Test loss:', test_scores[0])
    print('Test accuracy:', test_scores[1])
    return True

if __name__ == '__main__':
    train_dense_model_main()
