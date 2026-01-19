#!/bin/bash
# Script to run Next.js with automatic Node version switching

cd "$(dirname "$0")"

# Load nvm if available
if [ -s "$HOME/.nvm/nvm.sh" ]; then
  source "$HOME/.nvm/nvm.sh"
  
  # If .nvmrc exists, use it
  if [ -f .nvmrc ]; then
    nvm use
  else
    # Otherwise use Node 22
    nvm use 22 2>/dev/null || nvm use 20 2>/dev/null || echo "Failed to switch to Node 20/22"
  fi
fi

# Check Node version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 20 ]; then
  echo "⚠️  Error: Node.js version $(node -v) is too old."
  echo "Next.js 16 requires Node.js >= 20.9.0"
  echo ""
  echo "Solution:"
  echo "1. Switch to Node 20+ via nvm:"
  echo "   source ~/.nvm/nvm.sh && nvm use 22"
  echo ""
  echo "2. Or run this script again (it will try to switch automatically)"
  exit 1
fi

# Run Next.js
exec npm run dev
