#!/bin/bash

# Setup script for Small Business Marketing Tool
# This script sets up the development environment

set -e  # Exit on error

echo "🚀 Setting up Small Business Marketing Tool..."
echo ""

# Check Python version
echo "📦 Checking Python version..."
python3 --version

# Check Node.js version
echo "📦 Checking Node.js version..."
node --version

echo ""
echo "🔧 Setting up backend..."

# Backend setup
cd backend

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
OPENAI_API_KEY=sk-your-key-here
FLASK_ENV=development
PORT=5001
EOF
    echo "⚠️  Please edit backend/.env and add your OPENAI_API_KEY"
else
    echo "✅ .env file already exists"
fi

cd ..

echo ""
echo "🔧 Setting up frontend..."

# Frontend setup
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your OPENAI_API_KEY"
echo "2. Start backend: cd backend && source venv/bin/activate && python3 app.py"
echo "3. Start frontend: cd frontend && npm start"
echo ""
echo "Backend will run on http://localhost:5001"
echo "Frontend will run on http://localhost:3001"

