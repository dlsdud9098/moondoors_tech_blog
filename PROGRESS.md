# 프로젝트 진행 상황 체크리스트

> **마지막 업데이트:** 2025-11-17
> **전체 진행률:** 0/36 (0%)
> **포트 설정:** Frontend: 3777 / Backend: 8777

---

## 📊 Phase별 진행 현황

| Phase | 완료/전체 | 진행률 | 예상 시간 |
|-------|----------|--------|-----------|
| Phase 1: Backend Foundation | 0/8 | 0% | 16-20h |
| Phase 2: Frontend Foundation | 0/6 | 0% | 11-15h |
| Phase 3: Multimedia Features | 0/8 | 0% | 18-22h |
| Phase 4: Content Management | 0/8 | 0% | 17-21h |
| Phase 5: Polish & Advanced | 0/6 | 0% | 13-16h |
| **전체** | **0/36** | **0%** | **75-94h** |

---

## Phase 1: Backend Foundation (0/8)

### #1 FastAPI Project Setup with Testing Infrastructure
- [ ] 프로젝트 초기화 완료
- [ ] pytest 설정 완료
- [ ] 디렉토리 구조 생성
- [ ] 기본 헬스체크 엔드포인트
- [ ] 테스트 통과 (coverage > 80%)
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 1-2시간
**담당자:** -
**이슈 번호:** -

---

### #2 PostgreSQL Database Setup and Connection
- [ ] PostgreSQL 설치 및 설정
- [ ] SQLAlchemy async 설정
- [ ] Alembic 마이그레이션 설정
- [ ] 데이터베이스 연결 테스트
- [ ] 환경 변수 설정
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2시간
**담당자:** -
**의존성:** #1
**이슈 번호:** -

---

### #3 Article and Tag Database Models
- [ ] Article 모델 생성
- [ ] Tag 모델 생성
- [ ] 관계 설정 (Many-to-Many)
- [ ] Pydantic 스키마 생성
- [ ] 마이그레이션 파일 생성
- [ ] 모델 테스트 통과
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2시간
**담당자:** -
**의존성:** #2
**이슈 번호:** -

---

### #4 Article CRUD API Endpoints
- [ ] GET /api/v1/articles (목록, 페이지네이션)
- [ ] GET /api/v1/articles/{id} (상세)
- [ ] POST /api/v1/articles (생성)
- [ ] PUT /api/v1/articles/{id} (수정)
- [ ] DELETE /api/v1/articles/{id} (삭제)
- [ ] API 테스트 통과
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2-3시간
**담당자:** -
**의존성:** #3
**이슈 번호:** -

---

### #5 Media File Database Model
- [ ] MediaFile 모델 생성
- [ ] Article-MediaFile 관계 설정
- [ ] 파일 타입별 필드 정의
- [ ] Pydantic 스키마 생성
- [ ] 마이그레이션 파일 생성
- [ ] 모델 테스트 통과
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2시간
**담당자:** -
**의존성:** #3
**이슈 번호:** -

---

### #6 File Upload Service with Validation
- [ ] 파일 타입 검증 (확장자, MIME, magic bytes)
- [ ] 파일 크기 검증
- [ ] 저장소 추상화 (local/S3)
- [ ] 파일명 생성 (UUID)
- [ ] 파일 저장 서비스
- [ ] 유닛 테스트 통과
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 3시간
**담당자:** -
**의존성:** #5
**이슈 번호:** -

---

### #7 Image Upload API Endpoint
- [ ] POST /api/v1/media/images 엔드포인트
- [ ] 이미지 업로드 처리
- [ ] 썸네일 자동 생성
- [ ] WebP 변환
- [ ] 메타데이터 추출 (크기, 포맷)
- [ ] API 테스트 통과
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2시간
**담당자:** -
**의존성:** #6
**이슈 번호:** -

---

### #8 Video/Audio/Document Upload Endpoints
- [ ] POST /api/v1/media/videos 엔드포인트
- [ ] POST /api/v1/media/audios 엔드포인트
- [ ] POST /api/v1/media/documents 엔드포인트
- [ ] 비디오 메타데이터 추출 (duration, codec)
- [ ] 오디오 메타데이터 추출
- [ ] 문서 파일 검증
- [ ] API 테스트 통과
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2-3시간
**담당자:** -
**의존성:** #6, #7
**이슈 번호:** -

---

## Phase 2: Frontend Foundation (0/6)

### #9 React + Vite Project Setup with Testing
- [ ] React 프로젝트 초기화 (Vite)
- [ ] TypeScript 설정
- [ ] Vitest 설정
- [ ] React Testing Library 설정
- [ ] Playwright 설정
- [ ] 기본 컴포넌트 테스트 통과
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 1-2시간
**담당자:** -
**이슈 번호:** -

---

### #10 API Client Service and React Query Setup
- [ ] Axios 클라이언트 설정
- [ ] TanStack Query 설정
- [ ] API 타입 정의 (TypeScript)
- [ ] 에러 핸들링
- [ ] 인터셉터 설정
- [ ] Mock 서버 테스트
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2시간
**담당자:** -
**의존성:** #9
**이슈 번호:** -

---

### #11 React Router and Basic Layout
- [ ] React Router 설정
- [ ] Header 컴포넌트
- [ ] Footer 컴포넌트
- [ ] Navigation 컴포넌트
- [ ] 레이아웃 구조
- [ ] 라우팅 테스트 통과
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2시간
**담당자:** -
**의존성:** #9
**이슈 번호:** -

---

### #12 Article List Page with Pagination
- [ ] 홈 페이지 라우트
- [ ] 게시글 목록 컴포넌트
- [ ] 게시글 카드 컴포넌트
- [ ] 페이지네이션 컴포넌트
- [ ] 로딩 상태 처리
- [ ] 빈 상태 처리
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2-3시간
**담당자:** -
**의존성:** #10, #11
**이슈 번호:** -

---

### #13 Article Detail Page with Markdown Rendering
- [ ] 게시글 상세 페이지 라우트
- [ ] react-markdown 설정
- [ ] 코드 하이라이팅 (Shiki)
- [ ] 마크다운 스타일링
- [ ] 메타데이터 표시
- [ ] 렌더링 테스트 통과
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2-3시간
**담당자:** -
**의존성:** #10, #11
**이슈 번호:** -

---

### #14 Responsive Design and Mobile Optimization
- [ ] 모바일 레이아웃 (< 768px)
- [ ] 태블릿 레이아웃 (768-1024px)
- [ ] 데스크탑 레이아웃 (> 1024px)
- [ ] 터치 제스처 지원
- [ ] 반응형 이미지
- [ ] 크로스 브라우저 테스트
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2시간
**담당자:** -
**의존성:** #11-#13
**이슈 번호:** -

---

## Phase 3: Multimedia Features (0/8)

### #15 Drag and Drop File Upload Component
- [ ] react-dropzone 통합
- [ ] 드래그 앤 드롭 UI
- [ ] 다중 파일 선택
- [ ] 파일 미리보기
- [ ] 업로드 진행률 표시
- [ ] 에러 처리
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2-3시간
**담당자:** -
**의존성:** #10
**이슈 번호:** -

---

### #16 Image Gallery Component
- [ ] 이미지 그리드 레이아웃
- [ ] Lightbox 기능
- [ ] 이미지 확대/축소
- [ ] 썸네일 표시
- [ ] 반응형 그리드
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2시간
**담당자:** -
**의존성:** #13
**이슈 번호:** -

---

### #17 Video Player Component
- [ ] react-player 통합
- [ ] 비디오 컨트롤
- [ ] 자동재생 설정
- [ ] 음소거 토글
- [ ] 전체화면 지원
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2시간
**담당자:** -
**의존성:** #13
**이슈 번호:** -

---

### #18 Audio Player Component
- [ ] 오디오 플레이어 UI
- [ ] 재생/일시정지 컨트롤
- [ ] 진행바
- [ ] 볼륨 컨트롤
- [ ] 재생 시간 표시
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 1-2시간
**담당자:** -
**의존성:** #13
**이슈 번호:** -

---

### #19 File Download Component
- [ ] 다운로드 링크 컴포넌트
- [ ] 파일 정보 표시 (이름, 크기)
- [ ] 다운로드 아이콘
- [ ] 파일 타입별 아이콘
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 1시간
**담당자:** -
**의존성:** #13
**이슈 번호:** -

---

### #20 Media Manager Interface
- [ ] 미디어 관리 페이지
- [ ] 업로드 UI
- [ ] 미디어 브라우저
- [ ] 미디어 선택 기능
- [ ] 미디어 삭제 기능
- [ ] 검색 및 필터링
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 3시간
**담당자:** -
**의존성:** #15-#19
**이슈 번호:** -

---

### #21 Media API Integration
- [ ] GET /api/v1/media 엔드포인트
- [ ] DELETE /api/v1/media/{id} 엔드포인트
- [ ] 필터링 (타입별)
- [ ] 페이지네이션
- [ ] API 테스트 통과
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2시간
**담당자:** -
**의존성:** #1-#8
**이슈 번호:** -

---

### #22 Embed Media in Articles
- [ ] 마크다운에서 미디어 삽입 문법
- [ ] 이미지 삽입 ![alt](url)
- [ ] 비디오 삽입 커스텀 문법
- [ ] 오디오 삽입 커스텀 문법
- [ ] 미디어 미리보기 (편집기)
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2-3시간
**담당자:** -
**의존성:** #13, #16-#19
**이슈 번호:** -

---

## Phase 4: Content Management (0/7)

### #23 Markdown Editor with Preview
- [ ] 코드 에디터 컴포넌트
- [ ] 분할 화면 (편집/미리보기)
- [ ] 실시간 미리보기
- [ ] 마크다운 툴바
- [ ] 단축키 지원
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 3-4시간
**담당자:** -
**의존성:** #13
**이슈 번호:** -

---

### #24 Article Create/Edit Page
- [ ] 게시글 작성 페이지
- [ ] 게시글 수정 페이지
- [ ] 제목 입력 필드
- [ ] 내용 에디터 (마크다운)
- [ ] 태그 선택
- [ ] 임시저장/발행 버튼
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 3시간
**담당자:** -
**의존성:** #10, #23
**이슈 번호:** -

---

### #25 Table of Contents (TOC) Component
- [ ] 마크다운 헤딩에서 자동 TOC 생성
- [ ] 우측 사이드바 TOC UI
- [ ] Scroll Spy (현재 위치 하이라이트)
- [ ] TOC 항목 클릭 시 smooth scroll
- [ ] 모바일에서 접기/펼치기
- [ ] 중첩 헤딩 구조 지원 (H2, H3)
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2-3시간
**담당자:** -
**의존성:** #13
**이슈 번호:** -

---

### #26 Tag System
- [ ] GET /api/v1/tags 엔드포인트
- [ ] POST /api/v1/tags 엔드포인트
- [ ] 태그 선택 UI
- [ ] 태그별 필터링
- [ ] 태그 자동완성
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2-3시간
**담당자:** -
**의존성:** #4, #24
**이슈 번호:** -

---

### #27 Search Functionality
- [ ] GET /api/v1/articles/search 엔드포인트
- [ ] 전문 검색 구현
- [ ] 검색 UI (검색창)
- [ ] 검색 결과 페이지
- [ ] 하이라이팅
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 3시간
**담당자:** -
**의존성:** #4, #12
**이슈 번호:** -

---

### #28 SEO Meta Tags
- [ ] 동적 title 태그
- [ ] meta description
- [ ] Open Graph 태그
- [ ] Twitter Card 태그
- [ ] Canonical URL
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2시간
**담당자:** -
**의존성:** #13
**이슈 번호:** -

---

### #29 CORS Configuration
- [ ] CORS 미들웨어 설정 (port 3777 허용)
- [ ] 환경별 allowed origins
- [ ] Preflight 요청 처리
- [ ] 보안 헤더 설정
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 1시간
**담당자:** -
**의존성:** #1
**이슈 번호:** -

---

### #30 Markdown Sanitization
- [ ] 백엔드 nh3 sanitization
- [ ] 프론트엔드 rehype-sanitize
- [ ] XSS 방지 테스트
- [ ] 허용/차단 태그 설정
- [ ] 보안 테스트 통과
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 1-2시간
**담당자:** -
**의존성:** #1, #13
**이슈 번호:** -

---

## Phase 5: Polish & Advanced Features (0/6)

### #31 Performance Optimization - Backend
- [ ] 데이터베이스 인덱싱
- [ ] 쿼리 최적화
- [ ] Redis 캐싱
- [ ] 응답 시간 < 200ms (p95)
- [ ] 부하 테스트 통과
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2-3시간
**담당자:** -
**의존성:** 모든 백엔드 이슈
**이슈 번호:** -

---

### #32 Performance Optimization - Frontend
- [ ] 코드 스플리팅
- [ ] Lazy loading
- [ ] 번들 최적화
- [ ] 이미지 최적화
- [ ] FCP < 1.5s, TTI < 3s
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2-3시간
**담당자:** -
**의존성:** 모든 프론트엔드 이슈
**이슈 번호:** -

---

### #33 E2E Testing Suite
- [ ] 게시글 작성 플로우
- [ ] 파일 업로드 플로우
- [ ] 검색 플로우
- [ ] 모바일 시나리오
- [ ] 크로스 브라우저 테스트
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 3-4시간
**담당자:** -
**의존성:** 모든 기능
**이슈 번호:** -

---

### #34 CI/CD Pipeline
- [ ] GitHub Actions 워크플로우
- [ ] 백엔드 테스트 자동화
- [ ] 프론트엔드 테스트 자동화
- [ ] 린팅 자동화
- [ ] 배포 자동화
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2시간
**담당자:** -
**의존성:** #33
**이슈 번호:** -

---

### #35 Deployment Documentation
- [ ] Docker Compose 설정 (port 3777/8777)
- [ ] 환경 변수 문서화
- [ ] 배포 가이드 작성
- [ ] 백업 전략 문서
- [ ] 모니터링 설정
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2시간
**담당자:** -
**의존성:** 모든 기능
**이슈 번호:** -

---

### #36 Security Audit and Hardening
- [ ] 보안 스캔 실행
- [ ] 취약점 수정
- [ ] CSP 헤더 설정
- [ ] Rate limiting
- [ ] 보안 문서 작성
- [ ] TDD 문서 작성 완료

**상태:** ⏳ 대기중
**예상 시간:** 2-3시간
**담당자:** -
**의존성:** 모든 기능
**이슈 번호:** -

---

## 🎯 다음 액션 아이템

1. [ ] GitHub 이슈 35개 생성
2. [ ] Phase 1 상세 TDD 계획 생성
3. [ ] 개발 환경 설정 (Python, Node.js)
4. [ ] PostgreSQL 설치
5. [ ] 이슈 #1 시작

---

## 📝 참고 문서

- [기술 스택 분석](docs/00-tech-stack-analysis.md)
- [이슈 상세 명세](docs/01-issue-breakdown.md)
- [전체 이슈 요약](docs/02-complete-issue-summary.md)
- [GitHub 이슈 템플릿](docs/03-github-issue-templates.md)

---

## 💡 TDD 워크플로우

각 이슈는 다음 사이클을 따릅니다:

1. **🔴 RED**: 실패하는 테스트 작성
   - Commit: `test(#N): add test for [feature]`

2. **🟢 GREEN**: 테스트를 통과하는 최소 코드 작성
   - Commit: `feat(#N): implement [feature]`

3. **🔵 REFACTOR**: 코드 품질 개선
   - Commit: `refactor(#N): improve [aspect]`

4. **📝 DOCUMENT**: 완료 표시
   - `docs/[N]-[feature]-tdd.md` 업데이트
   - Commit: `docs(#N): mark [feature] complete`

---

## 📊 성공 기준

### 코드 품질
- ✅ 테스트 커버리지 > 80% (백엔드, 프론트엔드)
- ✅ TypeScript strict mode: 100%
- ✅ ESLint/Pylint 에러: 0개
- ✅ 심각한 보안 취약점: 0개

### 성능
- ✅ 백엔드 API 응답시간: < 200ms (p95)
- ✅ 프론트엔드 FCP: < 1.5s
- ✅ 프론트엔드 TTI: < 3s
- ✅ 파일 업로드: 최대 100MB 지원

### 확장성
- ✅ 10,000개 게시글 지원
- ✅ 100,000개 미디어 파일 지원
- ✅ 1,000명 동시 접속 처리
