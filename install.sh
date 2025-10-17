#!/bin/bash

set -e

echo "Starting Last-fm-collage-maker install..."

if [ -n "$1" ]; then
    INSTALL_DIR="$1"
else
    if [ -d "/usr/local/bin" ]; then
        INSTALL_DIR="/usr/local/bin"
    else
        INSTALL_DIR="$HOME/bin"
    fi
fi

if [ ! -d "$INSTALL_DIR" ]; then
    echo "Creating $INSTALL_DIR directory..."
    mkdir -p "$INSTALL_DIR"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/main.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: main.py script not found"
    exit 1
fi

BASH_SCRIPT="$INSTALL_DIR/lastfm"

echo "Creating bash script..."

TEMP_SCRIPT=$(mktemp)
echo "Temporary script created at: $TEMP_SCRIPT"

cat > "$TEMP_SCRIPT" << 'EOF'
#!/bin/bash

SCRIPT_DIR="SCRIPT_DIR_PLACEHOLDER"
MAIN_SCRIPT="$SCRIPT_DIR/main.py"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: virtual environment not found at $SCRIPT_DIR/.venv"
    echo "Please create virtual environment and install all dependencies"
    exit 1
fi

if [ ! -f "$MAIN_SCRIPT" ]; then
    echo "Error: main.py script not found at $MAIN_SCRIPT"
    exit 1
fi

"$VENV_PYTHON" "$MAIN_SCRIPT" "$@"
EOF

if sed --version >/dev/null 2>&1; then
    sed -i "s|SCRIPT_DIR_PLACEHOLDER|$SCRIPT_DIR|g" "$TEMP_SCRIPT"
else
    sed -i '' "s|SCRIPT_DIR_PLACEHOLDER|$SCRIPT_DIR|g" "$TEMP_SCRIPT"
fi

echo "Installing to: $BASH_SCRIPT"

sudo cp "$TEMP_SCRIPT" "$BASH_SCRIPT"
sudo chmod +x "$BASH_SCRIPT"
rm -f "$TEMP_SCRIPT"

sudo chmod +x "$BASH_SCRIPT"
sudo chmod 755 "$BASH_SCRIPT"

echo "Installation completed!"