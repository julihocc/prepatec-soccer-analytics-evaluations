#!/bin/bash
# Simple conversion script for all question banks
# Usage: ./convert-all.sh

set -e

echo "🎯 Converting question banks to QTI format..."
echo "=============================================="

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Ensure txttoqti is available
if ! command -v txttoqti &> /dev/null; then
    echo "❌ txttoqti not found. Please install: pip install txttoqti>=0.4.0"
    exit 1
fi

# Convert each period
for periodo in periodo-{1,2,3}; do
    if [ -d "$periodo/canvas" ]; then
        # Find the input file
        input_file=$(ls "$periodo/canvas/banco-preguntas-"*.txt 2>/dev/null | head -1)
        output_file="$periodo/canvas/$periodo-qti.zip"
        
        if [ -n "$input_file" ]; then
            echo "📝 Converting $periodo..."
            if txttoqti -i "$input_file" -o "$output_file" 2>/dev/null; then
                echo "   ✅ $output_file created successfully"
            else
                echo "   ❌ Failed to convert $periodo"
                exit 1
            fi
        else
            echo "   ⚠️  No question file found in $periodo/canvas"
        fi
    else
        echo "   ⚠️  Directory $periodo/canvas not found"
    fi
done

echo ""
echo "🎉 All conversions completed successfully!"
echo "📁 QTI files are in each período's canvas directory"