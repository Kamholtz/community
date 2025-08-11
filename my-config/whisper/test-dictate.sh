#!/bin/bash
# Simple test script to debug dictation pipeline

MODEL="$HOME/.local/share/whisper/models/ggml-small.en.bin"
if [ ! -f "$MODEL" ]; then
    echo "Model not found: $MODEL" >&2
    exit 1
fi

echo "Testing dictation pipeline..."
echo "Speak into your microphone now:"

# Test with direct output first
whisper-stream -m "$MODEL" -t "$(nproc)" -c 1 | while IFS= read -r line; do
    echo "Raw output: '$line'"
    
    # Clean the line
    cleaned=$(echo "$line" | sed -E 's/^\[[^]]+\]\s*//')
    echo "Cleaned: '$cleaned'"
    
    # Skip empty lines
    if [ -z "${cleaned// }" ]; then
        echo "Skipping empty line"
        continue
    fi
    
    echo "Processing: '$cleaned'"
    
    # Try clipboard
    printf '%s ' "$cleaned" | xclip -selection clipboard
    echo "Copied to clipboard: '$cleaned'"
    
    # Check clipboard
    clipcontent=$(xclip -selection clipboard -o)
    echo "Clipboard contains: '$clipcontent'"
    
    # Try paste
    echo "Attempting paste..."
    xdotool key --clearmodifiers ctrl+v
    
    sleep 0.5
done