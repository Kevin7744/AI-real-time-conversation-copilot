from flask import Flask, request, jsonify, render_template
import replicate
import tempfile
import os
from minio import Minio
from keys import MINIO_ACCESS_KEY, MINIO_SECRET_KEY


# MinIO Configuration
minio_access_key = MINIO_ACCESS_KEY
minio_secret_key = MINIO_SECRET_KEY
minio_endpoint = "172.31.53.234:9001"
minio_bucket_name = "voicebots"

# Initialize MinIO client
minio_client = Minio(
    minio_endpoint,
    access_key=minio_access_key,
    secret_key=minio_secret_key,
    secure=False  # Set to True if MinIO server supports HTTPS
)

app = Flask(__name__)
model = replicate

# render html
@app.route("/")
def index():
    return render_template("index.html")

# function to transcript audio using whisper
@app.route("/process-audio", methods=["POST"])
def process_audio_data():
    audio_data = request.files["audio"].read()

    print("Processing audio...")
    # Create a temporary file to save the audio data
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_data)
            temp_audio.flush()

            # Upload to MinIO instead of AWS S3
            minio_client.fput_object(minio_bucket_name, temp_audio.name, temp_audio.name)
            temp_audio_uri = f"http://{minio_endpoint}/{minio_bucket_name}/{temp_audio.name}"

        output = model.run(
            "vaibhavs10/incredibly-fast-whisper:3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c",
            input={
                "task": "transcribe",
                "audio": temp_audio_uri,
                "language": "english",
                "timestamp": "chunk",
                "batch_size": 64,
                "diarise_audio": False,
            },
        )

        print(output)
        results = output["text"]

        return jsonify({"transcript": results})
    except Exception as e:
        print(f"Error running Replicate model: {e}")
        return None

# function to generate suggestion using mixtral
@app.route("/get-suggestion", methods=["POST"])
def get_suggestion():
    print("Getting suggestion...")
    data = request.get_json()  # Parse JSON data from the request
    transcript = data.get("transcript", "")  # Extract transcript
    prompt_text = data.get("prompt", "")  # Extract prompt text

    prompt = f"""
    {transcript}
    ------
    {prompt_text}
    """

    suggestion = ""
    for event in model.stream(
        "mistralai/mistral-7b-instruct-v0.2",
        input={
            "debug": False,
            "top_k": 50,
            "top_p": 0.9,
            "prompt": prompt,
            "temperature": 0.6,
            "max_new_tokens": 512,
            "min_new_tokens": -1,
            "prompt_template": "<s>[INST] {prompt} [/INST] ",
            "repetition_penalty": 1.15,
        },
    ):
        suggestion += str(event)  # Accumulate the output

    return jsonify({"suggestion": suggestion})  # Send as JSON response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
