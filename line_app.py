{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "\n",
    "# 引入套件 flask\n",
    "from flask import Flask, request, abort\n",
    "\n",
    "from linebot import (\n",
    "    LineBotApi, WebhookHandler\n",
    ")\n",
    "# 引入 linebot 異常處理\n",
    "from linebot.exceptions import (\n",
    "    InvalidSignatureError\n",
    ")\n",
    "# 引入 linebot 訊息元件\n",
    "from linebot.models import (\n",
    "    MessageEvent, TextMessage, TextSendMessage,\n",
    ")\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "\n",
    "# LINE_CHANNEL_SECRET 和 LINE_CHANNEL_ACCESS_TOKEN 類似聊天機器人的密碼，記得不要放到 repl.it 或是和他人分享\n",
    "# 從環境變數取出設定參數\n",
    "LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')\n",
    "LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')\n",
    "line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)\n",
    "handler = WebhookHandler(LINE_CHANNEL_SECRET)\n",
    "\n",
    "\n",
    "# 此為歡迎畫面處理函式，當網址後面是 / 時由它處理\n",
    "@app.route(\"/\", methods=['GET'])\n",
    "def hello():\n",
    "    return 'hello heroku'\n",
    "\n",
    "# 此為 Webhook callback endpoint 處理函式，當網址後面是 /callback 時由它處理\n",
    "@app.route(\"/callback\", methods=['POST'])\n",
    "def callback():\n",
    "    # 取得網路請求的標頭 X-Line-Signature 內容，確認請求是從 LINE Server 送來的\n",
    "    signature = request.headers['X-Line-Signature']\n",
    "\n",
    "    # 將請求內容取出\n",
    "    body = request.get_data(as_text=True)\n",
    "\n",
    "    # handle webhook body（轉送給負責處理的 handler，ex. handle_message）\n",
    "    try:\n",
    "        handler.handle(body, signature)\n",
    "    except InvalidSignatureError:\n",
    "        print(\"Invalid signature. Please check your channel access token/channel secret.\")\n",
    "        abort(400)\n",
    "\n",
    "    return 'OK'\n",
    "\n",
    "# decorator 負責判斷 event 為 MessageEvent 實例，event.message 為 TextMessage 實例。所以此為處理 TextMessage 的 handler\n",
    "@handler.add(MessageEvent, message=TextMessage)\n",
    "def handle_message(event):\n",
    "    # 決定要回傳什麼 Component 到 Channel，這邊使用 TextSendMessage\n",
    "    # event.message.text 為使用者的輸入，把它原封不動回傳回去\n",
    "    line_bot_api.reply_message(\n",
    "        event.reply_token,\n",
    "        TextSendMessage(text=event.message.text))\n",
    "\n",
    "# __name__ 為內建變數，若程式不是被當作模組引入則為 __main__\n",
    "if __name__ == \"__main__\":\n",
    "    # 此處不使用 reol.it，所以不用設定 IP 和 Port，flask 預設為 5000 port\n",
    "    app.run()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
