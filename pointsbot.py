import random
import re
import datetime
import gspread
import configparser
from oauth2client.service_account import ServiceAccountCredentials

from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mregex_handler import MRegexHandler
from matrix_bot_api.mcommand_handler import MCommandHandler

# Global variables
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
SHEET_NAME = "Giveth_Points_Tracker"
sheet = client.open(SHEET_NAME).sheet1

def dish_points_callback(room, event):
    try:
        body = event['content']['body']
        args = body.split()
        n_points = args[1]
        point_type = args[2]
        match = re.search('([@\w:.-]+) for (.*)', body)
        handle = match.group(1)
        reason = match.group(2)
        event_id = event['event_id']
        room_id = event['room_id']
        location = "https://riot.im/app/#/room/" + room_id + "/" + event_id
        now = datetime.datetime.now()
        date = str(now.day) + "-" + str(now.month) + "-" + str(now.year)
        sender = event['sender'].split(":")[0]
        row = [sender, handle, n_points, point_type, reason, date, location]
        sheet.append_row(row)
        room.send_text(sender + " dished " + str(n_points) + " " + point_type + " points to " + handle)
    except AttributeError:
        room.send_text("ERROR, please use the following format:\n\
!dish [#of points] [type of points] points to [handle] for [reason explaining why]")


def points_help_callback(room, event):
    room.send_text("Please dish points using the format:\n\
!dish [#of points] [type of points] points to [handle] for [reason explaining why]")


def main():

    # Load configuration
    config = configparser.ConfigParser()
    config.read("config.ini")
    username = config.get("Matrix", "Username")
    password = config.get("Matrix", "Password")
    server = config.get("Matrix", "Homeserver")

    # Create an instance of the MatrixBotAPI
    bot = MatrixBotAPI(username, password, server)

    # Add a regex handler waiting for the echo command
    dish_handler = MCommandHandler("dish", dish_points_callback)
    bot.add_handler(dish_handler)

    help_handler =  MCommandHandler("pointshelp", points_help_callback)
    bot.add_handler(help_handler)

    # Start polling
    bot.start_polling()

    # Infinitely read stdin to stall main thread while the bot runs in other threads
    while True:
        input()

if __name__ == "__main__":
    main()
