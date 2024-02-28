# Conversation Copilot

## Overview

Conversation Copilot is a Flask-based web application designed to assist users during interviews or conversations by providing real-time transcriptions and suggestions. The application leverages advanced AI models for audio transcription and generating contextually relevant suggestions to enhance the conversation flow. It's particularly useful for scenarios like user interviews, where capturing detailed responses and generating insightful follow-up questions can significantly impact the quality of the conversation.

## Features

- **Audio Recording**: Users can record their conversations directly through the web interface.
- **Real-time Transcription**: The application transcribes audio input in real-time, providing immediate text output of the conversation.
- **Intelligent Suggestions**: Based on the transcribed text and a user-defined prompt, the application generates suggestions or follow-up questions to guide the conversation.

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **AI Models**: Replicate for transcription, Mistral for generating suggestions
- **Storage**: MinIO S3-compatible storage for audio files

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Flask
- MinIO Server (for S3-compatible storage)
- Replicate and Mistral API access

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/kevin7744/conversation-copilot.git
   cd conversation-copilot
   ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    ```For Windows (PowerShell):
    $env:MINIO_ACCESS_KEY="your_minio_access_key"
    $env:MINIO_SECRET_KEY="your_minio_secret_key"
    $env:REPLICATE_API_TOKEN="your_replicate_api_token"

    For Unix/Linux:
    export MINIO_ACCESS_KEY="your_minio_access_key"
    export MINIO_SECRET_KEY="your_minio_secret_key"
    export REPLICATE_API_TOKEN="your_replicate_api_token"
    ```

4. Start the Flask application:
    ```
    flask run
    ```

The application will be available at http://127.0.0.1:5000/.

