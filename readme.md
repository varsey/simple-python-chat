#how to use
1. Start server `python chat/server.py`
2. Start client `python chat/client.py`
3. Start one more client to chat `python chat/client.py`

Для установки зависимостей проекта необходимо выполнить

```
pip install -r requirements.txt
```

Для просмотра списка установленных пакетов

```
pip list
```

Для выгрузки списка установленных пакетов

```
pip freeze > requirements.txt
```

Для установки Telnet

MacOS:
```
brew install telnet
```

Ubuntu:
```
sudo apt-get install telnet
```

Windows: [инструкция](https://help.keenetic.com/hc/ru/articles/213965809-%D0%92%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D1%81%D0%BB%D1%83%D0%B6%D0%B1-Telnet-%D0%B8-TFTP-%D0%B2-Windows)

## Возможные проблемы

### Проблема установки PyQt5-sip (Windows)

- Необходимо установить С++ build tools
    - [Объяснение](https://stackoverflow.com/a/40525033/4941870)
    - [Качать отсюда](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019) "Build Tools for Visual Studio 2019"
    - Установить.
    - Перезагрузить компьютер
    - Повторить установку пакетов `pip install -r requirements.txt`
