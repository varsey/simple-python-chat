import sys
from PyQt5 import QtWidgets
from gui import design

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver


class ChatClient(LineOnlyReceiver):
    """
    Класс для работы с подключением к серверу
    """
    factory: 'ChatFactory'

    def __init__(self, factory):
        """
        Запоминаем фабрику для последующего обращения
        :param factory:
        """
        self.factory = factory

    def connectionMade(self):
        """
        Обработчик установки соединения с сервером
        :return:
        """
        self.factory.window.protocol = self  # записали в окно приложения текущий протокол

    def lineReceived(self, line):
        """
        Обработчик получения новой строки от сервера
        :param line:
        :return:
        """
        message = line.decode()  # раскодируем
        self.factory.window.plainTextEdit.appendPlainText(message)  # добавим в поле сообщений


class ChatFactory(ClientFactory):
    """
    Класс фабрики для создания подключения
    """
    window: 'ExampleApp'

    def __init__(self, window):
        """
        Запоминаем окно приложения в конструкторе для обращения
        :param window:
        """
        self.window = window

    def buildProtocol(self, addr):
        """
        Обработчик создания подключения
        :param addr:
        :return:
        """
        return ChatClient(self)


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    """
    Класс для запуска графического приложения
    """
    protocol: ChatClient  # протокол подключения
    reactor = None  # ссылка на рекатор для обращения

    def __init__(self):
        """
        Запуск приложения и обработчиков
        """
        super().__init__()
        self.setupUi(self)  # подгружаем интерфейс
        self.init_handlers()  # настраиваем обработчики действий

    def init_handlers(self):
        """
        Создание обработчиков действий (кнопки, поля и тд)
        :return:
        """
        self.pushButton.clicked.connect(self.send_message)  # событие нажатия на кнопку

    def closeEvent(self, event):
        """
        Обработчик закрытия окна
        :param event:
        :return:
        """
        self.reactor.callFromThread(self.reactor.stop)  # остановка реактора

    def send_message(self):
        """
        Обработчик для отправки сообщения на сервер
        :return:
        """
        self.protocol.sendLine(self.lineEdit.text().encode())  # отправили на сервер
        self.lineEdit.setText('')  # сброс текста


def main():
    # создаем приложение
    app = QtWidgets.QApplication(sys.argv)
    # испортируем реактор для Qt
    import qt5reactor

    # создаем графическое окно
    window = ExampleApp()
    window.show()

    # настройка реактора Qt
    qt5reactor.install()
    # импортируем стандартный реактор
    from twisted.internet import reactor

    # стнадартный запуск реактора
    reactor.connectTCP("localhost", 7410, ChatFactory(window))
    # передаем его также в окно для обращения
    window.reactor = reactor
    reactor.run()


if __name__ == '__main__':
    main()
