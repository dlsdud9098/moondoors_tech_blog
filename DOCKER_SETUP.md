# Docker 통합 관리 가이드

> **프로젝트:** React + FastAPI Tech Blog
> **포트 설정:** Frontend (3777) / Backend (8777) / PostgreSQL (5432) / Qdrant (6333)

---

## 📦 Docker Compose 아키텍처

```
┌─────────────────────────────────────────────────────┐
│                  Docker Network                      │
│                  (blog_network)                      │
│                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │   Frontend   │  │   Backend    │  │PostgreSQL │ │
│  │  React+Vite  │◄─┤   FastAPI    │◄─┤    15     │ │
│  │   Port 3777  │  │   Port 8777  │  │Port 5432  │ │
│  └──────────────┘  └──────┬───────┘  └───────────┘ │
│                            │                         │
│                            ▼                         │
│                    ┌──────────────┐                 │
│                    │    Qdrant    │                 │
│                    │  VectorDB    │                 │
│                    │  Port 6333   │                 │
│                    └──────────────┘                 │
│                                                       │
│  ┌──────────────┐                                   │
│  │   pgAdmin    │  (Optional, --profile tools)      │
│  │   Port 5050  │                                   │
│  └──────────────┘                                   │
└─────────────────────────────────────────────────────┘

        ▲
        │ Mount: /mnt/storage/models (Local LLM)
        │
```

---

## 🚀 빠른 시작

### 1. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# 필요한 값 수정 (SECRET_KEY, PASSWORD 등)
nano .env
```

### 2. Docker Compose 실행

```bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 특정 서비스 로그만 보기
docker-compose logs -f backend
```

### 3. 접속 확인

- **Frontend**: http://localhost:3777
- **Backend API**: http://localhost:8777
- **Backend Docs**: http://localhost:8777/docs
- **PostgreSQL**: localhost:5432
- **Qdrant UI**: http://localhost:6333/dashboard
- **pgAdmin** (optional): http://localhost:5050

---

## 📋 Docker Compose 서비스 구성

### 1. PostgreSQL (postgres)
- **이미지**: postgres:15-alpine
- **포트**: 5432
- **볼륨**: postgres_data
- **환경변수**:
  - POSTGRES_USER: bloguser
  - POSTGRES_PASSWORD: blogpassword
  - POSTGRES_DB: techblog
- **Health Check**: pg_isready

### 2. Qdrant (qdrant)
- **이미지**: qdrant/qdrant:latest
- **포트**: 6333 (HTTP), 6334 (gRPC)
- **볼륨**: qdrant_data
- **용도**: Vector Database (AI Semantic Search)
- **Health Check**: HTTP /healthz

### 3. Backend (backend)
- **빌드**: ./backend/Dockerfile
- **포트**: 8777
- **볼륨**:
  - ./backend → /app (코드 동기화)
  - /mnt/storage/models → /models (LLM 모델)
  - backend_uploads → /app/uploads (파일 업로드)
- **의존성**: postgres, qdrant
- **Health Check**: HTTP /health
- **Hot Reload**: uvicorn --reload

### 4. Frontend (frontend)
- **빌드**: ./frontend/Dockerfile
- **포트**: 3777
- **볼륨**:
  - ./frontend → /app (코드 동기화)
  - /app/node_modules (익명 볼륨)
- **의존성**: backend
- **Health Check**: HTTP /
- **Hot Reload**: vite --host 0.0.0.0

### 5. pgAdmin (pgadmin) - Optional
- **이미지**: dpage/pgadmin4:latest
- **포트**: 5050
- **활성화**: `docker-compose --profile tools up`

---

## 🔧 주요 명령어

### 서비스 관리

```bash
# 전체 시작 (백그라운드)
docker-compose up -d

# 전체 시작 (로그 출력)
docker-compose up

# 전체 중지
docker-compose down

# 전체 중지 + 볼륨 삭제
docker-compose down -v

# 재시작
docker-compose restart

# 특정 서비스만 재시작
docker-compose restart backend
```

### 빌드

```bash
# 전체 재빌드
docker-compose build

# 캐시 없이 재빌드
docker-compose build --no-cache

# 특정 서비스만 재빌드
docker-compose build backend
```

### 로그 확인

```bash
# 전체 로그
docker-compose logs -f

# 마지막 100줄
docker-compose logs --tail=100

# 특정 서비스
docker-compose logs -f frontend backend
```

### 컨테이너 접속

```bash
# Backend 컨테이너 접속
docker-compose exec backend bash

# Frontend 컨테이너 접속
docker-compose exec frontend sh

# PostgreSQL 접속
docker-compose exec postgres psql -U bloguser -d techblog
```

### 데이터베이스 관리

```bash
# DB 백업
docker-compose exec postgres pg_dump -U bloguser techblog > backup.sql

# DB 복원
docker-compose exec -T postgres psql -U bloguser techblog < backup.sql

# Alembic 마이그레이션 실행
docker-compose exec backend alembic upgrade head

# 새 마이그레이션 생성
docker-compose exec backend alembic revision --autogenerate -m "migration message"
```

---

## 🔍 Health Check 확인

```bash
# 모든 서비스 상태 확인
docker-compose ps

# 개별 Health Check
curl http://localhost:8777/health     # Backend
curl http://localhost:3777            # Frontend
curl http://localhost:6333/healthz    # Qdrant
docker-compose exec postgres pg_isready -U bloguser  # PostgreSQL
```

---

## 📦 볼륨 관리

### 볼륨 목록

- **postgres_data**: PostgreSQL 데이터
- **qdrant_data**: Qdrant 벡터 DB 데이터
- **backend_uploads**: 업로드된 파일 (이미지, 비디오, 문서)
- **pgadmin_data**: pgAdmin 설정

### 볼륨 명령어

```bash
# 볼륨 목록 확인
docker volume ls | grep blog

# 볼륨 상세 정보
docker volume inspect moondoors_tech_blog_postgres_data

# 볼륨 삭제 (⚠️ 데이터 손실 주의)
docker volume rm moondoors_tech_blog_postgres_data
```

---

## 🔐 보안 설정

### 1. 환경 변수 변경 (필수)

`.env` 파일에서 다음 값들을 **반드시** 변경하세요:

```bash
# 강력한 비밀번호 생성
openssl rand -base64 32

# .env 파일 수정
SECRET_KEY=<생성된_랜덤_값>
POSTGRES_PASSWORD=<강력한_비밀번호>
PGADMIN_DEFAULT_PASSWORD=<강력한_비밀번호>
JWT_SECRET_KEY=<생성된_랜덤_값>
```

### 2. 프로덕션 모드

프로덕션 환경에서는 별도의 `docker-compose.prod.yml` 사용 권장:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 🐛 트러블슈팅

### 1. 포트 충돌

```bash
# 포트 사용 확인
lsof -i :3777
lsof -i :8777
lsof -i :5432

# 사용 중인 프로세스 종료
kill -9 <PID>
```

### 2. 볼륨 권한 문제

```bash
# 볼륨 권한 수정 (backend uploads)
docker-compose exec backend chown -R 1000:1000 /app/uploads
```

### 3. 데이터베이스 연결 실패

```bash
# PostgreSQL 로그 확인
docker-compose logs postgres

# 수동 연결 테스트
docker-compose exec backend python -c "from app.database import engine; print('DB OK')"
```

### 4. Hot Reload 작동 안 함

```bash
# 컨테이너 재시작
docker-compose restart backend frontend

# 볼륨 마운트 확인
docker-compose exec backend ls -la /app
docker-compose exec frontend ls -la /app
```

### 5. LLM 모델 경로 문제

```bash
# 호스트에서 모델 경로 확인
ls -la /mnt/storage/models/gemma2-9b

# 컨테이너 내부에서 확인
docker-compose exec backend ls -la /models/gemma2-9b

# 권한 확인 (읽기 권한 필요)
chmod -R 755 /mnt/storage/models/gemma2-9b
```

---

## 🎯 개발 워크플로우

### 1. 처음 시작할 때

```bash
# 1. 저장소 클론
git clone <repo-url>
cd moondoors_tech_blog

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일 수정

# 3. Docker Compose 실행
docker-compose up -d

# 4. 데이터베이스 마이그레이션
docker-compose exec backend alembic upgrade head

# 5. 브라우저에서 확인
open http://localhost:3777
```

### 2. 일상적인 개발

```bash
# 아침: 서비스 시작
docker-compose up -d

# 코드 수정 (./backend, ./frontend)
# → Hot Reload 자동 적용

# 로그 확인
docker-compose logs -f backend

# 저녁: 서비스 중지
docker-compose down
```

### 3. 데이터베이스 스키마 변경

```bash
# 1. 모델 수정 (backend/app/models/*.py)

# 2. 마이그레이션 생성
docker-compose exec backend alembic revision --autogenerate -m "add new field"

# 3. 마이그레이션 적용
docker-compose exec backend alembic upgrade head
```

### 4. 테스트 실행

```bash
# Backend 테스트
docker-compose exec backend pytest

# Frontend 테스트
docker-compose exec frontend npm test

# E2E 테스트
docker-compose exec frontend npm run test:e2e
```

---

## 📊 모니터링

### Docker Stats

```bash
# 실시간 리소스 사용량
docker stats
```

### 서비스별 리소스 제한 (docker-compose.yml에 추가)

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

---

## 🚀 프로덕션 배포

### 1. 프로덕션용 Dockerfile 작성

**backend/Dockerfile.prod:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8777", "--workers", "4"]
```

**frontend/Dockerfile.prod:**
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 2. 프로덕션 Compose 파일

**docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  backend:
    build:
      dockerfile: Dockerfile.prod
    environment:
      APP_ENV: production
      DEBUG: "false"
    restart: always

  frontend:
    build:
      dockerfile: Dockerfile.prod
    restart: always
```

### 3. 배포 실행

```bash
# 프로덕션 빌드 및 실행
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# HTTPS (Nginx Proxy Manager or Traefik 사용 권장)
```

---

## 📝 체크리스트

### 초기 설정
- [ ] `.env` 파일 생성 및 수정
- [ ] SECRET_KEY, PASSWORD 변경
- [ ] /mnt/storage/models 경로 확인
- [ ] Docker 및 Docker Compose 설치 확인

### 서비스 시작
- [ ] `docker-compose up -d` 실행
- [ ] Health Check 통과 확인
- [ ] Frontend 접속 확인 (3777)
- [ ] Backend API 문서 확인 (8777/docs)
- [ ] PostgreSQL 연결 확인
- [ ] Qdrant 연결 확인

### 개발 환경
- [ ] Hot Reload 작동 확인
- [ ] 데이터베이스 마이그레이션 적용
- [ ] 테스트 실행 확인

---

## 🔗 관련 문서

- [프로젝트 진행 상황](PROGRESS.md)
- [기능 목록](FEATURES.md)
- [추가 기능 제안](ADDITIONAL_FEATURES.md)
- [기술 스택 분석](docs/00-tech-stack-analysis.md)

---

## 💡 팁

### 1. 개발 속도 향상

```bash
# 특정 서비스만 재시작 (빠름)
docker-compose restart backend

# 전체 재시작 (느림, 피하기)
docker-compose down && docker-compose up -d
```

### 2. 디스크 공간 확보

```bash
# 사용하지 않는 이미지/컨테이너 정리
docker system prune -a

# 볼륨은 유지하면서 정리
docker system prune
```

### 3. 로그 파일 크기 제한

`docker-compose.yml`에 추가:
```yaml
x-logging: &default-logging
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

services:
  backend:
    logging: *default-logging
```

---

## 🆘 지원

문제가 발생하면:
1. `docker-compose logs -f` 로그 확인
2. Health Check 상태 확인: `docker-compose ps`
3. 환경 변수 확인: `.env` 파일
4. GitHub Issues 등록

**Happy Coding! 🚀**
