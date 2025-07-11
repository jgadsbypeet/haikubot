from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/haiku', methods=['POST'])
def haiku():
    user_input = request.form.get('text') or "life, the universe, and everything"

    prompt = (
        "Write a haiku (5-7-5) that reflects progressive values like empathy, justice, or inclusion. "
        f"Use this idea as inspiration:\n\n{user_input}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    haiku = response.choices[0].message.content.strip()

    return jsonify({
        "response_type": "in_channel",
        "text": f"🌸 *Your haiku:*\n{haiku}"
    })

if __name__ == '__main__':
    app.run(port=5000)
