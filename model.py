# model.py
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

train_dir = "data/train"
test_dir = "data/test"
if not os.path.exists(train_dir) or not os.path.exists(test_dir):
    raise SystemExit("Put dataset folders in data/train and data/test (folders per class).")

train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=15, zoom_range=0.1, horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)

train_gen = train_datagen.flow_from_directory(train_dir, target_size=(48,48), color_mode='grayscale', batch_size=64, class_mode='categorical')
test_gen = test_datagen.flow_from_directory(test_dir, target_size=(48,48), color_mode='grayscale', batch_size=64, class_mode='categorical')

num_classes = train_gen.num_classes

model = Sequential([
    Conv2D(32, (3,3), activation='relu', padding='same', input_shape=(48,48,1)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu', padding='same'),
    MaxPooling2D(2,2),
    Conv2D(128, (3,3), activation='relu', padding='same'),
    MaxPooling2D(2,2),
    Dropout(0.25),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

model.compile(optimizer=Adam(0.0005), loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()
model.fit(train_gen, epochs=20, validation_data=test_gen)
model.save("model.h5")
print("Saved model.h5")
