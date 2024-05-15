from flask import Flask, request, jsonify
import requests
from utils import MODEL_URL, DELIMETERS
import json

app = Flask(__name__)

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer <YOUR_API_KEY>'
}

def save_data(topic: str, response):
    filename = topic
    for delimiter in DELIMETERS:
        filename = " ".join(filename.split(delimiter))
    print("Logged into:", filename)
    with open(f"gpt_answer_{'_'.join(filename.split())}.txt", "a") as f:
        f.write(response.json()["choices"][0]["message"]["content"])

@app.route('/get_texts', methods=['POST'])
def get_texts():
    user_data = request.get_json()

    companies = user_data.get('companies', [])
    topics = user_data.get('topics', [])

    if not isinstance(companies, list):
        return jsonify({ "error": "Companies must be a list." }), 400
    for comp in companies:
        for topic in topics:
            input = {
                    "messages":[{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Сгенерируй 3 новостей про {comp}, делай их непоходими друг на друга. Два абзаца на каждую новость, по длиннее но так чтобы вместилось все, стиль деловой, используй конкретные цифры. Учитывай контескт деятельности компании и придумай интересный кейс. Главная тема новости - {topic} Каждую новость начинай с ее номера цифрой. Новости могут быть как негативными так и позитивными."
                        }
                    ]
                }],
                "is_sync": True,
            }
            response = requests.post(MODEL_URL, json=input, headers=headers)

            save_data(topic, response)

    return jsonify('All went right'), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)

@app.route('/get_info', methods=['GET'])
def get_info():
    topic = request.args.get('topic')
    
    if not topic:
        return jsonify({'message': 'Topic parameter is required'}), 400
    
    with open('data.json', 'r') as file:
        data = json.load(file)
    
    if topic in data:
        return jsonify({'topic': topic, 'info': data[topic]})
    else:
        return jsonify({'message': 'Topic not found'}), 404

