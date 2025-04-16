from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load the Hugging Face model
generator = pipeline("text-generation", model="paola-md/light-recipes-italian")

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    
    # Try to get ingredients from Dialogflow request
    ingredients = req['queryResult']['queryText']
    
    # Format for model input
    prompt = f"ingredienti: {ingredients}\nricetta:"
    result = generator(prompt, max_length=200, do_sample=True)[0]['generated_text']
    
    recipe = result.split("ricetta:")[-1].strip()

    return jsonify({'fulfillmentText': recipe})

if __name__ == '__main__':
    app.run(port=5000)
