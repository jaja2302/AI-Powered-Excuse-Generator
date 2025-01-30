from flask import Flask, request, jsonify, render_template
import requests
from datetime import datetime

app = Flask(__name__)
OLLAMA_CONFIG = {
    "high_quality": {
        "temperature": 1.2,  # Lebih kreatif
        "top_p": 0.2,
        "num_predict": 70000,
        "num_ctx": 70000,
        "num_gpu": 24,
        "num_thread": 7
    },
    "fast": {
        "temperature": 0.1,
        "top_p": 0.2,
        "num_predict": 35000,
        "num_ctx": 35000,
        "num_gpu": 12,
        "num_thread": 4
    }
}
# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_response(prompt):
    data = {
        "model": "llama3-8b-instruct",
        "prompt": prompt,
        "stream": False,
        "options": OLLAMA_CONFIG["high_quality"]
    }
    response = requests.post(OLLAMA_URL, json=data)
    return response.json()["response"].strip()

def get_question_response(question):
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Anda adalah generator alasan konyol dan absurd. Berikan jawaban kreatif, lucu, dan filosofis maksimal 2 kalimat untuk setiap pertanyaan.
    Jawaban harus mengandung unsur humor dan tidak masuk akal, tapi tetap cerdas dan menghibur.
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    {question}?<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
    return generate_response(prompt)

def get_khodam_response(name, birth):
    birth_date = datetime.strptime(birth, '%Y-%m-%d')
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Anda adalah peramal khodam yang absurd dan lucu. Berikan jawaban kreatif tentang khodam/makhluk halus pelindung seseorang.
    Jawaban harus mengandung: nama khodam yang unik & lucu, kebiasaan aneh khodam tersebut, dan satu pesan konyol dari khodam.
    Format: "🌟 [Nama Khodam] | 👻 [Kebiasaan] | 💌 [Pesan]"
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    Cek khodam untuk {name} (lahir: {birth_date.strftime('%d %B %Y')})
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
    return generate_response(prompt)

def get_jodoh_response(name1, birth1, name2, birth2):
    birth_date1 = datetime.strptime(birth1, '%Y-%m-%d')
    birth_date2 = datetime.strptime(birth2, '%Y-%m-%d')
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Anda adalah peramal cinta yang absurd dan lucu. Berikan ramalan kecocokan pasangan dengan cara yang kreatif dan menghibur.
    Jawaban harus mengandung: persentase kecocokan yang random, alasan absurd kenapa cocok/tidak, dan satu saran konyol.
    Format: "❤️ [Persentase] | 🔮 [Alasan] | 💡 [Saran]"
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    Cek kecocokan antara {name1} (lahir: {birth_date1.strftime('%d %B %Y')}) dengan {name2} (lahir: {birth_date2.strftime('%d %B %Y')})
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
    return generate_response(prompt)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def handle_generate():
    data = request.json
    response_type = data.get('type')
    
    if response_type == 'question':
        response = get_question_response(data.get('question'))
        html_response = f"❓ <strong>{data.get('question')}?</strong><br>🤖 {response}"
    elif response_type == 'khodam':
        response = get_khodam_response(data.get('name'), data.get('birth'))
        html_response = f"👻 <strong>Hasil Pembacaan Khodam untuk {data.get('name')}</strong><br>{response}"
    elif response_type == 'jodoh':
        response = get_jodoh_response(data.get('name1'), data.get('birth1'), 
                                    data.get('name2'), data.get('birth2'))
        html_response = f"❤️ <strong>Hasil Ramalan Jodoh</strong><br>{response}"
    
    return jsonify({"response": html_response})

if __name__ == '__main__':
    app.run(port=5000, debug=True)