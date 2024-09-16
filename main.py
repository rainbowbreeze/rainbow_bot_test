""" Requires Python 3.6 because of string formatting
"""

# This for Google Cloud Functions management
import asyncio
import os

# This for ViaggiaTreno parsing
import requests
import datetime
import pytz


from functions_framework import http
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram import Update


@http
def telegram_bot(request):
    return asyncio.run(main(request))


async def main(request):
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    app = Application.builder().token(token).build()
    bot = app.bot

    app.add_handler(CommandHandler("start", on_start))
    app.add_handler(CommandHandler("ritardi_pavia", on_delays_pavia))
    app.add_handler(CommandHandler("ritardi_garibaldi_sott", on_delays_milano_garibaldi_sott))
    app.add_handler(CommandHandler("ritardi_rogoredo", on_delays_milano_rogoredo))
    app.add_handler(MessageHandler(filters.TEXT, on_message))

    if request.method == 'GET':
        await bot.set_webhook(f'https://{request.host}/telegram_bot')
        return "webhook set"

    async with app:
        update = Update.de_json(request.json, bot)
        await app.process_update(update)

    return "ok"


async def on_start(update: Update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm your first bot!"
    )


async def on_message(update: Update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )


async def on_delays_pavia(update: Update, context):
    send_delays_for_station("S01860", update, context)


async def on_delays_milano_garibaldi_sott(update: Update, context):
    send_delays_for_station("S01647", update, context)


async def on_delays_milano_rogoredo(update: Update, context):
    send_delays_for_station("S01820", update, context)



async def send_delays_for_station(station_code: str, update: Update, context) -> None:
    message = get_data_for_a_station(station_code)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )


def call_rest_api(url: str):
    """Calls a REST API using GET and returns the JSON payload."""

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


def time_to_string_literal(time: datetime, timezone_name: str) -> str:
    """Return a given time in a format used by the api

    Ideally: Sun Sep 15 2024 18:42:33 GMT+0200 (Central European Summer Time)
    Current: Sun Sep 15 2024 19:53:25 +0200 (CEST)
    """
    dt = datetime.datetime.now()

    # Set the timezone to Central European Summer Time
    timezone = pytz.timezone(timezone_name)
    dt = dt.astimezone(timezone)

    # Convert the datetime to a string in the desired format
    formatted_string = dt.strftime("%a %b %d %Y %H:%M:%S %z (%Z)")
    return formatted_string


def epoch_to_time(epoch_time: int, timezone_name: str) -> datetime:
    """Converts an epoch timestamp to a time in a specified timezone.

    Args:
        epoch_time (int): The epoch timestamp to convert.
        timezone_name (str): The name of the timezone to convert to.

    Returns:
        datetime.datetime: The converted datetime object.
    """

    # Create a datetime object from the epoch timestamp in UTC
    dt = datetime.datetime.fromtimestamp(epoch_time / 1000, tz=pytz.utc)

    # Convert the datetime object to the specified timezone
    timezone = pytz.timezone(timezone_name)
    dt = dt.astimezone(timezone)

    return dt


def is_empty_or_null(string):
    """Checks if a string is empty or null after trimming all spaces.

    Args:
      string: The string to check.

    Returns:
      True if the string is empty or null after trimming spaces, False otherwise.
    """

    if string is None or string.strip() == "":
        return True
    else:
        return False


def get_data_for_a_station(station_code: str) -> str:
    timezone_name: str = "Europe/Rome"
    time_for_url: str = time_to_string_literal(
        datetime.datetime.now(), timezone_name
    ).replace(" ", "%20")
    # api_url: str = "http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/partenze/S01860/Sun%20Sep%2015%202024%2018:42:33%20GMT+0200%20(Central%20European%20Summer%20Time)"
    api_url: str = f"http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/partenze/{station_code}/{time_for_url}"
    print(api_url)


    json_data = call_rest_api(api_url)
    train_list: str = ""

    if json_data:
        # import json
        # print(json.dumps(json_data, indent=4))
        if isinstance(json_data, list):
            for item in json_data:
                if "compNumeroTreno" in item:
                    try:
                        train: str = item["compNumeroTreno"]
                        destination: str = item["destinazione"]
                        departure_time: datetime = epoch_to_time(
                            item["orarioPartenza"], "Europe/Rome"
                        )
                        platform: str = item["binarioEffettivoPartenzaDescrizione"]
                        delay: int = item["ritardo"]
                        # circolante
                        partito: str = item["compInStazionePartenza"][0]
                        arrivato: str = item["compInStazioneArrivo"][0]

                        train_list += f"{train} per {destination} delle {departure_time.hour:02d}:{departure_time.minute:02d}: "
                        #print(f"{train} per {destination} delle {departure_time.hour:02d}:{departure_time.minute:02d}: ", end="")
                        if not is_empty_or_null(partito):
                            # When the train has left the station, I don't care anymore about its potential delay
                            # But the data has the train delay
                            train_list += f"{partito}"
                            #print(f"{partito}", end="")
                        else:
                            train_list += f"{delay}min"
                            #print(f"{delay}min", end="")
                            if not is_empty_or_null(arrivato):
                                train_list += f"{arrivato}min"
                                #print(f"{arrivato}min", end="")
                        train_list += "\n"
                        #print("")  # new line
                    except Exception as e:
                        train_list += "Si è verificato un errore processando il treno: " + type(e) + " - " + e + "\n"
                        print("Si è verificato un errore processando il treno: ", type(e), " - ", e)
                else:
                    train_list += "L'item non è un treno\n"
                    print("L'item non è un treno")
        else:
            train_list += "The returned data is not an array.\n"
            print("The returned data is not an array.")

    return train_list

