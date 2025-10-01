README

# StoryCraft AI

StoryCraft AI is a cross-platform intelligent storywriting application designed to support writers with entity recognition, dynamic profiling, continuity tracking, and emotionally resonant editing tools. It runs on desktop, cloud, web, and mobile environments.

## 🧠 Core Features

- Rich text editor with Markdown and WYSIWYG support

- NLP-based entity recognition and profile generation

- Scene-level continuity engine with fantasy calendar support

- Focused Work Mode with session logging and emotional tone snapshots

- Modular backend with FastAPI and optional Docker containerization

- Plagiarism detection and editorial tone analysis

- Real-time co-authoring and export options (PDF, DOCX, EPUB, HTML)

## 🗂️ File Structure

See the full skeleton in the project root for module breakdowns:

- `main.py`: Editor logic and UI scaffolding

- `entity_rec_profiler/`: Entity recognition and profiling

- `continuity_engine/`: Timeline inference and consistency checks

- `focus_mode/`: Timer canvas, session logger, tone snapshot

- `backend/`: API endpoints and sanitization logic

- `ui_config/`: Layout and theme settings

- `dictionary/`: Word lookup and synonym retrieval

- `reminders/`: Break reminder logic

- `logs/`: Local session metadata

## 🛠️ Development Setup

```bash

# Clone the repo

git clone https://github.com/yourusername/storycraft-ai.git

cd storycraft-ai

# Create virtual environment

python -m venv venv

source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies

pip install -r requirements.txt

# Run the editor

python main.py