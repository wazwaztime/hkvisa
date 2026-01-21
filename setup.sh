#!/bin/bash
# Setup script for HK Visa Appointment Checker

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Hong Kong Visa Appointment Checker - Setup              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
if ! python3 --version; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi
echo "✓ Python 3 found"
echo ""

# Install dependencies
echo "Installing dependencies..."
if ! pip3 install -r requirements.txt; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

# Setup configuration
if [ ! -f "config.env" ]; then
    echo "Creating config.env from example..."
    cp config.example.env config.env
    echo "✓ Created config.env"
    echo ""
    echo "⚠️  IMPORTANT: Please edit config.env with your settings:"
    echo "   - SMTP credentials (email username and password)"
    echo "   - Recipient email address"
    echo "   - Schedule time"
    echo ""
    read -p "Press Enter to open config.env in nano (or Ctrl+C to exit and edit manually)..."
    nano config.env
else
    echo "✓ config.env already exists"
fi
echo ""

# Test run
echo "Would you like to run a test check? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "Running test check..."
    python3 main.py --once
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Setup Complete!                                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "To start the scheduler:"
echo "  python3 main.py"
echo ""
echo "To run a one-time check:"
echo "  python3 main.py --once"
echo ""
echo "To run with Docker:"
echo "  docker-compose up -d"
echo ""
