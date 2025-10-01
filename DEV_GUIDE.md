# Platogram Developer Guide

## Processing Flow

### Text Files (No Assembly Required)
```bash
# Local files
plato transcript.txt --model anthropic --title --abstract
plato document.json --model anthropic --passages

# Remote text URLs (JSON/TXT/MD)
plato https://example.com/data.json --model anthropic --chapters
```

### Audio Files (Assembly Required)
```bash
# Local audio
plato audio.mp3 --assemblyai-api-key KEY --model anthropic --title

# Remote audio/video URLs
plato https://youtube.com/watch?v=ID --assemblyai-api-key KEY --model anthropic --abstract
plato https://example.com/podcast.mp3 --assemblyai-api-key KEY --model anthropic --passages
```

## Decision Logic

**extract_transcript()** follows this order:

1. **Local Files**: `os.path.exists(url)` → `is_audio_file()` check → ASR or text parsing
2. **Remote URLs**:
   - `.json/.txt/.md` → download as text → parse as transcript
   - Audio/video → download_audio() → ASR transcribe
   - Has subtitles → use existing subtitles

## Installation Options

```bash
# Text-only (lighter)
pip install git+https://github.com/a-shrinked-org/plato-unchained.git

# Full audio support
pip install 'git+https://github.com/a-shrinked-org/plato-unchained.git[asr]'
```

## Chunking

Use `--chunk-size` for large transcripts:
```bash
plato large_file.json --chunk-size 8000 --model anthropic --passages
```

Auto-chunking handles most cases, manual override for performance tuning.

## Key Functions

- `is_audio_file()`: Extension-based audio detection
- `parse_local_transcript_file()`: Multi-format text parsing
- `extract_transcript()`: Unified processing entry point
- Assembly optional via `asr_model` parameter

## Text File Formats Supported

1. `[timestamp_ms] text`
2. `HH:MM:SS text` or `MM:SS text`
3. `timestamp_ms: text`
4. Plain text (auto-assigns 3s intervals)