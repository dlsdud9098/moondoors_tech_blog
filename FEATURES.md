# 테크 블로그 기능 목록

> **프로젝트:** React + FastAPI 기반 테크 블로그
> **포트 설정:** Frontend (3777) / Backend (8777)
> **업데이트:** 2025-11-17

---

## 🎯 핵심 기능

### 1. 📝 게시글 관리 (Article Management)

#### 1.1 게시글 작성/수정
- **마크다운 에디터**
  - 실시간 미리보기 (Split-pane)
  - 마크다운 문법 지원 (GFM - GitHub Flavored Markdown)
  - 코드 블록 작성 (Syntax highlighting with Shiki)
  - 마크다운 툴바 (제목, 굵게, 기울임, 링크, 이미지 등)
  - 단축키 지원 (Ctrl+B, Ctrl+I 등)

- **게시글 메타데이터**
  - 제목 (Title)
  - 설명 (Description)
  - 태그 (Tags) - 다중 선택 가능
  - 발행 상태 (Draft / Published)

- **임시저장 & 발행**
  - 자동 임시저장 (Auto-save drafts)
  - 임시저장된 글 목록 관리
  - 발행 전 미리보기
  - 발행 시간 기록

#### 1.2 게시글 목록 (Article List)
- **홈 페이지**
  - 최신 게시글 목록 표시
  - 게시글 카드 형식 (제목, 요약, 날짜, 태그)
  - 썸네일 이미지 표시
  - 읽기 시간 추정 (Reading time estimation)
  - 페이지네이션 (Pagination)
  - 무한 스크롤 (선택사항)

- **게시글 정렬**
  - 최신순 (Latest)
  - 오래된순 (Oldest)
  - 조회수순 (선택사항)

#### 1.3 게시글 상세 페이지 (Article Detail)
- **콘텐츠 렌더링**
  - 마크다운 → HTML 변환
  - 코드 하이라이팅 (Shiki)
  - 목차 (Table of Contents) - **오른쪽 사이드바**
  - 헤딩 구조 표시 (H2, H3 중첩)
  - Scroll Spy (현재 위치 하이라이트)
  - TOC 항목 클릭 시 smooth scroll
  - 모바일에서 TOC 접기/펼치기

- **멀티미디어 지원**
  - 이미지 갤러리 (Lightbox)
  - 비디오 플레이어 (게시글 내 직접 재생)
  - 오디오 플레이어
  - 파일 다운로드 링크

- **메타 정보**
  - 작성일/수정일
  - 읽기 시간
  - 태그 목록

---

## 🎨 멀티미디어 기능

### 2. 📷 이미지 관리

#### 2.1 이미지 업로드
- **드래그 앤 드롭 업로드** (react-dropzone)
- **다중 파일 선택**
- **파일 검증**
  - 확장자 검사 (.jpg, .jpeg, .png, .gif, .webp)
  - MIME 타입 검사
  - Magic bytes 검사 (보안)
  - 파일 크기 제한 (최대 10MB)

#### 2.2 이미지 처리
- **자동 최적화**
  - 썸네일 생성 (여러 크기)
  - WebP 변환 (용량 절감)
  - EXIF 메타데이터 추출

- **이미지 갤러리**
  - 그리드 레이아웃 (반응형)
  - Lightbox 기능 (확대/축소)
  - 이미지 선택 및 삽입
  - Alt text 및 Caption 지원

### 3. 🎬 비디오 관리

#### 3.1 비디오 업로드
- **지원 포맷:** MP4, WebM, MOV
- **파일 크기 제한:** 최대 100MB
- **비디오 메타데이터 추출**
  - 재생 시간 (Duration)
  - 해상도 (Resolution)
  - 코덱 정보 (Codec)

#### 3.2 비디오 플레이어
- **react-player 통합**
- **게시글 내 직접 재생**
- **플레이어 컨트롤**
  - 재생/일시정지
  - 음량 조절
  - 전체화면 모드
  - 자동재생 옵션
  - 음소거 토글

- **썸네일 자동 생성**
- **YouTube/Vimeo 임베드 지원** (선택사항)

### 4. 🎵 오디오 관리

#### 4.1 오디오 업로드
- **지원 포맷:** MP3, WAV, OGG
- **파일 크기 제한:** 최대 20MB
- **메타데이터 추출**
  - 재생 시간
  - 비트레이트
  - 샘플레이트

#### 4.2 오디오 플레이어
- **커스텀 플레이어 UI**
- **재생 컨트롤**
  - 재생/일시정지
  - 진행바 (Seek bar)
  - 볼륨 조절
  - 재생 시간 표시 (현재/전체)
  - 재생 속도 조절 (선택사항)

### 5. 📄 문서 파일 관리

#### 5.1 문서 업로드
- **지원 포맷:** PDF, DOC, DOCX
- **파일 크기 제한:** 최대 10MB
- **파일 검증** (MIME type, extension, magic bytes)

#### 5.2 문서 다운로드
- **다운로드 링크 컴포넌트**
- **파일 정보 표시**
  - 파일명
  - 파일 크기
  - 파일 타입 아이콘
- **다운로드 카운트** (선택사항)

### 6. 🗂️ 미디어 관리자

- **미디어 라이브러리**
  - 업로드된 모든 미디어 파일 브라우저
  - 타입별 필터링 (이미지/비디오/오디오/문서)
  - 검색 기능
  - 페이지네이션

- **미디어 선택 및 삽입**
  - 게시글 작성 시 미디어 선택 모달
  - 미디어 미리보기
  - 마크다운에 자동 삽입

- **미디어 삭제**
  - 개별 삭제
  - 미사용 파일 정리 (선택사항)

---

## 🔍 검색 및 필터링

### 7. 🔎 검색 기능

#### 7.1 전문 검색 (Full-text Search)
- **검색 대상**
  - 게시글 제목
  - 게시글 내용
  - 태그

- **검색 UI**
  - 헤더 검색창
  - 실시간 검색 제안 (선택사항)
  - 검색 결과 하이라이팅

#### 7.2 검색 결과 페이지
- **결과 목록 표시**
- **검색어 하이라이팅**
- **관련도순 정렬**
- **페이지네이션**

### 8. 🏷️ 태그 시스템

#### 8.1 태그 관리
- **태그 생성**
  - 게시글 작성 시 태그 추가
  - 태그 자동완성
  - 중복 태그 방지

- **태그 목록 페이지**
  - 모든 태그 표시
  - 태그별 게시글 수 표시
  - 태그 클라우드 (선택사항)

#### 8.2 태그 필터링
- **태그별 게시글 필터링**
- **다중 태그 선택** (AND/OR 조건)
- **태그 조합 검색**

---

## 📱 UI/UX 기능

### 9. 🎨 레이아웃 및 디자인

#### 9.1 반응형 디자인
- **모바일 우선 (Mobile-first)**
  - 모바일 (< 768px)
  - 태블릿 (768-1024px)
  - 데스크탑 (> 1024px)

- **터치 제스처 지원**
  - 스와이프
  - 핀치 줌 (이미지)

#### 9.2 네비게이션
- **헤더 (Header)**
  - 로고/제목
  - 메인 메뉴
  - 검색창
  - 다크모드 토글

- **푸터 (Footer)**
  - 저작권 정보
  - 소셜 링크
  - RSS 피드 링크

#### 9.3 다크 모드
- **라이트/다크 테마 전환**
- **사용자 선호 설정 저장** (localStorage)
- **시스템 설정 자동 감지** (prefers-color-scheme)

### 10. 🚀 성능 최적화

#### 10.1 프론트엔드 최적화
- **코드 스플리팅** (Code splitting)
- **Lazy loading** (이미지, 컴포넌트)
- **번들 최적화**
- **이미지 최적화** (WebP, responsive images)
- **목표 성능**
  - FCP (First Contentful Paint) < 1.5s
  - TTI (Time to Interactive) < 3s
  - LCP (Largest Contentful Paint) < 2.5s

#### 10.2 백엔드 최적화
- **데이터베이스 인덱싱**
- **쿼리 최적화** (N+1 방지)
- **Redis 캐싱** (선택사항)
- **응답 시간 목표:** < 200ms (p95)

---

## 🔒 보안 기능

### 11. 🛡️ 보안

#### 11.1 파일 업로드 보안
- **다중 검증 레이어**
  1. 파일 확장자 검사
  2. MIME 타입 검사
  3. Magic bytes 검사 (실제 파일 타입)
  4. 파일 크기 제한

- **악성 파일 차단**
- **파일명 sanitization**
- **UUID 파일명 생성**

#### 11.2 XSS 방지
- **마크다운 sanitization**
  - 백엔드: nh3 (Rust-based)
  - 프론트엔드: rehype-sanitize
- **허용 태그/속성 화이트리스트**
- **위험한 프로토콜 차단** (javascript:, vbscript:)

#### 11.3 CORS 설정
- **환경별 allowed origins**
  - Development: http://localhost:3777
  - Production: 실제 도메인
- **Credentials 지원**
- **Preflight 요청 처리**

#### 11.4 추가 보안
- **CSP (Content Security Policy) 헤더**
- **Rate limiting** (API 요청 제한)
- **SQL Injection 방지** (ORM 사용)

---

## 📊 SEO 및 메타데이터

### 12. 🔍 SEO 최적화

#### 12.1 메타 태그
- **동적 title 태그**
- **meta description**
- **Open Graph 태그** (Facebook, LinkedIn)
- **Twitter Card 태그**
- **Canonical URL**

#### 12.2 구조화 데이터
- **Schema.org 마크업** (선택사항)
  - Article schema
  - BlogPosting schema
  - Author schema

#### 12.3 RSS 피드
- **자동 생성 RSS 피드**
- **피드 구독 링크**

#### 12.4 사이트맵
- **XML sitemap 자동 생성**
- **robots.txt 설정**

---

## 🧪 테스팅 및 품질

### 13. ✅ 테스트

#### 13.1 백엔드 테스트 (pytest)
- **단위 테스트** (Unit tests)
  - 모델 테스트
  - 서비스 로직 테스트
  - 유틸리티 함수 테스트

- **통합 테스트** (Integration tests)
  - API 엔드포인트 테스트
  - 파일 업로드 테스트
  - 데이터베이스 연동 테스트

- **목표 커버리지:** > 80%

#### 13.2 프론트엔드 테스트
- **Vitest (Unit/Integration)**
  - 컴포넌트 테스트 (React Testing Library)
  - 훅 테스트
  - 유틸리티 함수 테스트

- **Playwright (E2E)**
  - 게시글 작성 플로우
  - 파일 업로드 플로우
  - 검색 플로우
  - 크로스 브라우저 테스트

#### 13.3 코드 품질
- **TypeScript strict mode: 100%**
- **ESLint/Pylint: 0 errors**
- **자동 포맷팅** (Black, Prettier)

---

## 🚀 배포 및 운영

### 14. 🔧 개발 환경

#### 14.1 포트 설정
- **Frontend (React + Vite):** http://localhost:3777
- **Backend (FastAPI):** http://localhost:8777
- **Database (PostgreSQL):** localhost:5432

#### 14.2 개발 도구
- **Hot reload** (Frontend/Backend 모두)
- **자동 타입 체크** (TypeScript, mypy)
- **자동 테스트 실행** (Watch mode)

### 15. 📦 배포

#### 15.1 Docker 지원
- **Docker Compose 설정**
  - Frontend 컨테이너
  - Backend 컨테이너
  - PostgreSQL 컨테이너
  - Redis 컨테이너 (선택사항)

#### 15.2 CI/CD 파이프라인
- **GitHub Actions**
  - 백엔드 테스트 자동화
  - 프론트엔드 테스트 자동화
  - 린팅 자동화
  - 배포 자동화

#### 15.3 배포 옵션
- **백엔드:**
  - Docker + Railway/Render
  - AWS ECS
  - Google Cloud Run

- **프론트엔드:**
  - Vercel/Netlify
  - Cloudflare Pages
  - AWS S3 + CloudFront

- **데이터베이스:**
  - Railway PostgreSQL
  - AWS RDS
  - Supabase

---

## 📈 향후 확장 기능 (선택사항)

### 16. 🔮 추가 기능 아이디어

#### 16.1 소셜 기능
- **댓글 시스템** (Giscus via GitHub Discussions)
- **소셜 공유 버튼** (Facebook, Twitter, LinkedIn)
- **게시글 좋아요** (Like/Reaction)

#### 16.2 사용자 기능
- **사용자 인증** (JWT 기반)
- **관리자 대시보드**
- **게시글 통계** (조회수, 인기 글)

#### 16.3 콘텐츠 기능
- **시리즈/카테고리 기능**
- **관련 게시글 추천**
- **뉴스레터 구독**

#### 16.4 분석 기능
- **Google Analytics 통합**
- **Web Vitals 모니터링**
- **사용자 행동 분석**

---

## 📋 기능 구현 현황

현재 구현 현황은 [PROGRESS.md](PROGRESS.md)에서 확인할 수 있습니다.

**총 36개 이슈** (5단계)
- **Phase 1:** Backend Foundation (8개 이슈)
- **Phase 2:** Frontend Foundation (6개 이슈)
- **Phase 3:** Multimedia Features (8개 이슈)
- **Phase 4:** Content Management (8개 이슈)
- **Phase 5:** Polish & Advanced (6개 이슈)

**예상 개발 시간:** 75-94시간 (2-3주, 1인 개발 기준)

---

## 🎯 성공 기준

### 코드 품질
- ✅ 테스트 커버리지 > 80%
- ✅ TypeScript strict mode: 100%
- ✅ ESLint/Pylint 에러: 0개
- ✅ 심각한 보안 취약점: 0개

### 성능
- ✅ 백엔드 API 응답: < 200ms (p95)
- ✅ 프론트엔드 FCP: < 1.5s
- ✅ 프론트엔드 TTI: < 3s
- ✅ 파일 업로드: 최대 100MB

### 확장성
- ✅ 10,000개 게시글 지원
- ✅ 100,000개 미디어 파일 지원
- ✅ 1,000명 동시 접속 처리

---

## 📚 참고 문서

- [기술 스택 분석](docs/00-tech-stack-analysis.md)
- [이슈 상세 명세](docs/01-issue-breakdown.md)
- [전체 이슈 요약](docs/02-complete-issue-summary.md)
- [진행 상황 체크리스트](PROGRESS.md)
