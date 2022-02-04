import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [650, 550]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()
        self.z = 8

    def getImage(self):
        self.map_request = "https://static-maps.yandex.ru/1.x/?ll=47.30,56.00&size=650,450&z=8&l=map"
        response = requests.get(self.map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(self.map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

    def initUI(self):
        self.setFixedSize(*SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)
        self.out()

    def out(self):
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
            self.map_request = f"https://static-maps.yandex.ru/1.x/?ll=47.30,56.00&size=650,450&z={self.z}&l=map"
            self.out()
        elif event.key() == Qt.Key_PageUp and self.z > 2:
            self.z -= 1
            self.map_request = f"https://static-maps.yandex.ru/1.x/?ll=47.30,56.00&size=650,450&z={self.z}&l=map"
            self.out()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())