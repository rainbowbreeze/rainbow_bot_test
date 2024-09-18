# Tests to manage a Telegram bot using Google Cloud Function


Reference videos
- [Learn Cloud Functions by deploying a simple Telegram Bot](https://www.youtube.com/watch?v=olH-xCZ7zYk)
  - https://github.com/rznzippy/yt-gcp-telegram-bot
  - Setting permissions to call funcions by everyone
  - Telegram bot is registered doing a manual GET call to the cloud functio address
- [Build, deploy and host a Telegram Bot on Google Cloud Functions for free using Python](https://www.youtube.com/watch?v=jzwMzUAAOWk)
- [Building a Serverless Telegram bot using Google Cloud Functions…!](https://medium.com/@2004.vimald/building-a-serverless-telegram-bot-using-google-cloud-functions-27883047f40b)
  - It uses the command line
  - No async or other calls
- https://gitlab.com/Athamaxy/telegram-bot-tutorial/-/blob/main/TutorialBot.py
  - Simple code to set telegram menu once a command is sent
  - It uses command handlers /something
    - They need to be registered in Botfather, defining in the code doesn't configure the bot
  - It uses MessageHandler to process to rest of the test sent to the bot
  - A good reading connected with https://core.telegram.org/bots/tutorial#echo-bot


## Google Cloud Functions management

To deploy the cloud function, open the Cloud IDE in the root folder of the project, then follow the steps in the first video

Select the region: https://cloud.google.com/about/locations#europe
europe-west8 -> Milan -> It doesn't work, so I selected europe-west3

Once the cloud function was deployed for the first time, edit the function and set the TELEGRAM_BOT_TOKEN env var following Google Cloud console UI help: https://cloud.google.com/functions/docs/configuring/env-var






## Trenitalia ViaggiaTreno notes

Previous doc on Trenitalia APIs
- https://github.com/sabas/trenitalia
- https://github.com/Razorphyn/Informazioni-Treni-Italiani
- https://github.com/roughconsensusandrunningcode/TrainMonitor/wiki/API-del-sistema-Viaggiatreno
- https://github.com/SimoDax/Trenitalia-API/wiki/Nuove-API-Trenitalia-lefrecce.it
- https://github.com/levnikmyskin/ritarditalia/blob/master/telegram_bot/main_bot.py
  - https://www.reddit.com/r/italy/comments/b1cncm/un_bot_telegram_per_i_ritardi_di_trenitalia/
- https://github.com/jacopo-j/TrenitaliaAPI
- https://github.com/TrinTragula/api-trenitalia


Using http://www.viaggiatreno.it/infomobilita/index.jsp and looking at the Netork traffic in Chome DevTools, is possible to see the calls made to Trenitalia API to get details for train station and specific train

The API can be called via get directly on the web browser

This is the most efficient way to get latest on APIs to call


https://trainstats.altervista.org/
- has delays day byu train
- found on Reddit, https://www.reddit.com/r/italy/comments/d702r4/ho_creato_un_sito_per_monitorare_i_ritardi_di/ 