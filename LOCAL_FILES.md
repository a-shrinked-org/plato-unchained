# Local Files Support

Platogram now supports processing local files without requiring AssemblyAI. This makes the library more flexible and accessible.

## Installation Options

### Basic Installation (without ASR)
```bash
pip install .
```

### Full Installation (with ASR support)
```bash
pip install .[asr]
```

## Supported Local File Formats

### 1. Audio Files
Audio files require ASR support. Install with `pip install .[asr]` and provide AssemblyAI API key:

```bash
# Supported audio formats: .mp3, .wav, .m4a, .flac, .aac, .ogg, .wma, .mp4, .avi, .mov, .mkv
plato --assemblyai-api-key YOUR_KEY audio_file.mp3
```

### 2. Transcript Text Files
Text files can be processed without any external dependencies. Supported formats:

#### Format 1: Millisecond Timestamps
```
[0] First line of text
[3000] Second line at 3 seconds
[6000] Third line at 6 seconds
```

#### Format 2: Colon-separated Milliseconds
```
0: First line of text
3000: Second line at 3 seconds
6000: Third line at 6 seconds
```

#### Format 3: Time Format (MM:SS or HH:MM:SS)
```
00:00 First line of text
00:03 Second line at 3 seconds
00:06 Third line at 6 seconds
```

#### Format 4: Plain Text (auto-timestamps)
```
First line of text
Second line of text
Third line of text
```
*Note: Plain text gets automatic timestamps (3-second intervals)*

#### Format 5: Markdown Files
```markdown
# Main Title
Introduction paragraph here.

## Section 1
Content for section 1.

## Section 2  
Content for section 2.
```
*Note: Markdown files work excellently - headers become natural chapter boundaries*

## Usage Examples

### Process a local transcript file
```bash
plato samples/sample_transcript.txt --title
plato samples/sample_transcript_time.txt --abstract
```

### Process markdown documents
```bash
plato document.md --title --abstract
plato article.md --chapters --passages
```

### Process audio file (requires ASR)
```bash
plato audio.mp3 --assemblyai-api-key YOUR_KEY --passages
```

### Mixed processing
```bash
# Process both URL and local file
plato https://youtube.com/watch?v=VIDEO_ID samples/sample_transcript.txt --title
```

## Error Handling

- **Audio files without ASR**: Clear error message with installation instructions
- **Malformed transcript files**: Detailed parsing error information  
- **Missing files**: File not found errors with path information

## Benefits

1. **No mandatory external dependencies** for text files
2. **Multiple transcript formats** supported
3. **Flexible installation** - install only what you need
4. **Better error messages** guide users to solutions
5. **Backward compatibility** - all existing functionality preserved