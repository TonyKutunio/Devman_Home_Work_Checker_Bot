#Devman Telegram Bot
This Bot will sends notifications of code review from Devman to the telegram.
  
   
## How to install
`Python3` should be already installed. Then use pip (or pip3, if there is a conflict with `Python2`) to install dependencies:   

```
pip install -r requirements.txt
```  
## setting up .env variables   
  You will  have to set your environment variables up, with `.env` file where you going to store
  your `TELEGRAM_API_TOKEN`, your `TELEGRAM_CHAT_ID` and your `DEVMAN_API_TOKEN`  
  

You can use [Notepad++](https://notepad-plus-plus.org/downloads/) to create `.env` file for Windows,
or [CotEditor](https://coteditor.com/) for MacOS.
  
##### This is an example of how it looks like inside of your .env file. 
(You can choose your own variable names if you want)  
```
TELEGRAM_API_TOKEN=Your_TelgramToken
TELEGRAM_CHAT_ID=yourChatId
DEVMAN_API_TOKEN=_ApiKey
```

Variables has to be with CAPITAL letters and without any spaces at all!  

### Project Goals  
To make life easier
 
