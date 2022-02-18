import os
import sys
import requests
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

SCREEN_SIZE = [650, 550]
SLOI = {0: 'Схема map', 1: 'Спутник sat', 2: 'Гибрид sat,skl'}


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        self.map_request = "https://static-maps.yandex.ru/1.x/?ll=47.30,56.00&size=650,450&z=8&l=map"
        response = requests.get(self.map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(self.map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

    def initUI(self):
        self.setFocusPolicy(Qt.StrongFocus)
        self.l = 0
        self.k = 0.7
        self.m = 1.8
        self.setFixedSize(*SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)
        self.image.setGeometry(0, 0, 650, 450)
        self.sloi = QPushButton(self)
        self.sloi.setGeometry(275, 475, 100, 50)
        self.sloi.setText(SLOI[self.l].split()[0])
        self.sloi.setFont(QFont("Arial", 15))
        self.sloi.clicked.connect(self.Sloi_)
        self.coords = QLineEdit(self)
        self.coords.setText('Координаты в градусах')
        self.coords.setGeometry(10, 475, 150, 25)
        self.mashtab = QLineEdit(self)
        self.mashtab.setText('Масштаб')
        self.mashtab.setGeometry(10, 500, 150, 25)
        self.show_ = QPushButton(self)
        self.show_.setGeometry(167, 475, 100, 50)
        self.show_.setText('Показать')
        self.show_.clicked.connect(self.Show_)


    def out(self):
        self.map_request = f"https://static-maps.yandex.ru/1.x/?ll={self.width},{self.longitude}&size=650,450&z=" \
                           f"{self.z}&l={SLOI[self.l % 3].split()[-1]}"
        response = requests.get(self.map_request)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown and self.z < 23:
            self.z += 1
            self.k /= 2
            self.m /= 2
            self.out()
        elif event.key() == Qt.Key_PageUp and self.z > 2:
            self.z -= 1
            self.k *= 2
            self.m *= 2
            self.out()
        elif event.key() == Qt.Key_Up:
            self.longitude += self.k
            self.out()
        elif event.key() == Qt.Key_Down:
            self.longitude -= self.k
            self.out()
        elif event.key() == Qt.Key_Right:
            self.width += self.m
            self.out()
        elif event.key() == Qt.Key_Left:
            self.width -= self.m
            self.out()

    def Sloi_(self):
        self.l += 1
        self.sloi.setText(SLOI[self.l % 3].split()[0])
        self.out()

    def Show_(self):
        self.z = self.mashtab.text()
        if self.z.isdigit():
            self.z = int(self.z)
            if 23 < self.z or self.z < 2:
                self.z = 8
                self.width, self.longitude = 47.30, 56
            else:
                try:
                    self.width, self.longitude = map(float, self.coords.text().split())
                except ValueError:
                    self.z = 8
                    self.width, self.longitude = 47.30, 56
        else:
            self.z = 8
            self.width, self.longitude = 47.30, 56
        self.out()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())