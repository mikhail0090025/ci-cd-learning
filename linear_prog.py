import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split
import os
import numpy as np

model_path = 'best_model.h5'
if os.path.exists(model_path):
    print(f"Найдена сохранённая модель: {model_path}. Загружаем...")
    model = tf.keras.models.load_model(model_path)
    print("Модель загружена!")
else:
    print("Сохранённая модель не найдена. Создаём новую...")
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(2, activation='linear'),
        tf.keras.layers.Dense(20, activation='elu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(20, activation='elu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(1, activation='linear'),
    ])

checkpoint = ModelCheckpoint(
    'best_model.h5',
    monitor='val_loss',
    save_best_only=True,
    mode='min',
    verbose=1
)

# Компилируем модель
model.compile(
    optimizer='adam',  # Оптимизатор Adam (хорошо подходит для CNN)
    loss='mean_squared_error',  # Функция потерь для бинарной классификации
    metrics=['mae']  # Отслеживаем метрику accuracy
)
inputs = []
outputs = []
for num in range(-20, 21):
    for step in range(-15, 16):
        inputs.append([num, num + step])
        outputs.append([num + step + step])
inputs = np.array(inputs, dtype=float)
outputs = np.array(outputs, dtype=float)
train_inputs, train_outputs, test_inputs, test_outputs = train_test_split(inputs, outputs, test_size=0.05, random_state=52)
# Обучаем модель
history = model.fit(
    x=inputs,
    y=outputs,
    batch_size=32,
    epochs=300,
    verbose=1,
    validation_data=None,
    validation_split=0.2,
    callbacks=None,
    shuffle=True,
)

# Создаём ось x для графика (номера эпох)
epochs = range(1, len(history.history['val_loss']) + 1)  # [1, 2, ..., 30]

# Рисуем график
plt.plot(epochs, history.history['val_loss'], label='Validation Loss', color='red')
plt.plot(epochs, history.history['loss'], label='Train Loss', color='green')
plt.plot(epochs, history.history['mae'], label='MAE', color='blue')
plt.xlabel('Epoch')  # Подпись оси x
plt.ylabel('Validation Loss')  # Подпись оси y
plt.title('Train and Validation Losses')  # Заголовок графика
plt.legend()  # Показываем легенду (чтобы различать линии)
plt.grid(True)  # Добавляем сетку для наглядности
plt.show()  # Показываем график

print("\n=== Интерактивный тест модели ===")
while True:
    try:
        num = float(input("Введите число num (-20 до 20): "))
        if num < -20 or num > 20:
            print("Число должно быть от -20 до 20!")
            continue
        step = float(input("Введите шаг step (-15 до 15): "))
        if step < -15 or step > 15:
            print("Шаг должен быть от -15 до 15!")
            continue
        
        # Формируем входные данные
        input_data = np.array([[num, num + step]], dtype=float)
        # Предсказание
        prediction = model.predict(input_data)
        expected = num + step + step
        print(f"Вход: [{num}, {num + step}]")
        print(f"Предсказание: {prediction[0][0]:.2f}")
        print(f"Ожидаемое значение: {expected:.2f}")
        
        # Спрашиваем, продолжать ли
        again = input("Хотите попробовать ещё? (да/нет): ").lower()
        if again != 'да':
            print("Тест завершен!")
            break
    except ValueError:
        print("Введите корректное число!")