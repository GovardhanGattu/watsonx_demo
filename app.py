from flask import Flask
from flask import render_template
from flask import request,jsonify
from src.incident_analyser import getQAChain,retriever
from src.procurement import procurement_retriever,procurement_chain
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

# Application end points for incident analyser use case - start

@app.route('/incidents')
def incidents_home():
    return render_template('incidentschat.html')

@app.route('/retrieveincidentdocs')
def incidents_retrieve():
    return render_template('incidentsretrieve.html')

@app.route("/reply", methods=["GET", "POST"])
def incidents_chat():
    question=request.form.get('msg')
    print(question)
    chain=getQAChain(question)
    response =chain["answer"]
    return str(response)
    
@app.route('/generate', methods=["GET", 'POST'])
def incidents_response():
    question = request.form.get('msg')
    response = retriever(question)
    print(response)
    return str(response)

@app.route('/chat',methods=["POST"])
def incidents_answer():
    question=request.get_json()
    query = question["query"]
    print(query)
    chain=getQAChain(query)
    response =chain["answer"]
    return jsonify({"answer":response})

# Application end points for incident analyser use case - End


# Application end points for procurement use case - start

@app.route('/procurement')
def procurement_home():
    return render_template('procurementchat.html')

@app.route('/retrieveprocurementdocs')
def procurement_retrieve():
    return render_template('procurementretrieve.html')

@app.route("/analyse", methods=["GET", "POST"])
def procurement_chat():
    question=request.form.get('msg')
    print(question)
    chain=procurement_chain(question)
    response =chain["answer"]
    return str(response)
    
@app.route('/analysedoc', methods=["GET", 'POST'])
def procurement_response():
    question = request.form.get('msg')
    response = procurement_retriever(question)
    print(response)
    return str(response)

@app.route('/insights',methods=["POST"])
def procurement_answer():
    question=request.get_json()
    query = question["query"]
    print(query)
    chain=procurement_chain(query)
    response =chain["answer"]
    return jsonify({"answer":response})

# Application end points for procurement use case - End



if __name__=="__main__" :
    app.run(host="0.0.0.0",port=3000 ,debug=True)