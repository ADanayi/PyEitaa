# PyEitaa
This simple library can be used to send messages and files to Eitaa messenger super-groups and channels.

## How to install
Currently you should clone this git repository, but in future I'm going to publish it on the `PyPI` so you can install it using `pip`. However, right now just clone the whole folder alongside your main python script file and use it. 

For example if I have a `main.py` file in `project` folder then I open a terminal in `project` folder and enter this command:

```bash
git clone https://github.com/ADanayi/PyEitaa
```

Following examples can be written in `main.py` file.

## How to use
*It takes less than 5 minutes!*

The usage is pretty simple. First visit [eitaayar](https://eitaayar.ir) and create your account. In the API part you can get your access token and you can also register the bot (@Sender) for super-groups and channels.

### 1) Sending a text message
You can easily create a bot object. It gets the `access_token` and `chat_id` and then you can send text, photo and sticker messages using this bot.
```python
import PyEitaa

token = 'YOUR SECRET TOKEN from eitaayar.ir'
chat_id = 'YOUR CHAT (CHANNEL OR SUPER GROUP) ID from eitaayar.ir'

bot = PyEitaa.Eitaayar(token, chat_id)

message = bot.sendMessage('Hello from Bot!') # Or you can use sendText as simple alias
```

### 2) Checking if the message is sent
Simply use if expression:

```python
message = bot.sendMessage('Hello from Bot!')
if message:
    print('message is sent!')
```

Also if you are developing you can simply print the message:
```python
message = bot.sendMessage('Hello from Bot!')
print(message) # Eitaayar(17037639@message)->ok
```

### 3) Reply
The message in previous examples has a `message_id` property. You can use it to reply:

```python
message = bot.sendMessage('I am a bot')
if message:
    message2 = bot.sendMessage('And I reply my messages!', reply_to_message_id=message.message_id)
```

### 4) Send File, Photo, Gif and Sticker
Simply use this syntax:

```python
doc_msg = bot.sendFile('doc.pdf', caption='This is a pdf!')
photo_msg = bot.sendPhoto('photo.jpg', caption='This is my photo!')
gif_msg = bot.sendGif('moving.gif', caption='This is a gif!') # .mp4 files are allowed too.
sticker_msg = bot.sendSticker('sticker.png', caption='This is a sticker!')
```

Note: sendPhoto and sendFile are exactly the same.

### 5) Super-fast method
Consider you want to send a number of messages replying each other. Simply use this method:

```python
bot.sendMessage('Hello.').reply.\
    sendMessage('I am Abolfazl.').reply.\
    sendMessage('My last name is Danayi.').reply.\
    sendMessage('I am a PhD student in Electrical Engineering...').reply.\
    sendFile('photo.jpg', 'this is my photo!')
```