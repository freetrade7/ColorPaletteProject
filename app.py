import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json

config = dotenv_values('.env');
openai.api_key = config["OPENAI_API_KEY"]


app = Flask(__name__,
    template_folder='templates',
    static_url_path='', 
    static_folder='static'
)

def get_colors(msg):
    prompt = f"""
    You are a color palette generator.
    The palettes should be between 2 and 8 colors.

    Desired Format: pure JSON array of hexadecimal color codes without any additional words.

    Text: {msg} 
    Answer:
    """

    response = openai.Completion.create(
        prompt=prompt,
        model="text-davinci-003",
        max_tokens=200,
    )

    colors = json.loads(response["choices"][0]["text"])
    return colors

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}
    

@app.route("/")
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)
