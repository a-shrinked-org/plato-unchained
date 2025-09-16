# Platogram: Transform Audio into Knowledge
*Plato on drugs*

Platogram is an open-source project that converts audio content into structured, readable essays with embedded references. It's designed to help researchers, content creators, and knowledge workers extract valuable insights from audio sources like lectures, podcasts, and interviews.

## Key Features

- Convert audio from YouTube, local files, etc into well-structured text.
- **Process local transcript files** without external dependencies.
- **Handle large audio files** - optimized for hour+ recordings without token limits.
- Create passages, summaries, and titles from audio content.
- Maintain references to the original transcript and timestamps.
- Create a searchable knowledge base from processed audio.
- Use the generated content for further AI-powered analysis and content creation.
- **Optional AssemblyAI integration** - use only what you need.

## Getting Started

<a target="_blank" href="https://colab.research.google.com/github/code-anyway/platogram/blob/main/notebooks/quick_start.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

### Prerequisites

- Access to Anthropic's Claude API (required)
- Assembly AI API access (optional, for transcription)
- Python 3.10+
- FFmpeg (optional, for transcription)

### Installation

#### Basic Installation (transcript files only)
```bash
pip install .
```

#### Full Installation (with audio file support)
```bash
pip install .[asr]
```

Or from git:
```bash
pip install git+https://github.com/code-anyway/platogram.git
```

## Basic Usage

### Command Line Interface (CLI)

#### Process YouTube/Web Content
Obtain your API keys for Anthropic and AssemblyAI. Provide a URL to audio source.

```bash
plato \
--anthropic-api-key "YOUR_ANTHROPIC_API_KEY" \
--assemblyai-api-key "YOUR_ASSEMBLYAI_API_KEY" \
https://www.youtube.com/shorts/XsLK3tPy9SI
```

#### Process Local Files (No ASR needed)
```bash
# Process transcript files
plato transcript.txt --title --abstract

# Process markdown documents
plato document.md --chapters --passages

# Multiple formats supported:
# [0] Text with millisecond timestamps
# 00:00 Text with time format
# Plain text without timestamps
# Markdown files with headers
```

#### Process Audio Files (Requires ASR)
```bash
plato audio.mp3 --assemblyai-api-key "YOUR_ASSEMBLYAI_API_KEY"
```

#### Process via Inputs File
You can also pass a text file with many inputs (one per line; lines starting with `#` are ignored):

```bash
plato \
--anthropic-api-key "YOUR_ANTHROPIC_API_KEY" \
--assemblyai-api-key "YOUR_ASSEMBLYAI_API_KEY" \
--inputs-file inputs.txt
```

See [LOCAL_FILES.md](LOCAL_FILES.md) for detailed format specifications and examples.

### Python SDK

```python
import platogram as plato


# Initialize models
llm = plato.llm.get_model("anthropic/claude-3-5-sonnet", "YOUR_ANTHROPIC_API_KEY")
asr = plato.asr.get_model("assembly-ai/best", "YOUR_ASSEMBLYAI_API_KEY")  # Optional

# Process audio
url = "https://www.youtube.com/shorts/XsLK3tPy9SI"
transcript = plato.extract_transcript(url, asr)
content = plato.index(transcript, llm)

# Access generated content
print(content.title)
print(content.summary)

for passage in content.passages:
    print(passage)
```

## Use Cases

- Create searchable archives of lectures or conference talks
- Generate blog posts or articles from podcast episodes
- Extract key insights from interviews or meetings
- Build a personal knowledge base from audio content
- Enhance learning by converting lectures into structured notes

## Acknowledgments

- Uses transcript and text of Chapter 1: Atoms in Motions from Feynman Lectures on Physics, [Copyright © 1963-1965, 2006, 2013 by the California Institute of Technology, Michael A. Gottlieb and Rudolf Pfeiffer](https://www.feynmanlectures.caltech.edu/III_copyright.html)

## Feedback and Support

We're actively seeking feedback to improve Platogram. For questions, suggestions, or issues, please contact us at [platogram@codeanyway.com](mailto:platogram@codeanyway.com) or open an issue on GitHub.

Start transforming your audio content into valuable, structured knowledge today with Platogram!

## Copyright and License

Copyright (c) 2023-2024 Code Anyway, Inc.
https://codeanyway.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
