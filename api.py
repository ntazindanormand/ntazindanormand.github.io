from flask import Flask, request, jsonify
import bardapi
import os

app = Flask(__name__)

# Set your __Secure-1PSID value to key
token = 'YgjfslpT83yYcV48tlNWjOrRVx5pxNzVylaJt-Gt1Yp95kY__RUwXIORQJTc5HYGTf3Q8Q.'

@app.route('/', methods=['POST'])
def get_answer():
    input_text = request.json.get('prompt')

    if input_text:
        response = bardapi.core.Bard(token).get_answer(input_text)
        response = list(response)  # Convert set to list
        return jsonify({'response': response})
    else:
        return jsonify({'message': 'Please provide the "prompt" parameter.'})

if __name__ == '__main__':
    app.run()
