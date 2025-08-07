import requests
import subprocess
import re

def run_command(command):
    command = re.sub(r"^```cmd\n|```$", "", command.strip(), flags=re.MULTILINE).strip()
    
    commands = command.splitlines()

    output = ""
    for cmd in commands:
        if not cmd.strip():
            continue
        completed_process = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        output += completed_process.stdout + completed_process.stderr

    return output

def get_command_output(user_input):
    url = "https://synchrony-hackathon.onrender.com/api/command/gemini"
    payload = {"input": user_input}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        if data.get("success") and "result" in data:
            raw_command = data['result']
            
            if "```cmd" in raw_command:
                result = run_command(raw_command)
                return result
            else:
                return raw_command
        else:
            return "Invalid response from API."
    except requests.exceptions.RequestException as e:
        return f"API request failed: {str(e)}"