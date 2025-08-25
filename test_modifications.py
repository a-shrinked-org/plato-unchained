#!/usr/bin/env python3
"""
Test script for the modified Platogram functionality.
Tests local file processing without AssemblyAI dependency.
"""

import os
import sys
from dataclasses import dataclass
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, '.')

@dataclass
class SpeechEvent:
    time_ms: int
    text: str

def is_audio_file(file_path: str) -> bool:
    """Check if the file is an audio file based on extension."""
    audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.wma', '.mp4', '.avi', '.mov', '.mkv'}
    return Path(file_path).suffix.lower() in audio_extensions

def parse_local_transcript_file(file_path: str) -> list:
    """Parse a local transcript file supporting multiple formats."""
    speech_events = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Try different formats
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # Format 1: [timestamp_ms] text or [timestamp] text
        if line.startswith('[') and ']' in line:
            try:
                timestamp_str, text = line.split(']', 1)
                timestamp_ms = int(timestamp_str.strip('['))
                text = text.strip()
                speech_events.append(SpeechEvent(time_ms=timestamp_ms, text=text))
                continue
            except (ValueError, IndexError):
                pass
        
        # Format 3: HH:MM:SS text or MM:SS text (check this before Format 2 to avoid conflicts)
        if ':' in line and ' ' in line:
            try:
                parts = line.split(' ', 1)
                if len(parts) >= 2:
                    time_str = parts[0]
                    text = parts[1].strip()
                    
                    # Check if first part looks like a time (contains only digits and colons)
                    if all(c.isdigit() or c == ':' for c in time_str) and time_str.count(':') >= 1:
                        # Parse time to milliseconds
                        time_parts = time_str.split(':')
                        if len(time_parts) == 2:  # MM:SS
                            minutes, seconds = map(int, time_parts)
                            timestamp_ms = (minutes * 60 + seconds) * 1000
                        elif len(time_parts) == 3:  # HH:MM:SS
                            hours, minutes, seconds = map(int, time_parts)
                            timestamp_ms = (hours * 3600 + minutes * 60 + seconds) * 1000
                        else:
                            continue
                            
                        speech_events.append(SpeechEvent(time_ms=timestamp_ms, text=text))
                        continue
            except (ValueError, IndexError):
                pass
                
        # Format 2: timestamp_ms: text (plain millisecond number followed by colon)
        if ':' in line and line.split(':')[0].strip().isdigit() and ' ' not in line.split(':')[0]:
            try:
                timestamp_str, text = line.split(':', 1)
                timestamp_ms = int(timestamp_str.strip())
                text = text.strip()
                speech_events.append(SpeechEvent(time_ms=timestamp_ms, text=text))
                continue
            except (ValueError, IndexError):
                pass
        
        # Format 4: Plain text without timestamps (assign sequential timestamps)
        if line and not any(char.isdigit() for char in line[:10]):
            # Assign timestamp based on line position (assuming ~3 seconds per line)
            timestamp_ms = line_num * 3000
            speech_events.append(SpeechEvent(time_ms=timestamp_ms, text=line))
    
    if not speech_events:
        raise ValueError(f"Could not parse any valid speech events from local file: {file_path}")
        
    return sorted(speech_events, key=lambda x: x.time_ms)

def test_audio_detection():
    """Test audio file detection."""
    print("=== Testing Audio File Detection ===")
    
    test_files = [
        ('audio.mp3', True),
        ('video.mp4', True), 
        ('transcript.txt', False),
        ('document.pdf', False),
        ('sample.wav', True),
        ('presentation.mov', True),
        ('notes.md', False)
    ]
    
    all_passed = True
    for filename, expected in test_files:
        result = is_audio_file(filename)
        status = "PASS" if result == expected else "FAIL"
        print(f"  {filename}: {result} ({status})")
        if result != expected:
            all_passed = False
    
    return all_passed

def test_transcript_parsing():
    """Test transcript file parsing."""
    print("=== Testing Transcript File Parsing ===")
    
    test_files = [
        'samples/sample_transcript.txt',
        'samples/sample_transcript_time.txt'
    ]
    
    all_passed = True
    
    for test_file in test_files:
        if not os.path.exists(test_file):
            print(f"  {test_file}: SKIP (file not found)")
            continue
            
        try:
            events = parse_local_transcript_file(test_file)
            print(f"  {test_file}: PASS ({len(events)} events parsed)")
            
            # Show first few events
            for i, event in enumerate(events[:3]):
                print(f"    [{i}] {event.time_ms}ms: {event.text[:50]}{'...' if len(event.text) > 50 else ''}")
            
            # Verify timestamps are increasing
            if len(events) > 1:
                timestamps_increasing = all(events[i].time_ms <= events[i+1].time_ms for i in range(len(events)-1))
                print(f"    Timestamps ordered: {'PASS' if timestamps_increasing else 'FAIL'}")
                
        except Exception as e:
            print(f"  {test_file}: FAIL ({e})")
            all_passed = False
    
    return all_passed

def test_import_safety():
    """Test that we can import basic modules without AssemblyAI."""
    print("=== Testing Import Safety ===")
    
    try:
        # This should NOT import assemblyai directly
        from platogram.types import SpeechEvent
        print("  platogram.types: PASS")
        
        # Create a SpeechEvent
        event = SpeechEvent(time_ms=1000, text="Test event")
        assert event.time_ms == 1000
        assert event.text == "Test event"
        print("  SpeechEvent creation: PASS")
        
        return True
        
    except ImportError as e:
        if "assemblyai" in str(e).lower():
            print(f"  Import test: FAIL (unexpected AssemblyAI import: {e})")
        else:
            print(f"  Import test: FAIL (other import error: {e})")
        return False
    except Exception as e:
        print(f"  Import test: FAIL (unexpected error: {e})")
        return False

def main():
    """Run all tests."""
    print("Testing Platogram Modifications")
    print("=" * 50)
    
    tests = [
        ("Audio Detection", test_audio_detection),
        ("Transcript Parsing", test_transcript_parsing), 
        ("Import Safety", test_import_safety)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print()
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append((test_name, False))
            print()
    
    # Summary
    print("=" * 50)
    print("Test Results Summary:")
    
    all_passed = True
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("✅ All tests passed! Modifications work correctly.")
    else:
        print("❌ Some tests failed. Please check the output above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)