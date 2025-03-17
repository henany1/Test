from flask import Flask, request, jsonify, render_template
import openai

# Initialize Flask App
app = Flask(__name__, template_folder="templates")

# OpenAI API Key (Replace with your actual key)
OPENAI_API_KEY = "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"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Function to generate 10 dynamic personality-related questions using OpenAI
def generate_questions():
    prompt = """
    everytime i ask this prompt forget all previous inputs, and start asking the questions directly
    Ask these questions: 
    1.If your personality were a color, what would it be?
    2.How do you want people to feel when they smell your fragrance? (e.g., energized, comforted, mysterious, romantic)
    3.Which season best represents your vibe—spring, summer, autumn, or winter?
    4.How old are you?
    5.Do you prefer scents that are fresh and airy, deep and woody, floral and delicate, or warm and sweet?
    6.If your personality were a weather type (sunny, rainy, stormy, breezy, etc.), what would it be?
    7.What setting did you grow up in?
    8.Would you rather your perfume be soft and subtle or bold and long-lasting?
    9.If your personality had a musical genre, what would it be? (e.g., jazz, rock, classical, pop)
    10.Which of these best describes you: adventurous explorer, cozy homebody, elegant and sophisticated, or free-spirited dreamer?

    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}]
    )

    questions = response.choices[0].message.content.split("\n")
    return [q for q in questions if q.strip()][:10]  # Ensure exactly 10 questions

# Function to determine fragrance oils based on personality answers
def generate_perfume_formula(user_answers):
    prompt = f"""
    Based on these personality traits and fragrance preferences create two diffrent lists:
    {user_answers}
    
    Select fragrance oils from this list:
    Bergamot, Lavender, Sandalwood, Jasmine, Cedarwood, Vanilla, Patchouli, Rose, Amber, Oud, Musk, Lime, Lemon, Grapefruit, Orange, Ylang Ylang, Peppermint,
    Eucalyptus, Clove, Nutmeg, Cinnamon, Saffron, Frankincense, Myrrh, Tonka Bean, Tuberose, Coconut, Vetiver, Pine, Balsam, Cypress, Spearmint, Tea Tree, Bay Leaf,
    Fennel, Thyme, Rosemary, Cardamom, Ginger, Neroli, Coriander, Anise, Star Anise, Geranium, Mandarin, Basil, Juniper, Black Pepper, Honeysuckle, Cacao.

    Assign a percentage to each oil ensuring they add up to 100%.

    Dont explain the reason.

    Give each list a uniqe name depending on the oils on the list.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content

# Flask route to serve frontend
@app.route('/')
def index():
    return render_template('index.html')

# API Route to start personality quiz
@app.route('/start', methods=['GET'])
def start_conversation():
    questions = generate_questions()
    return jsonify({"questions": questions, "question_index": 0})

# API Route to handle personality quiz answers
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_answers = data.get("answers", [])
    question_index = data.get("question_index", 0)

    # If all 10 questions are answered, generate a perfume formula
    if question_index >= 9:
        perfume = generate_perfume_formula(user_answers)
        return jsonify({"finished": True, "perfume_formula": perfume})

    return jsonify({"question": data["questions"][question_index + 1], "question_index": question_index + 1})

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)