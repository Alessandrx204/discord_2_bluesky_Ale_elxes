{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python311
  ];

  shellHook = ''
    # Create and activate virtual environment
    if [ ! -d .venv ]; then
      echo "Creating virtual environment..."
      python -m venv .venv
    fi
    source .venv/bin/activate
    
    # Install dependencies
    echo "Installing Python dependencies..."
    pip install -q discord.py atproto python-dotenv
    
    # Load environment variables from .env if it exists
    if [ -f .env ]; then
      echo "Loading environment variables from .env"
      export $(cat .env | grep -v '^#' | xargs)
    else
      echo "⚠️  No .env file found. Copy .env.example to .env and fill in your credentials."
    fi
    
    echo "✅ Development environment ready!"
  '';
}
