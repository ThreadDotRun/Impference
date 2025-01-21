from flask import Flask, request, render_template
import subprocess
import os
from flask import jsonify
import re
from SpecialCharacterRemover import SpecialCharacterRemover
import time

# Create Flask app instance
app = Flask(__name__)

class Llama:
    def __init__(self, model, execution_endpoint=None):
        self.model = model
        if execution_endpoint is not None:
            pass

    def prompt(self, prompt):
        print(f"{prompt}: ")
        return input()

    def run_llama(self, user_prompt
                  , context_size='2048'
                  , batch_size='8'
                  , num_tokens='1024'
                  , temperature='0.8'
                  , keep='75'
                  , repeat_penalty='1.1'
                  , color=True
                  , temp=.08):
            
        response = []
        command = ['/media/tdrsvr/a2c28d32-eac8-4438-b371-ce4a345bbf6d/llama/llama.cpp/main', '-m', self.model, '-c', context_size, '-b', batch_size, '-n', num_tokens,
                   '--keep', keep, '--repeat_penalty', repeat_penalty, '--no-penalize-nl', '--mirostat-lr', "0.1",
                  "--temp", "0.15", "--tfs", "0.95", "--mirostat-ent", "4.0"]        
        print(f"")
        print(f"command = {command}")
        if color:
            command.append('--color')

        command += ['-p', user_prompt]

        try:
            with subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as proc:
                for line in proc.stdout:
                    #print(f"Line: {line}", end='')
                    # Escape HTML special characters and replace newlines with <br> tags
                    #escaped_line = line.replace('\n', '<br>')
                    response.append(line)
                    time.sleep(5)
                    #command_clear_buffers = "sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'"
                    #full_command = f"echo {password} | sudo -S {command_clear_buffers}"
                    #result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print(f"line {line}")
        except subprocess.SubprocessError as e:
            print(f"An error occurred: {e}")
            response = ["Error processing the request."]
        return ''.join(response)

    def save_output(self, prompt, output):
        safe_prompt = prompt.replace(' ', '_')
        filename = f"{safe_prompt}.txt"
        with open(filename, 'w') as f:
            f.write(output)

model_folder = './models'         
prompts_folder = './prompts'  # Path to the prompts folder
context_size_folder = './context_size'  # contexts
num_tokens_folder = './num_tokens'  # Path to num tokens
temperature_folder = './temperatures'  # Path to temps folder
#For prompt use promtname.txt with prompt in the file
#For the rest just feate a file where then name is <number>.txt with no data in it. The file proefix is the data like:
# 32.txt, 64.txt, etc for context length and num_tokens. Models obviously go in the model folder 
#Like 
#├── temperatures
#│   ├── 0.05.temp
#│   ├── 0.3.temp
#│   ├── 1.5.temp
#│   └── 1.temp

def get_model_list():    
    return [f for f in os.listdir(model_folder)]

def get_prompt_list():
    return [f for f in os.listdir(prompts_folder) ]

def get_cls_list():
    return [f for f in os.listdir(context_size_folder) ]

def get_num_tokens_list():
    return [f for f in os.listdir(num_tokens_folder) ]

def get_temperature_list():
    return [f for f in os.listdir(temperature_folder) ]
    
@app.route('/', methods=['GET'])
def index():
    print(f"Root running...")
    models = get_model_list()
    prompts = get_prompt_list()  # Get the list of prompts
    ctls = get_cls_list()
    gntl = get_num_tokens_list()
    temperatures = get_temperature_list()
    
    num_tokens = [re.sub(".*ipynb.*", "1", gnt.replace(".ctl", "")) for gnt in gntl]    
    selected_ctls = [re.sub(".*ipynb.*", "1", ctl.replace(".ctl", "")) for ctl in ctls]
    selected_temperatures = [re.sub(".*ipynb.*", "1", temperature.replace(".temp", "")) for temperature in temperatures]
    print(f"selected_temperatures: {selected_temperatures}")
    return render_template('index.html', models=models, prompts=prompts, cls_list=selected_ctls, num_tokens=num_tokens, temps=selected_temperatures)

@app.route('/run_model', methods=['POST'])
def run_model():
    print(f"run_model running...")
    data = request.get_json()
    selected_model = data['model']
    selected_prompt_file = data['prompt']
    user_input = data['input']
    selected_ctls = data['ctls']  # Get the selected context size    
    num_token = data['num_tokens']
    temps = data['temps']
    print(f"temperature: {temps}")
    try:
        batch_size = data['batch_size']
    except:
        batch_size = selected_ctls

    try:
        # Construct the full path to the prompt file
        prompt_file_path = os.path.join('prompts', selected_prompt_file)
        print(f"prompt_file_path: {prompt_file_path}")
    
        # Read the content of the selected prompt file
        with open(prompt_file_path, 'r') as file:
            system_prompt = f"{file.read().strip()}"
    except:
        system_prompt = ""

    # Now format the user_input with the system prompt    
    #formatted_input = f"System Role: `{system_prompt}`\n\nInstruction: `{user_input}`"   
    
    print(f"formatted_input: {user_input}")
    llama = Llama(f"{model_folder}/{selected_model}")
    response = llama.run_llama(user_input, context_size=f'{selected_ctls}', batch_size=f'{selected_ctls}', num_tokens=f'{num_token}', temp=f'{temps}')
    text_processor = SpecialCharacterRemover()
    print(f"Raw response: {response}")    
    #pattern = "\n"
    #response =  re.sub(pattern, "<br>", response)
    #re.sub(pattern, "", response)
    print(f"response1: {response}")
    response = text_processor.remove_special_chars(response)
    #response = text_processor.extract_text(response, start_delimiter="response\":")
    print(f"response2: {response}")
    #response = response[len(formatted_input):]
    response = re.sub("\\n", '<br>\n', response)

    try:
        with open(filename, 'w') as file:
            file.write(f"\n -- Result {response}")
    except Exception as e:
        print(f"Erro generated response writing file. {str(e)}")
    
    return jsonify(response=f"{response}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)





