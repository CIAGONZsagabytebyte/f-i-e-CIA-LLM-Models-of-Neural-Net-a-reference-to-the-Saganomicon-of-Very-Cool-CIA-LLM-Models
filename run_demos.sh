#!/bin/bash
# Solarpunk Space Starter Kit - Demo Launcher
# Quick script to run various demos

echo "========================================"
echo "SOLARPUNK SPACE STARTER KIT"
echo "Ring-0 Edition | f(i) = -i | No Neurons"
echo "========================================"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python
if ! command_exists python3 && ! command_exists python; then
    echo "❌ Python not found. Please install Python 3.7+"
    exit 1
fi

PYTHON_CMD="python3"
if ! command_exists python3; then
    PYTHON_CMD="python"
fi

echo "Select a demo to run:"
echo ""
echo "1. Pygame Prototype (Playable 2D Game)"
echo "2. Binary Art Generator (Generate Textures)"
echo "3. Web Demo (Open in Browser)"
echo "4. Install Dependencies"
echo "5. Run All Generators"
echo "0. Exit"
echo ""
read -p "Enter choice [0-5]: " choice

case $choice in
    1)
        echo ""
        echo "🎮 Launching Pygame Prototype..."
        echo "Controls: WASD/Arrows to move, R to restart, ESC to quit"
        echo ""
        $PYTHON_CMD pygame_solarpunk/main.py
        ;;
    2)
        echo ""
        echo "🎨 Generating Binary Art Textures..."
        $PYTHON_CMD binary_art/binary_art.py
        echo ""
        echo "✅ Done! Check binary_art/output/ for generated images"
        ;;
    3)
        echo ""
        echo "🌐 Opening Web Demo..."
        if command_exists xdg-open; then
            xdg-open web_solarpunk/index.html
        elif command_exists open; then
            open web_solarpunk/index.html
        else
            echo "Please open web_solarpunk/index.html in your browser"
        fi
        ;;
    4)
        echo ""
        echo "📦 Installing Python dependencies..."
        $PYTHON_CMD -m pip install -r solarpunk_requirements.txt
        echo ""
        echo "✅ Dependencies installed!"
        ;;
    5)
        echo ""
        echo "🚀 Running all generators..."
        echo ""
        echo "1/1: Binary Art Generator..."
        $PYTHON_CMD binary_art/binary_art.py
        echo ""
        echo "✅ All generators complete!"
        echo "📁 Check binary_art/output/ for generated files"
        ;;
    0)
        echo "Goodbye! 🌿⚡🚀"
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "Thank you for using Solarpunk Space!"
echo "f(i) = -i | Pure Mathematics | No Neurons"
echo "========================================"
