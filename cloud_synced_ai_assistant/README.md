# Cloud-Synced AI Personal Assistant

Local + cloud-connected assistant to take voice or text commands, detect intent, and sync notes/events across Notion, Obsidian, and Google Calendar. Optional Streamlit UI.

## Features
- Voice input (SpeechRecognition + PyAudio) and voice feedback (pyttsx3)
- Intent recognition (keyword-based)
- Notion: add page to a database
- Obsidian: write Markdown notes to a vault folder
- Google Calendar: create events with OAuth
- Local action history logging
- Streamlit micro-frontend
- Dockerfile for containerization (UI)

## Project Structure
```
cloud_synced_ai_assistant/
├── main.py
├── config.py
├── notion_module.py
├── obsidian_module.py
├── calendar_module.py
├── voice_module.py
├── intent_module.py
├── requirements.txt
├── README.md
├── Dockerfile
├── app.py
└── assets/
    └── screenshots/
```

## Prerequisites
- Python 3.10+
- Windows: Ensure microphone works; install PyAudio wheels if needed
- Notion: create integration and share a database with it
- Google: create OAuth "Desktop App" credentials
- Optional: Docker Desktop for container run (Streamlit UI)

## Configuration
Create a `.env` in `cloud_synced_ai_assistant/` or set environment variables.

```
APP_NAME=Cloud-Synced AI Assistant
DEFAULT_TIMEZONE=UTC
STREAMLIT_PORT=8501

# Notion
NOTION_API_KEY=secret_xxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Obsidian
OBSIDIAN_VAULT_PATH=C:\\Users\\<you>\\Obsidian Vault

# Google
GOOGLE_CALENDAR_ID=primary
GOOGLE_CREDENTIALS_FILE=./credentials.json
GOOGLE_TOKEN_FILE=./token.json

# Features
VOICE_INPUT_ENABLED=true
VOICE_FEEDBACK_ENABLED=true
```

Place `credentials.json` (Google OAuth client secret) in the project folder. The first run will generate `token.json` after browser consent.

## Install and Run (CLI)
```
# from project root
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt

# Optional: place .env and credentials.json
python main.py
```
- Speak a command or type when prompted.
- Examples:
  - "Add a note to Notion about meeting ideas"
  - "Write this in Obsidian: brainstorm project"
  - "Add meeting at 5 pm tomorrow"

## Streamlit UI
```
.venv\\Scripts\\activate
streamlit run app.py --server.port=8501
```
Open http://localhost:8501

## Docker (Streamlit UI)
The image includes audio deps, but microphone inside containers is limited; use text UI in container.
```
docker build -t ai-assistant:latest .
docker run -p 8501:8501 --name ai-assistant ai-assistant:latest
```

## AWS Deployment Notes
- EC2: run the Docker image on a small instance (t3.small+), behind an ALB or NLB. Store secrets in SSM Parameter Store or Secrets Manager.
- Lambda: suitable for API-based interactions (Streamlit not supported). Extract core logic into AWS Lambda handler and use API Gateway. Use layers for dependencies.
- ECS Fargate: run the Streamlit container; attach to ALB; store secrets via task definition + SSM.
- Observability: send logs to CloudWatch; use structured logs if extending.

## Troubleshooting
- PyAudio install on Windows: use prebuilt wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio or `pip install PyAudio` with Build Tools.
- Notion: ensure the integration is added to the target database (Share → Add connections).
- Google: if token issues, delete `token.json` and re-run to re-consent.
- Obsidian: verify `OBSIDIAN_VAULT_PATH` exists and is accessible.

## Security
- Do not commit credentials.json or token.json.
- Use Secrets Manager/SSM for cloud deployments.

## Roadmap
- Replace keyword intents with LLM-based parser.
- Add unit tests and pre-commit.
- Add OpenTelemetry and structured logging schema.

## License
MIT

## Streamlit Cloud Deployment

Deploy the Streamlit UI (`app.py`) to Streamlit Community Cloud.

1. Push this project to a GitHub repository.
2. In Streamlit Cloud, create a new app pointing to `app.py` (main branch).
3. Configure Secrets (Settings → Secrets) using the example file:
   - See `.streamlit/secrets.example.toml` and paste values into the Secrets editor.
   - Required at minimum:
     - `NOTION_API_KEY`
     - `NOTION_DATABASE_ID`
     - `GOOGLE_CREDENTIALS_JSON` (full JSON from your Desktop OAuth client)
     - Optional: `GOOGLE_TOKEN_JSON` (paste after first local OAuth run)
     - Set `VOICE_INPUT_ENABLED="false"` and `VOICE_FEEDBACK_ENABLED="false"` on Streamlit Cloud.
4. No additional requirements needed—`requirements.txt` is used automatically.
5. First-time Google OAuth:
   - Streamlit Cloud cannot run the local browser OAuth flow. Do one of the following:
     - Run locally once to generate `token.json`, then open it and paste its content into Streamlit secrets as `GOOGLE_TOKEN_JSON`.
     - Or pre-generate a refreshable token using your OAuth credentials off-platform and paste as `GOOGLE_TOKEN_JSON`.
6. Notion:
   - Ensure your Notion integration is added to the database. The title property must be named `Name`.

Notes:
- On Streamlit Cloud, mic input is disabled; use the text UI. TTS is disabled by secrets defaults.
- Google OAuth files are written at runtime from secrets; nothing is committed to the repo.
