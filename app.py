import requests
import json
import time
import sys
import os
import random

# Define your app token directly in the script
app_token = "8532504230140290|vriVvrS7gZz4orSXFkoKMNnLZRI"

# Get the access token for the user (from Kiwi Browser and Vinhtool)
access_token = ""

# Commands to listen for
commands = ["bot", "taklu", "beta", "babu"]

# Function to send messages based on command
def send_message(convo_id, message):
    url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    payload = {
        'message': message
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.ok:
        print(f"[+] Message sent to convo {convo_id}: {message}")
    else:
        print(f"[x] Failed to send message to convo {convo_id}")

# Read commands.txt for messages
def load_messages():
    with open('commands.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

# Check if the command is valid
def process_command(command):
    if command in commands:
        messages = load_messages()
        if messages:
            return random.choice(messages)
    return None

# Check if the group UID is listed in convo.txt
def is_valid_convo(convo_id):
    with open('convo.txt', 'r') as file:
        convo_ids = [line.strip() for line in file.readlines()]
    return convo_id in convo_ids

def main():
    while True:
        # Simulating command reception (this should be replaced with actual message receiving logic)
        convo_id = input("Enter convo ID (group UID): ").strip()
        command = input("Enter command: ").strip()

        if is_valid_convo(convo_id):
            message = process_command(command)
            if message:
                send_message(convo_id, message)
            else:
                print(f"[!] Invalid command: {command}")
        else:
            print(f"[!] Convo ID {convo_id} not in convo.txt")

if __name__ == '__main__':
    main()
