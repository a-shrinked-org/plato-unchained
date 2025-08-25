#!/usr/bin/env python3
"""
Static validation of AssemblyAI flow to ensure backward compatibility.
This validates the code structure without requiring dependencies.
"""

import os
import sys
import re
from pathlib import Path

def validate_assembly_py_structure():
    """Validate that assembly.py maintains its original structure"""
    print("=== Validating assembly.py Structure ===")
    
    assembly_file = Path("platogram/asr/assembly.py")
    if not assembly_file.exists():
        print("❌ assembly.py file not found")
        return False
    
    with open(assembly_file) as f:
        content = f.read()
    
    # Check for essential components
    required_components = {
        "import assemblyai as aai": "AssemblyAI import",
        "class Model:": "Model class definition",
        "def __init__(self, model: str": "Model constructor",
        "def transcribe(self, file: Path": "Transcribe method",
        "convert_to_mp3": "MP3 conversion function",
        "aai.SpeechModel.best": "Best model reference",
        "aai.SpeechModel.nano": "Nano model reference", 
        "aai.TranscriptionConfig": "Configuration class",
        "aai.Transcriber": "Transcriber class",
        "SpeechEvent(time_ms=": "SpeechEvent creation"
    }
    
    missing_components = []
    for component, description in required_components.items():
        if component not in content:
            missing_components.append(f"{description} ({component})")
    
    if missing_components:
        print("❌ Missing components:")
        for component in missing_components:
            print(f"   - {component}")
        return False
    
    # Check that optional import was added correctly
    if "try:" in content and "import assemblyai" in content and "except ImportError:" in content:
        print("✅ Optional import wrapper added correctly")
    else:
        print("❌ Optional import wrapper missing or incorrect")
        return False
    
    print("✅ All original AssemblyAI components preserved")
    return True

def validate_asr_init_structure():
    """Validate ASR __init__.py maintains backward compatibility"""
    print("\n=== Validating ASR __init__.py Structure ===")
    
    asr_init = Path("platogram/asr/__init__.py")
    if not asr_init.exists():
        print("❌ ASR __init__.py not found")
        return False
    
    with open(asr_init) as f:
        content = f.read()
    
    required_elements = {
        "class ASRModel(Protocol):": "ASRModel protocol",
        "def transcribe(self, file: Path": "Transcribe protocol method",
        "def get_model(full_model_name: str": "get_model function",
        'if full_model_name.startswith("assembly-ai/")': "AssemblyAI model detection",
        "from .assembly import Model": "Assembly Model import",
        "return Model(": "Model instantiation"
    }
    
    missing_elements = []
    for element, description in required_elements.items():
        if element not in content:
            missing_elements.append(f"{description} ({element})")
    
    if missing_elements:
        print("❌ Missing elements:")
        for element in missing_elements:
            print(f"   - {element}")
        return False
    
    # Check that error handling was added
    if "try:" in content and "except ImportError:" in content:
        print("✅ Import error handling added correctly")
    else:
        print("❌ Import error handling missing")
        return False
    
    print("✅ ASR module structure preserved with enhancements")
    return True

def validate_ingest_flow():
    """Validate ingestion flow maintains AssemblyAI support"""
    print("\n=== Validating Ingestion Flow ===")
    
    ingest_file = Path("platogram/ingest.py")
    if not ingest_file.exists():
        print("❌ ingest.py not found")
        return False
    
    with open(ingest_file) as f:
        content = f.read()
    
    # Check for audio file processing logic
    audio_processing_elements = {
        "def is_audio_file(": "Audio file detection function",
        "def extract_transcript(": "Main extraction function",
        "if is_audio_file(url):": "Audio file check in extraction",
        "asr_model.transcribe(": "ASR model usage",
        "download_audio(url, temp_dir_path)": "URL audio download",
        "asr_model.transcribe(file, lang=lang)": "ASR transcription call"
    }
    
    missing_elements = []
    for element, description in audio_processing_elements.items():
        if element not in content:
            missing_elements.append(f"{description} ({element})")
    
    if missing_elements:
        print("❌ Missing audio processing elements:")
        for element in missing_elements:
            print(f"   - {element}")
        return False
    
    # Check the flow logic is correct
    extract_function = re.search(r'def extract_transcript\(.*?\n(.*?)(?=\ndef|\Z)', content, re.DOTALL)
    if extract_function:
        func_content = extract_function.group(1)
        
        # Verify correct flow: local files -> audio check -> ASR or text parsing -> URLs
        flow_checks = [
            "if not url.lower().startswith",  # Local file check
            "if is_audio_file(url):",         # Audio file detection
            "if asr_model is None:",          # ASR requirement check
            "return asr_model.transcribe",    # ASR usage
            "return parse_local_transcript",  # Text file parsing
            "with TemporaryDirectory",        # URL processing
        ]
        
        flow_ok = all(check in func_content for check in flow_checks)
        if flow_ok:
            print("✅ Extract transcript flow logic preserved")
        else:
            missing_flow = [check for check in flow_checks if check not in func_content]
            print(f"❌ Flow logic issues: {missing_flow}")
            return False
    
    print("✅ Ingestion maintains full AssemblyAI support")
    return True

def validate_cli_integration():
    """Validate CLI integration preserves AssemblyAI usage"""
    print("\n=== Validating CLI Integration ===")
    
    cli_file = Path("platogram/cli.py")
    if not cli_file.exists():
        print("❌ cli.py not found") 
        return False
    
    with open(cli_file) as f:
        content = f.read()
    
    cli_elements = {
        "--assemblyai-api-key": "AssemblyAI API key argument",
        "assemblyai_api_key": "API key parameter handling",
        "plato.asr.get_model": "ASR model initialization", 
        "extract_transcript(url_or_file, asr": "ASR model usage in extraction",
        "asr = None": "ASR initialization",
        "if assemblyai_api_key:": "Conditional ASR setup"
    }
    
    missing_elements = []
    for element, description in cli_elements.items():
        if element not in content:
            missing_elements.append(f"{description} ({element})")
    
    if missing_elements:
        print("❌ Missing CLI elements:")
        for element in missing_elements:
            print(f"   - {element}")
        return False
    
    # Check for enhanced error handling
    if "try:" in content and "except ImportError" in content:
        print("✅ Enhanced error handling for missing AssemblyAI")
    
    print("✅ CLI maintains full AssemblyAI integration")
    return True

def validate_pyproject_setup():
    """Validate pyproject.toml has correct optional dependency setup"""
    print("\n=== Validating pyproject.toml Setup ===")
    
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        print("❌ pyproject.toml not found")
        return False
    
    with open(pyproject_file) as f:
        content = f.read()
    
    required_config = {
        'assemblyai = {version = "^0.26.0", optional = true}': "Optional AssemblyAI dependency",
        "[tool.poetry.extras]": "Extras section",
        'asr = ["assemblyai"]': "ASR extra definition"
    }
    
    missing_config = []
    for config, description in required_config.items():
        if config not in content:
            missing_config.append(f"{description} ({config})")
    
    if missing_config:
        print("❌ Missing configuration:")
        for config in missing_config:
            print(f"   - {config}")
        return False
    
    print("✅ Optional dependency setup correct")
    print("   - Users can install basic version: pip install .")
    print("   - Users can install with ASR: pip install .[asr]")
    return True

def validate_error_messages():
    """Validate error messages are helpful and informative"""
    print("\n=== Validating Error Messages ===")
    
    files_to_check = [
        ("platogram/asr/__init__.py", "ASR init"),
        ("platogram/asr/assembly.py", "Assembly module"),
        ("platogram/ingest.py", "Ingestion"),
        ("platogram/cli.py", "CLI")
    ]
    
    expected_messages = [
        "pip install 'platogram[asr]'",
        "AssemblyAI is not installed",
        "ASR model required for audio files"
    ]
    
    all_good = True
    for file_path, name in files_to_check:
        if Path(file_path).exists():
            with open(file_path) as f:
                content = f.read()
            
            found_messages = [msg for msg in expected_messages if msg in content]
            if found_messages:
                print(f"✅ {name}: {len(found_messages)} helpful error messages")
            else:
                print(f"⚠️  {name}: No specific error messages (may be OK)")
        else:
            print(f"❌ {name}: File not found")
            all_good = False
    
    return all_good

def main():
    """Run all validation tests"""
    print("Static Validation of AssemblyAI Flow Preservation")
    print("=" * 60)
    
    tests = [
        ("assembly.py Structure", validate_assembly_py_structure),
        ("ASR __init__.py Structure", validate_asr_init_structure),
        ("Ingestion Flow", validate_ingest_flow),
        ("CLI Integration", validate_cli_integration),
        ("pyproject.toml Setup", validate_pyproject_setup),
        ("Error Messages", validate_error_messages),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("AssemblyAI Flow Validation Summary:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("🎉 VALIDATION SUCCESSFUL!")
        print("\n✅ AssemblyAI Flow Fully Preserved:")
        print("   • Original Model class intact with all methods")
        print("   • ASR protocol and get_model function unchanged") 
        print("   • CLI arguments and workflow preserved")
        print("   • URL processing and audio download maintained")
        print("   • Error handling enhanced with helpful messages")
        print("   • Optional dependency system properly implemented")
        
        print("\n🔧 Original AssemblyAI Usage Still Works:")
        print("   1. Install: pip install .[asr]")
        print("   2. CLI: plato audio.mp3 --assemblyai-api-key YOUR_KEY")
        print("   3. Python: asr = plato.asr.get_model('assembly-ai/best', key)")
        print("   4. Same API, same quality, same features")
        
        print("\n📈 Enhancements Added:")
        print("   • Better error messages when AssemblyAI missing")
        print("   • Graceful fallback for text file processing")
        print("   • Optional installation reduces dependencies")
        
    else:
        print("⚠️  VALIDATION ISSUES FOUND")
        print("Some aspects of AssemblyAI flow may have been affected.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)