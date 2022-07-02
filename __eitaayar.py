# In the name of Allah

# Author: Abolfazl Danayi
# Email: adanayidet@gmail.com

import requests
import os
import typing as T


class _EitaayarResponse:
    def __init__(self, parent: 'Eitaayar', method_name: str, data: dict) -> None:
        self.__parent = parent
        self.__data = data
        self.__method_name = method_name

    @property
    def ok(self) -> bool:
        try:
            return self.__data["ok"]
        except:
            return False

    @property
    def reply(self) -> '_EitaayarReplier':
        return _EitaayarReplier(self.__parent, self.message_id)

    @property
    def message_id(self) -> T.Union[None, str]:
        if self.ok and "message_id" in self.result:
            return self.result["message_id"]
        else:
            return None

    def __repr__(self) -> str:
        return f'Eitaayar({self.message_id}@{self.__method_name.replace("send","").lower()})->{"ok" if self.ok else "error"}'

    @property
    def result(self) -> dict:
        return self.__data['result']

    def __getitem__(self, kw: str) -> str:
        return self.__data[kw]

    def __bool__(self) -> bool:
        return self.ok


class Eitaayar:
    """You can easily work with eitaayar platform. Just make an object of this class and start your work!"""

    def __init__(self, token: str, chat_id: str, timeout: float = 3000) -> None:
        self.__token = token
        self.__chat_id = chat_id
        self.__timeout = timeout

    @property
    def token(self) -> str:
        return self.__token

    @property
    def chat_id(self) -> str:
        return self.__chat_id

    @property
    def timeout(self) -> float:
        return self.__timeout

    def __post(self, method_name: str, data: dict, files=None):
        url = self.__url(method_name)
        header = {
            'User-Agent': "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.7) Gecko/2009032803"
        }
        if type(self) == _EitaayarReplier:
            data['reply_to_message_id'] = self.reply_to_message_id
        if 'reply_to_message_id' in data and data['reply_to_message_id'] is not None:
            r = data['reply_to_message_id']
            if type(r) == _EitaayarResponse:
                data['reply_to_message_id'] = r.message_id
        r = requests.post(url, data=data, timeout=self.__timeout,
                          headers=header, files=files)
        return _EitaayarResponse(self, method_name, r.json())

    def __url(self, method_name: str) -> str:
        return f'https://eitaayar.ir/api/{self.__token}/{method_name}'

    def getMe(self) -> _EitaayarResponse:
        ret = self.__post('getMe', {}, None)
        return ret

    def sendText(self, text: str, title: str = None, notify: bool = True, reply_to_message_id: str = None, pin: bool = False, viewCountForDelete: bool = None) -> _EitaayarResponse:
        return self.sendMessage(text, title, notify, reply_to_message_id, pin, viewCountForDelete)

    def sendMessage(self, text: str, title: str = None, notify: bool = True, reply_to_message_id: str = None, pin: bool = False, viewCountForDelete: bool = None) -> _EitaayarResponse:
        d = {
            'chat_id': self.__chat_id,
            'text': text
        }
        if title is not None:
            d['title'] = title
        if not notify:
            d['disable_notification'] = 1
        if reply_to_message_id is not None:
            d['reply_to_message_id'] = str(reply_to_message_id)
        if pin:
            d['pin'] = 1
        if viewCountForDelete:
            d['viewCountForDelete'] = int(viewCountForDelete)
        return self.__post('sendMessage', d, None)

    def sendFile(self, filepath: str, caption: str = None, filename: str = None, title: str = None, notify: bool = True, reply_to_message_id: str = None, pin: bool = False, viewCountForDelete: bool = None) -> _EitaayarResponse:
        d = {
            'chat_id': self.__chat_id
        }
        if filename is None:
            filename = os.path.split(filepath)[1]
        if caption is not None:
            d['caption'] = caption
        if title is not None:
            d['title'] = title
        if not notify:
            d['disable_notification'] = 1
        if reply_to_message_id is not None:
            d['reply_to_message_id'] = reply_to_message_id
        if pin:
            d['pin'] = 1
        if viewCountForDelete:
            d['viewCountForDelete'] = int(viewCountForDelete)
        files = {
            'file': (filename, open(filepath, 'rb'))
        }
        return self.__post('sendFile', d, files)

    def sendPhoto(self, filepath: str, caption: str = None, filename: str = None, title: str = None, notify: bool = True, reply_to_message_id: str = None, pin: bool = False, viewCountForDelete: bool = None) -> _EitaayarResponse:
        return self.sendFile(self, filepath, caption, filename, title, notify, reply_to_message_id, pin, viewCountForDelete)

    def sendGif(self, filepath: str, caption: str = None, title: str = None, notify: bool = True, reply_to_message_id: str = None, pin: bool = False, viewCountForDelete: bool = None) -> _EitaayarResponse:
        filename = os.path.split(filepath)[1]
        filename = f'{filename.split(".")[0]}.gif'
        return self.sendFile(filepath, filename, caption, title, notify, reply_to_message_id, pin, viewCountForDelete)

    def sendSticker(self, filepath: str, caption: str = None, title: str = None, notify: bool = True, reply_to_message_id: str = None, pin: bool = False, viewCountForDelete: bool = None) -> _EitaayarResponse:
        filename = os.path.split(filepath)[1]
        filename = f'{filename.split(".")[0]}.webp'
        return self.sendFile(filepath, filename, caption, title, notify, reply_to_message_id, pin, viewCountForDelete)


class _EitaayarReplier(Eitaayar):
    def __init__(self, parent_eitaayar: Eitaayar, reply_to_message_id: T.Union[None, str]) -> None:
        super().__init__(parent_eitaayar.token,
                         parent_eitaayar.chat_id, parent_eitaayar.timeout)
        self.__reply_to_message_id = reply_to_message_id

    @property
    def reply_to_message_id(self) -> T.Union[str, None]:
        return self.__reply_to_message_id
