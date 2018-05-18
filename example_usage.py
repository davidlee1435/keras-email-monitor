from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np

from monitor import EmailMonitor

data_dim = 16
timesteps = 8
num_classes = 10
batch_size = 32
train_mult = 1000

# Expected input batch shape: (batch_size, timesteps, data_dim)
# Note that we have to provide the full batch_input_shape since the network is stateful.
# the sample of index i in batch k is the follow-up for the sample i in batch k-1.
model = Sequential()
model.add(LSTM(32, return_sequences=True, stateful=True,
               batch_input_shape=(batch_size, timesteps, data_dim)))
model.add(LSTM(32, return_sequences=True, stateful=True))
model.add(LSTM(32, stateful=True))
model.add(Dense(10, activation='softmax'))


model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# Generate dummy training data
x_train = np.random.random((batch_size * train_mult, timesteps, data_dim))
y_train = np.random.random((batch_size * train_mult, num_classes))

# Generate dummy validation data
x_val = np.random.random((batch_size * 30, timesteps, data_dim))
y_val = np.random.random((batch_size * 30, num_classes))

email_callback = EmailMonitor("jl4397@columbia.edu")
model.fit(x_train, y_train,
          batch_size=batch_size, epochs=5, shuffle=False,
          validation_data=(x_val, y_val),
          callbacks=[email_callback])
