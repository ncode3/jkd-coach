#!/bin/bash

# SAMMO Fight IQ - Frontend Setup Script
# Automates the setup of the frontend integration

set -e  # Exit on error

echo "=========================================="
echo "SAMMO Fight IQ - Frontend Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Check if we're in the right directory
if [ ! -d "src" ]; then
    print_error "Error: src/ directory not found."
    print_info "Please run this script from your Lovable project root."
    exit 1
fi

print_info "Setting up SAMMO Fight IQ frontend integration..."
echo ""

# Step 1: Check for required directories
echo "Step 1: Checking directory structure..."
directories=("src/lib" "src/hooks" "src/components" "src/pages" "src/types" "src/utils")

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        print_info "Creating directory: $dir"
        mkdir -p "$dir"
        print_success "Created $dir"
    else
        print_success "Directory exists: $dir"
    fi
done
echo ""

# Step 2: Check if files already exist
echo "Step 2: Checking for existing files..."
files=(
    "src/lib/api.ts"
    "src/hooks/useAuth.ts"
    "src/hooks/useDashboard.ts"
    "src/hooks/useRounds.ts"
    "src/components/RoundLogger.tsx"
    "src/pages/Dashboard.tsx"
    "src/types/index.ts"
    "src/utils/format.ts"
    "src/utils/validation.ts"
)

existing_files=()
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        existing_files+=("$file")
    fi
done

if [ ${#existing_files[@]} -gt 0 ]; then
    print_info "Warning: The following files already exist:"
    for file in "${existing_files[@]}"; do
        echo "  - $file"
    done
    echo ""
    read -p "Do you want to overwrite them? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Setup cancelled."
        exit 0
    fi
fi
echo ""

# Step 3: Check for package.json
echo "Step 3: Checking package.json..."
if [ ! -f "package.json" ]; then
    print_info "package.json not found. Creating from template..."
    if [ -f "package.json.frontend.example" ]; then
        cp package.json.frontend.example package.json
        print_success "Created package.json"
    else
        print_error "Error: package.json.frontend.example not found."
        print_info "Please create package.json manually or use npm init."
    fi
else
    print_success "package.json exists"
fi
echo ""

# Step 4: Check for TypeScript configuration
echo "Step 4: Checking TypeScript configuration..."
if [ ! -f "tsconfig.json" ]; then
    print_info "tsconfig.json not found. Creating basic configuration..."
    cat > tsconfig.json <<EOF
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
EOF
    print_success "Created tsconfig.json"
else
    print_success "tsconfig.json exists"
    print_info "Make sure path aliases are configured: '@/*': ['./src/*']"
fi
echo ""

# Step 5: Check for Vite configuration
echo "Step 5: Checking Vite configuration..."
if [ ! -f "vite.config.ts" ]; then
    print_info "vite.config.ts not found. Creating basic configuration..."
    cat > vite.config.ts <<EOF
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
EOF
    print_success "Created vite.config.ts"
else
    print_success "vite.config.ts exists"
    print_info "Make sure path alias is configured: '@': path.resolve(__dirname, './src')"
fi
echo ""

# Step 6: Check for environment file
echo "Step 6: Checking environment configuration..."
if [ ! -f ".env" ]; then
    print_info ".env not found. Creating from template..."
    if [ -f ".env.frontend.example" ]; then
        cp .env.frontend.example .env
        print_success "Created .env"
        print_info "Please update VITE_API_URL in .env file"
    else
        print_info "Creating default .env..."
        echo "VITE_API_URL=http://localhost:8080" > .env
        print_success "Created .env with default settings"
    fi
else
    print_success ".env exists"
fi
echo ""

# Step 7: Check for Tailwind CSS
echo "Step 7: Checking Tailwind CSS configuration..."
if [ ! -f "tailwind.config.js" ] && [ ! -f "tailwind.config.ts" ]; then
    print_info "Tailwind config not found."
    read -p "Would you like to initialize Tailwind CSS? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v npx &> /dev/null; then
            npx tailwindcss init -p
            print_success "Initialized Tailwind CSS"
        else
            print_error "npx not found. Please install Node.js first."
        fi
    fi
else
    print_success "Tailwind CSS configured"
fi
echo ""

# Step 8: Install dependencies
echo "Step 8: Checking dependencies..."
if command -v npm &> /dev/null; then
    print_info "Checking if node_modules exists..."
    if [ ! -d "node_modules" ]; then
        print_info "Installing dependencies..."
        npm install
        print_success "Dependencies installed"
    else
        print_success "node_modules exists"
        read -p "Would you like to update dependencies? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            npm install
            print_success "Dependencies updated"
        fi
    fi
else
    print_error "npm not found. Please install Node.js first."
fi
echo ""

# Step 9: Summary
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
print_success "Frontend integration files are ready"
echo ""
echo "Next steps:"
echo "1. Update VITE_API_URL in .env file"
echo "2. Ensure backend is running on configured port"
echo "3. Start development server: npm run dev"
echo "4. Create Login/Register pages (see FRONTEND_INTEGRATION.md)"
echo "5. Add routing with React Router"
echo ""
echo "Documentation:"
echo "  - Full guide: FRONTEND_INTEGRATION.md"
echo "  - Quick reference: FRONTEND_QUICK_REFERENCE.md"
echo "  - File summary: FRONTEND_FILES_SUMMARY.md"
echo ""
print_info "Visit http://localhost:5173 after starting dev server"
echo ""
