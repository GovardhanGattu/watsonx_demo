from flask import Flask, render_template, request
from main import getQAChain
app = Flask(__name__)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/answer', methods=["GET","POST"])
def answer_question():
    question = request.form.get('question')
    print(question)

    chain = getQAChain(question)
    print(chain["answer"])
    
    return render_template('index.html',response=chain["answer"])

if __name__ == '__main__':
    app.run(debug=True)   
