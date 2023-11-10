import requests
import json
import datetime

class BraveChat:
    def __init__(self, x_brave_key):
            self.headers = {
                "pragma": "no-cache",
                "cache-control": "no-cache",
                "accept": "text/event-stream",
                "x-brave-key": x_brave_key,
                "content-type": "application/json",
                "sec-fetch-site": "none",
                "sec-fetch-mode": "no-cors",
                "sec-fetch-dest": "empty",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9"
            }
            self.url = "https://ai-chat.bsg.brave.com/v1/complete"
            
    def get_current_datetime(self):
        dateday = {
            "day": datetime.datetime.today().strftime('%A'),
            "month": datetime.datetime.today().strftime('%B'),
            "date": datetime.datetime.today().strftime('%d'),
            "year": datetime.datetime.today().strftime('%Y'),
            "time": datetime.datetime.today().strftime('%I:%M:%S %p'),
        }
        return dateday
    
    def generate_response(self, userinput, system_prompt=None):
        dateday = self.get_current_datetime()
        self.base_prompt = f"The current time and date is {dateday['day']}, {dateday['month']} {dateday['date']}, {dateday['year']} at {dateday['time']} PM"
        if system_prompt is None:
            system_prompt = self.base_prompt + "\n\nYour name is Leo, a helpful, respectful and honest AI assistant created by the company Brave. You will be replying to a user of the Brave browser. Always respond in a neutral tone. Be polite and courteous. Answer concisely in no more than 50-80 words.\n\nPlease ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n"
        else:
            system_prompt = self.base_prompt + system_prompt
            
        body = {
            "max_tokens_to_sample": 600,
            "model": "llama-2-13b-chat",
            "prompt": f'<s>[INST] <<SYS>>\{system_prompt}<</SYS>>\n\n{userinput} [/INST]',
            "stop_sequences": [
                "</response>",
                "</s>"
            ],
            "stream": "false",
            "temperature": 0.2,
            "top_k": -1,
            "top_p": 0.999
        }
        
        response = requests.post(url=self.url, headers=self.headers, data=json.dumps(body))
        
        if response.status_code == 200:
            data = json.loads(response.text)
            output = data["completion"]
            return '\n'+output
        else:
            return f"Error: {response.status_code} - {response.text}"
        
        
if __name__ == "__main__":
    x_brave_key = input("Enter your x-brave-key: ")
    system_prompt = input("Enter your system prompt (leave blank for default): ")
    if system_prompt == "":
        system_prompt = None
        
    chatbot = BraveChat(x_brave_key=x_brave_key)

    while True:
        user_input = input("Enter your message (type '0' to quit and '1' to update sys prompt): ")
        if user_input.lower() == "0":
            break
        if  user_input.lower() == "1":
            system_prompt = input("Enter your system prompt (leave blank for default): ")
            if system_prompt == "":
                system_prompt = None
            continue
        response = chatbot.generate_response(user_input, system_prompt=system_prompt)
        print(response)