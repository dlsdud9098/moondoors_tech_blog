# Docker 단일 컨테이너 개발 가이드

> **베이스 이미지:** chaosapic/base_image:latest
> **방식:** 하나의 컨테이너 안에서 모든 서비스 실행

---

## 🏗️ 아키텍처

```
┌─────────────────────────────────────────────────┐
│         chaosapic/base_image Container          │
│              (techblog_dev)                      │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Frontend (React + Vite)  :3777          │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Backend (FastAPI)        :8777          │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  PostgreSQL               :5432          │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Qdrant (VectorDB)        :6333          │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  Volumes:                                        │
│  - /workspace/moondoors_tech_blog (code)        │
│  - /models (LLM models from host)               │
│  - postgres_data (persistent)                   │
│  - qdrant_data (persistent)                     │
└─────────────────────────────────────────────────┘
```

---

## 🚀 빠른 시작

### 1. 프로젝트 초기화

```bash
# 환경 변수 설정
cp .env.example .env
# .env 편집 (필요시)

# 초기화 (자동으로 모든 서비스 시작)
make -f Makefile.dev init

# 또는 수동으로
docker-compose -f docker-compose.dev.yml up -d
```

### 2. 서비스 상태 확인

```bash
# 상태 확인
make -f Makefile.dev status

# 로그 확인
make -f Makefile.dev logs
```

### 3. 접속

- **Frontend**: http://localhost:3777
- **Backend API**: http://localhost:8777/docs
- **Qdrant UI**: http://localhost:6333/dashboard
- **PostgreSQL**: localhost:5432

---

## 📋 주요 명령어 (Makefile)

### 컨테이너 관리

```bash
# 시작
make -f Makefile.dev start

# 중지
make -f Makefile.dev stop

# 재시작
make -f Makefile.dev restart

# 컨테이너 접속
make -f Makefile.dev shell

# 로그 확인
make -f Makefile.dev logs
make -f Makefile.dev logs-backend
make -f Makefile.dev logs-frontend
```

### 서비스 재시작 (컨테이너 내부)

```bash
# 백엔드만 재시작
make -f Makefile.dev restart-backend

# 프론트엔드만 재시작
make -f Makefile.dev restart-frontend

# Qdrant만 재시작
make -f Makefile.dev restart-qdrant
```

### 데이터베이스 관리

```bash
# PostgreSQL 접속
make -f Makefile.dev db-shell

# 마이그레이션 실행
make -f Makefile.dev db-migrate

# 마이그레이션 생성
make -f Makefile.dev db-create-migration MSG="add user table"

# 백업
make -f Makefile.dev db-backup

# 복원
make -f Makefile.dev db-restore FILE=backup.sql
```

### 테스트

```bash
# 전체 테스트
make -f Makefile.dev test

# 백엔드 테스트만
make -f Makefile.dev test-backend

# 프론트엔드 테스트만
make -f Makefile.dev test-frontend
```

### 브라우저 열기

```bash
# 프론트엔드 열기
make -f Makefile.dev frontend

# 백엔드 API 문서 열기
make -f Makefile.dev backend

# Qdrant 대시보드 열기
make -f Makefile.dev qdrant
```

---

## 🔧 Docker Compose 직접 사용

```bash
# 시작
docker-compose -f docker-compose.dev.yml up -d

# 중지
docker-compose -f docker-compose.dev.yml down

# 로그
docker-compose -f docker-compose.dev.yml logs -f

# 상태 확인
docker-compose -f docker-compose.dev.yml ps
```

---

## 🏃 컨테이너 내부 작업

### 컨테이너 접속

```bash
# Shell 접속
docker exec -it techblog_dev bash

# 또는
make -f Makefile.dev shell
```

### 컨테이너 내부에서

```bash
# 프로젝트 디렉토리로 이동
cd /workspace/moondoors_tech_blog

# 백엔드 작업
cd backend
source .venv/bin/activate
pytest                          # 테스트
alembic upgrade head            # 마이그레이션
uvicorn app.main:app --reload  # 서버 재시작

# 프론트엔드 작업
cd frontend
npm install                     # 의존성 설치
npm run dev                     # 개발 서버 시작
npm test                        # 테스트

# 데이터베이스 접속
psql -U bloguser -d techblog

# 로그 확인
tail -f /var/log/fastapi.log
tail -f /var/log/vite.log
tail -f /var/log/qdrant.log
```

---

## 📂 파일 구조

```
moondoors_tech_blog/
├── docker-compose.dev.yml       # Docker Compose 설정
├── Makefile.dev                 # 편리한 명령어 모음
├── .env.example                 # 환경 변수 템플릿
├── scripts/
│   └── start-dev.sh            # 자동 시작 스크립트
├── backend/                     # FastAPI 백엔드
├── frontend/                    # React 프론트엔드
└── uploads/                     # 업로드 파일 (볼륨)
```

---

## 🔍 서비스별 상세 정보

### 1. Frontend (React + Vite)
- **포트**: 3777
- **로그**: `/var/log/vite.log`
- **프로세스**: `npm run dev`
- **재시작**: `make -f Makefile.dev restart-frontend`

### 2. Backend (FastAPI)
- **포트**: 8777
- **로그**: `/var/log/fastapi.log`
- **프로세스**: `uvicorn app.main:app --reload`
- **재시작**: `make -f Makefile.dev restart-backend`

### 3. PostgreSQL
- **포트**: 5432
- **데이터**: `/var/lib/postgresql/data/pgdata`
- **로그**: `/var/log/postgresql/postgresql.log`
- **접속**: `psql -U bloguser -d techblog`

### 4. Qdrant
- **포트**: 6333 (HTTP), 6334 (gRPC)
- **로그**: `/var/log/qdrant.log`
- **데이터**: `/qdrant/storage`
- **UI**: http://localhost:6333/dashboard

---

## 🐛 트러블슈팅

### 서비스가 시작되지 않을 때

```bash
# 로그 확인
make -f Makefile.dev logs

# 특정 서비스 로그
make -f Makefile.dev logs-backend
make -f Makefile.dev logs-frontend

# 컨테이너 접속해서 수동 확인
make -f Makefile.dev shell
```

### 포트 충돌

```bash
# 호스트에서 포트 사용 확인
lsof -i :3777
lsof -i :8777
lsof -i :5432
lsof -i :6333

# 컨테이너 재시작
make -f Makefile.dev restart
```

### 데이터베이스 연결 실패

```bash
# 컨테이너 접속
make -f Makefile.dev shell

# PostgreSQL 상태 확인
pg_isready -U bloguser -d techblog

# 수동 재시작
sudo -u postgres /usr/lib/postgresql/15/bin/pg_ctl restart -D /var/lib/postgresql/data/pgdata
```

### Hot Reload 작동 안 함

```bash
# 서비스 재시작
make -f Makefile.dev restart-backend
make -f Makefile.dev restart-frontend

# 또는 컨테이너 전체 재시작
make -f Makefile.dev restart
```

### 로그 파일이 너무 클 때

```bash
# 로그 정리
make -f Makefile.dev clean-logs
```

---

## 🎯 개발 워크플로우

### 일상적인 개발

```bash
# 1. 아침: 컨테이너 시작
make -f Makefile.dev start

# 2. 상태 확인
make -f Makefile.dev status

# 3. 코드 수정 (로컬에서)
# → Hot Reload 자동 적용

# 4. 필요시 로그 확인
make -f Makefile.dev logs-backend

# 5. 저녁: 컨테이너 중지
make -f Makefile.dev stop
```

### 데이터베이스 스키마 변경

```bash
# 1. 모델 수정 (backend/app/models/*.py)

# 2. 마이그레이션 생성
make -f Makefile.dev db-create-migration MSG="add new field"

# 3. 마이그레이션 적용
make -f Makefile.dev db-migrate
```

### 테스트 실행

```bash
# 전체 테스트
make -f Makefile.dev test

# 또는 컨테이너 접속해서
make -f Makefile.dev shell
cd backend && source .venv/bin/activate && pytest
```

---

## 💾 데이터 백업

### 자동 백업 (크론잡 설정)

컨테이너 내부에서:

```bash
# 크론탭 편집
crontab -e

# 매일 새벽 3시 백업
0 3 * * * docker exec techblog_dev pg_dump -U bloguser techblog > /backups/techblog_$(date +\%Y\%m\%d).sql
```

### 수동 백업

```bash
# 백업 생성
make -f Makefile.dev db-backup

# 백업 파일 확인
ls -lh backup_*.sql
```

---

## 🔄 베이스 이미지 업데이트

```bash
# 최신 베이스 이미지 pull
docker pull chaosapic/base_image:latest

# 컨테이너 재생성
make -f Makefile.dev stop
make -f Makefile.dev start
```

---

## 🌐 외부 접근 설정

### 포트 포워딩 (SSH Tunnel)

```bash
# 로컬에서 원격 서버 접근
ssh -L 3777:localhost:3777 \
    -L 8777:localhost:8777 \
    -L 5432:localhost:5432 \
    -L 6333:localhost:6333 \
    user@remote-server
```

### 방화벽 설정 (필요시)

```bash
# ufw 방화벽
sudo ufw allow 3777/tcp
sudo ufw allow 8777/tcp
```

---

## 📊 리소스 모니터링

```bash
# 컨테이너 리소스 사용량
docker stats techblog_dev

# 컨테이너 내부에서
top
htop  # 설치되어 있다면
```

---

## 🔐 보안 체크리스트

- [ ] `.env` 파일에서 SECRET_KEY 변경
- [ ] `.env` 파일에서 POSTGRES_PASSWORD 변경
- [ ] 프로덕션에서 DEBUG=false 설정
- [ ] CORS_ORIGINS를 실제 도메인으로 제한
- [ ] 파일 업로드 크기 제한 확인
- [ ] JWT_SECRET_KEY 강력한 값으로 변경

---

## 🎓 Tips

### 1. 빠른 재시작

특정 서비스만 재시작하면 전체를 재시작하는 것보다 빠릅니다:

```bash
# 백엔드 코드 수정 후
make -f Makefile.dev restart-backend

# 프론트엔드 설정 변경 후
make -f Makefile.dev restart-frontend
```

### 2. 로그 분석

```bash
# 에러만 필터링
docker exec techblog_dev tail -f /var/log/fastapi.log | grep ERROR

# 최근 100줄
docker exec techblog_dev tail -100 /var/log/vite.log
```

### 3. 디버깅

```bash
# Python 디버거 (pdb)
# backend 코드에 breakpoint() 추가
docker attach techblog_dev  # 터미널에서 디버깅
```

---

## 🆘 자주 묻는 질문 (FAQ)

**Q: 컨테이너가 시작되지 않아요**
```bash
# 로그 확인
docker logs techblog_dev

# 스크립트 권한 확인
ls -la scripts/start-dev.sh
chmod +x scripts/start-dev.sh
```

**Q: Hot Reload가 작동하지 않아요**
```bash
# 서비스 재시작
make -f Makefile.dev restart-backend
make -f Makefile.dev restart-frontend
```

**Q: 데이터가 사라졌어요**
```bash
# 볼륨 확인
docker volume ls | grep moondoors

# 볼륨이 삭제되지 않았다면 복구 가능
make -f Makefile.dev start
```

**Q: LLM 모델을 찾을 수 없어요**
```bash
# 호스트에서 모델 경로 확인
ls -la /mnt/storage/models/gemma2-9b

# 컨테이너에서 확인
make -f Makefile.dev shell
ls -la /models/gemma2-9b
```

---

## 🔗 관련 문서

- [프로젝트 진행 상황](PROGRESS.md)
- [기능 목록](FEATURES.md)
- [추가 기능 제안](ADDITIONAL_FEATURES.md)
- [기술 스택 분석](docs/00-tech-stack-analysis.md)

---

## 💬 지원

문제가 발생하면:
1. `make -f Makefile.dev logs` 로그 확인
2. `make -f Makefile.dev status` 상태 확인
3. 컨테이너 재시작: `make -f Makefile.dev restart`
4. 완전 초기화: `make -f Makefile.dev reset`

**Happy Coding! 🚀**
