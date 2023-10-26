import cv2
import mediapipe as mp  # Для распознования рук
import serial  # для отправки на COM порт

camera = cv2.VideoCapture(0)

mpHands = mp.solutions.hands  # Подключение алгоритмов поиска рук
hands = mpHands.Hands()     #  обьект "руки" с настройками
mpDraw = mp.solutions.drawing_utils  # утилиты для рисования

port = "COM13"
uart = serial.Serial(port, 9600)

p = [0 for i in range(21)]  # создаем массив из 21 ячейки для хранения высоты каждой точки
finger = [0 for i in range(5)]  # создаем массив из 5 ячеек для хранения положения каждого пальца


def distance(point_1, point_2):
    """# функция, возвращающая расстояние по модулю (без знака)"""
    return abs(point_1 - point_2)


while True:
    # считываем видео по одной картинке
    good, img = camera.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # преобразуем кадр в RGB

    results = hands.process(imgRGB)  # Поиск рук в кадре
    if results.multi_hand_landmarks:  # получает ли точки на руке
        for handLms in results.multi_hand_landmarks:  # получаем координаты каждой точки

            # проводим линии между точками
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # работаем с каждой точкой по отдельности
            # создаем список от 0 до 21 с координатами точек
            for id, point in enumerate(handLms.landmark):
                # получаем размеры изображения с камеры и масштабируем
                width, height, color = img.shape
                width, height = int(point.x * height), int(point.y * width)
                p[id] = height  # заполняем массив высотой каждой точки

                # выбираем нужную точку
                if id == 8:
                    cv2.circle(img, (width, height), 7, (255, 250, 255), cv2.FILLED)  # Рисует окружность на пальце
                if id == 12:
                    cv2.circle(img, (width, height), 7, (0, 0, 255), cv2.FILLED)
                if id == 0:
                    cv2.circle(img, (width, height), 7, (0, 0, 255), cv2.FILLED)
                # получаем расстояние, с которым будем сравнивать каждый палец
                distanceGood = distance(p[0], p[5]) + (distance(p[0], p[5] / 2))
               # print(distanceGood, distance(p[0], p[8]))

                # заполняем массив 1 (палец поднят) или 0 (палец сжат)
                finger[1] = 1 if distance(p[0], p[8]) > distanceGood / 3 else 0
                finger[2] = 1 if distance(p[0], p[12]) > distanceGood / 3 else 0
                finger[3] = 1 if distance(p[0], p[16]) > distanceGood / 3 else 0
                finger[4] = 1 if distance(p[0], p[20]) > distanceGood / 3 else 0
                finger[0] = 1 if distance(p[4], p[17]) > distanceGood / 3 else 0

                msg = '0'
                # 0 - большой палец, 1 - указательный, 2 - средний, 3 - безымянный, 4 - мизинец
                # жест "коза" - 01001

                # Указательный

                if not finger[1] and not finger[2] and not finger[3] and not finger[4] and not finger[0]:
                     msg = '0'
                else:

                        # print('Green High')
                        # msg = bytes(str(msg), 'utf-8')
                        # uart.write(msg)

                    # Указательный
                    if finger[1]:
                        msg = '1'

                    # Средний палец
                    if finger[2]:
                        msg = '2'

                    # Мизинец
                    # if finger[4]:
                    #     msg = '3'
                    #
                    # if finger[4]:
                    #     print('4')

                    # Большой
                    if finger[0]:
                        msg = '3'
                    # if finger[1] and finger[0]:
                    #     msg = '3'
                    # msg = bytes(str(msg), 'utf-8')
                    # uart.write(msg)

                # if msg != '':
                msg = bytes(str(msg), 'utf-8')
                uart.write(msg)
                print(msg)


    # Вывод в окошко
    cv2.imshow("Image", img)

    # Если нажата клавиша
    if cv2.waitKey(1) == ord('q'):
        break



