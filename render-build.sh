#!/bin/bash
set -o errexit

# Install Chrome
CHROME_DIR="/opt/render/project/.render/chrome"
if [ ! -d "$CHROME_DIR" ]; then
  echo "📦 Installing Google Chrome..."
  mkdir -p $CHROME_DIR
  cd $CHROME_DIR
  wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x google-chrome-stable_current_amd64.deb .
  rm google-chrome-stable_current_amd64.deb
  cd -
else
  echo "✅ Chrome already installed"
fi

# Install Python packages
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
