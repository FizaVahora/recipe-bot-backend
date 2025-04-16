from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load the recipe generation model (lightweight and recipe-specific)
generator = pipeline("text2text-generation", model="flax-community/t5-recipe-generation")

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # Extract ingredients from Dialogflow query
    ingredients = req['queryResult']['queryText']

    # Generate recipe using the model
    result = generator(ingredients, max_length=150)[0]['generated_text']

    return jsonify({'fulfillmentText': result})

if __name__ == '__main__':
    app.run(port=5000)


