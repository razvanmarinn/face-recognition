from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models


class EmotionModel:
    def __init__(self, input_shape=(48, 48, 3), num_classes=7):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.emotion_model = self.build_model()

    def build_model(self):
        model = models.Sequential()

        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))

        model.add(layers.Flatten())

        model.add(layers.Dense(512, activation='relu'))
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(self.num_classes, activation='softmax'))

        return model

    def train(self, train_generator, validation_generator, epochs=50, initial_epoch=0, model_weights_path=None):
        optimizer = 'adam'
        self.emotion_model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

        if model_weights_path:
            self.emotion_model.load_weights(model_weights_path)

        early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)

        model_checkpoint = ModelCheckpoint('best_emotion_model.h5', monitor='val_accuracy', mode='max',
                                           save_best_only=True)

        emotion_model_info = self.emotion_model.fit(
            train_generator,
            epochs=epochs,
            initial_epoch=initial_epoch,
            validation_data=validation_generator,
            callbacks=[early_stopping, reduce_lr, model_checkpoint])

        return emotion_model_info

    def save(self, model_weights_path='emotion_model.h5'):
        print("Saving model weights to disk")
        self.emotion_model.save_weights(model_weights_path)


train_dir = './train_img'
test_dir = './test_img'
image_size = (48, 48)
batch_size = 32

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical'
)

validation_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical'
)

emotion_model = EmotionModel(input_shape=image_size + (3,), num_classes=7)
emotion_model.train(train_generator, validation_generator, epochs=100, initial_epoch=80,
                    model_weights_path='custom_emotion_model4.h5')
emotion_model.save("custom_emotion_model5.h5")
