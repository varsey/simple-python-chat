from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineOnlyReceiver


class Client(LineOnlyReceiver):
    ip: str = None
    login: str = None
    factory: 'Chat'

    def __init__(self, factory):
        """
        Инициализация фабрики клиента
        :param factory:
        """
        self.factory = factory

    def connectionMade(self):
        """
        Обработчик подключения нового клиента
        """

        # FIXME: исправлено getHost на getPeer для клиента (спасибо Alexey Tischenko)
        self.ip = self.transport.getPeer().host
        self.factory.clients.append(self)

        print(f"Client connected: {self.ip}")

        self.sendLine("Welcome to the chat v0.1".encode())

    def lineReceived(self, data: bytes):
        """
        Обработчик нового сообщения от клиента
        :param data:
        """
        message = data.decode().replace('\n', '')

        # FIXME: Убрали пока проверку логина, сразу даем доступ на передачу сообщений

        server_message = f"<NEW MESSAGE> {message}"
        self.factory.notify_all_users(server_message)

        print(server_message)

    def connectionLost(self, reason=None):
        """
        Обработчик отключения клиента
        :param reason:
        """
        self.factory.clients.remove(self)
        print(f"Client disconnected: {self.ip}")


class Chat(ServerFactory):
    clients: list

    def __init__(self):
        """
        Инициализация сервера
        """
        self.clients = []
        print("*" * 10, "\nStart server \nCompleted [OK]")

    def startFactory(self):
        """
        Запуск процесса ожидания новых клиентов
        :return:
        """
        print("\n\nStart listening for the clients...")

    def buildProtocol(self, addr):
        """
        Инициализация нового клиента
        :param addr:
        :return:
        """
        return Client(self)

    def notify_all_users(self, data: str):
        """
        Отправка сообщений всем текущим пользователям
        :param data:
        :return:
        """
        for user in self.clients:
            user.sendLine(data.encode())


def start_server():
    reactor.listenTCP(7410, Chat())
    reactor.run()


if __name__ == '__main__':
    start_server()
