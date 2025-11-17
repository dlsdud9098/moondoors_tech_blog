#!/bin/bash

set -e

echo "=========================================="
echo "🚀 Tech Blog Development Environment"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Navigate to workspace
cd /workspace/moondoors_tech_blog

echo -e "${BLUE}📂 Working directory: $(pwd)${NC}"
echo ""

# ==========================================
# 1. PostgreSQL Setup
# ==========================================
echo -e "${BLUE}🐘 Starting PostgreSQL...${NC}"

# Check if PostgreSQL is already running
if pg_isready -U bloguser -d techblog &> /dev/null; then
    echo -e "${GREEN}✓ PostgreSQL already running${NC}"
else
    # Initialize PostgreSQL if needed
    if [ ! -d "/var/lib/postgresql/data/pgdata" ]; then
        echo -e "${YELLOW}Initializing PostgreSQL...${NC}"
        sudo -u postgres /usr/lib/postgresql/15/bin/initdb -D /var/lib/postgresql/data/pgdata
    fi

    # Start PostgreSQL
    sudo -u postgres /usr/lib/postgresql/15/bin/pg_ctl start -D /var/lib/postgresql/data/pgdata -l /var/log/postgresql/postgresql.log

    # Wait for PostgreSQL to be ready
    echo "Waiting for PostgreSQL..."
    for i in {1..30}; do
        if pg_isready -U postgres &> /dev/null; then
            break
        fi
        sleep 1
    done

    # Create user and database
    sudo -u postgres psql -c "CREATE USER bloguser WITH PASSWORD 'blogpassword';" 2>/dev/null || true
    sudo -u postgres psql -c "CREATE DATABASE techblog OWNER bloguser;" 2>/dev/null || true
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE techblog TO bloguser;" 2>/dev/null || true

    echo -e "${GREEN}✓ PostgreSQL started${NC}"
fi

echo ""

# ==========================================
# 2. Qdrant Setup
# ==========================================
echo -e "${BLUE}🔍 Starting Qdrant Vector Database...${NC}"

# Check if Qdrant is already running
if curl -s http://localhost:6333/healthz &> /dev/null; then
    echo -e "${GREEN}✓ Qdrant already running${NC}"
else
    # Start Qdrant in background
    nohup qdrant > /var/log/qdrant.log 2>&1 &

    # Wait for Qdrant to be ready
    echo "Waiting for Qdrant..."
    for i in {1..30}; do
        if curl -s http://localhost:6333/healthz &> /dev/null; then
            break
        fi
        sleep 1
    done

    echo -e "${GREEN}✓ Qdrant started${NC}"
fi

echo ""

# ==========================================
# 3. Backend Setup (FastAPI)
# ==========================================
echo -e "${BLUE}⚡ Setting up Backend (FastAPI)...${NC}"

if [ -d "backend" ]; then
    cd backend

    # Create virtual environment if not exists
    if [ ! -d ".venv" ]; then
        echo -e "${YELLOW}Creating Python virtual environment...${NC}"
        python3 -m venv .venv
    fi

    # Activate virtual environment
    source .venv/bin/activate

    # Install dependencies
    if [ -f "requirements.txt" ]; then
        echo -e "${YELLOW}Installing backend dependencies...${NC}"
        pip install -q --upgrade pip
        pip install -q -r requirements.txt

        if [ -f "requirements-dev.txt" ]; then
            pip install -q -r requirements-dev.txt
        fi
        echo -e "${GREEN}✓ Backend dependencies installed${NC}"
    fi

    # Run migrations
    if [ -f "alembic.ini" ]; then
        echo -e "${YELLOW}Running database migrations...${NC}"
        alembic upgrade head 2>/dev/null || echo "No migrations to run"
    fi

    # Start FastAPI server in background
    echo -e "${YELLOW}Starting FastAPI server on port 8777...${NC}"
    nohup uvicorn app.main:app --host 0.0.0.0 --port 8777 --reload > /var/log/fastapi.log 2>&1 &

    echo -e "${GREEN}✓ Backend started at http://localhost:8777${NC}"
    echo -e "${BLUE}  API Docs: http://localhost:8777/docs${NC}"

    cd ..
else
    echo -e "${YELLOW}⚠ Backend directory not found, skipping...${NC}"
fi

echo ""

# ==========================================
# 4. Frontend Setup (React + Vite)
# ==========================================
echo -e "${BLUE}⚛️  Setting up Frontend (React)...${NC}"

if [ -d "frontend" ]; then
    cd frontend

    # Install dependencies
    if [ -f "package.json" ]; then
        if [ ! -d "node_modules" ]; then
            echo -e "${YELLOW}Installing frontend dependencies...${NC}"
            npm install
            echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
        fi

        # Start Vite dev server in background
        echo -e "${YELLOW}Starting Vite dev server on port 3777...${NC}"
        nohup npm run dev -- --host 0.0.0.0 --port 3777 > /var/log/vite.log 2>&1 &

        echo -e "${GREEN}✓ Frontend started at http://localhost:3777${NC}"
    fi

    cd ..
else
    echo -e "${YELLOW}⚠ Frontend directory not found, skipping...${NC}"
fi

echo ""

# ==========================================
# Summary
# ==========================================
echo "=========================================="
echo -e "${GREEN}✨ All services started!${NC}"
echo "=========================================="
echo ""
echo -e "${BLUE}📍 Access Points:${NC}"
echo "  Frontend:        http://localhost:3777"
echo "  Backend API:     http://localhost:8777"
echo "  API Docs:        http://localhost:8777/docs"
echo "  PostgreSQL:      localhost:5432"
echo "  Qdrant UI:       http://localhost:6333/dashboard"
echo ""
echo -e "${BLUE}📝 Logs:${NC}"
echo "  Backend:  tail -f /var/log/fastapi.log"
echo "  Frontend: tail -f /var/log/vite.log"
echo "  Qdrant:   tail -f /var/log/qdrant.log"
echo "  PostgreSQL: tail -f /var/log/postgresql/postgresql.log"
echo ""
echo -e "${BLUE}🔧 Useful Commands:${NC}"
echo "  Enter container: docker exec -it techblog_dev bash"
echo "  Stop services:   docker-compose -f docker-compose.dev.yml down"
echo "  View logs:       docker logs -f techblog_dev"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop watching logs (services will keep running)${NC}"
echo ""

# Keep container running and tail logs
tail -f /var/log/fastapi.log /var/log/vite.log /var/log/qdrant.log 2>/dev/null || bash
