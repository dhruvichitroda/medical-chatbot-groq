#!/bin/bash
# template.sh — Quick project setup helper

echo "🏥 Medical Chatbot (Groq) — Setup Script"
echo "========================================="

# Create conda environment
echo "📦 Creating conda environment..."
conda create -n medibot python=3.10 -y
conda activate medibot

# Install dependencies
echo "📥 Installing requirements..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete! Next steps:"
echo "  1. Add your API keys to .env file"
echo "  2. Place PDF files in data/ folder"
echo "  3. Run: python store_index.py"
echo "  4. Run: python app.py"
echo "  5. Open: http://localhost:8080"
