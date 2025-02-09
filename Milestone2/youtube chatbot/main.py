from flask import Flask, render_template, request, jsonify
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

# Function to get YouTube transcript
def get_video_transcript(video_url):
    video_id = re.search(r"(?<=v=)[^&]+", video_url).group(0)
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = SRTFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        return formatted_transcript
    except Exception as e:
        return str(e)

# Initialize ChatBot
chatbot = ChatBot('YouTubeAssistant')

# Train the chatbot with the ChatterBot corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["message"]

    # If user inputs a YouTube URL
    if "http" in user_input and "youtube.com" in user_input:
        transcript = get_video_transcript(user_input)
        return jsonify({"response": f"Here's the video content:\n{transcript[:1000]}..."})  # Limit output
    else:
        response = chatbot.get_response(user_input)
        return jsonify({"response": str(response)})

if __name__ == "__main__":
    app.run(debug=True)
