from flask import Flask
from flask import render_template
from flask import request ,jsonify
from main import getQAChain,retriever
from flask_cors import CORS

app=Flask(__name__)
CORS(app)
@app.route('/home')
def home():
    return render_template('chat.html')

@app.route('/retrieve')
def retrieve():
    return render_template('retrieve.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    question=request.form.get('msg')
    chain=getQAChain(question)
    response =chain["answer"]
    return str(response)
    
@app.route('/gets', methods=["GET", 'POST'])
def get_response():
    question = request.form.get('msg')
    response = retriever(question)
    return str(response)



@app.route('/',methods=["POST"])
def chatai():
    question=request.get_json()
    query = question["query"]
    chain=getQAChain(query)
    response =chain["answer"]
    return jsonify({"answer":response})

if __name__=="__main__" :
    app.run(host="0.0.0.0",port=3000 ,debug=False)