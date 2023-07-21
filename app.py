from flask import Flask, render_template, request, jsonify
import bardapi
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

# Set your __Secure-1PSID value to key
token = 'YgjfslpT83yYcV48tlNWjOrRVx5pxNzVylaJt-Gt1Yp95kY__RUwXIORQJTc5HYGTf3Q8Q.'

class RestartingEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print("Detected change in source code. Restarting server...")
        os._exit(0)  # Force the server to exit and restart

def start_observer():
    path = os.path.abspath(os.path.dirname(__file__))
    event_handler = RestartingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        input_text = request.form['prompt']

        # Send an API request and get a response (assuming 'response' is a dictionary containing various data types)
        response = bardapi.core.Bard(token).get_answer(input_text)
        

        # Convert sets to lists before returning JSON
        response = convert_sets_to_lists(response)

        # Return the response data as JSON
        output = response["choices"][0]["content"][0]
        response = jsonify(output=output)  # Return JSON response
        response.headers.add('Access-Control-Allow-Origin', '*')  # Add the CORS header
        return response
    else:
        return render_template('index.html')

def convert_sets_to_lists(obj):
    if isinstance(obj, dict):
        return {key: convert_sets_to_lists(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_sets_to_lists(element) for element in obj]
    elif isinstance(obj, set):
        return list(obj)  # Convert set to list
    return obj

if __name__ == '__main__':
    start_observer()
    app.run(debug=True, use_reloader=False)
