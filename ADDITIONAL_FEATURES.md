# 추가 기능 제안 (2025 블로그 트렌드 기반)

> **조사 날짜:** 2025-11-17
> **기반 조사:** DEV.to, Medium, Hashnode, CodeSandbox, Pocket

---

## 🔍 조사 결과 요약

현대 테크 블로그 플랫폼(DEV.to, Hashnode, Medium)과 개발자 도구(CodeSandbox, Sandpack) 트렌드를 조사한 결과, 다음과 같은 핵심 기능들이 2025년 필수로 자리잡고 있습니다.

---

## 🎯 추천 추가 기능 (우선순위별)

### 🔥 Priority 1: 필수 추가 기능

> **제외된 기능:** Code Playground (Sandpack, CodeSandbox, Hashnode) - 불필요

#### 1. 📊 Reading Progress Bar & Analytics
**설명:** 게시글 상단에 읽기 진행률 표시 + 예상 읽기 시간

**주요 기능:**
- **Progress Bar**
  - 스크롤에 따라 진행률 표시 (0-100%)
  - 상단 고정 또는 헤더에 통합
  - 커스텀 색상 및 두께 설정
  - 부드러운 애니메이션

- **Reading Time Estimation**
  - 단어 수 기반 계산 (200-250 단어/분)
  - 이미지 viewing 시간 추가 (첫 이미지 12초, 이후 11초씩 감소)
  - 코드 블록 읽기 시간 추가 (일반 텍스트의 1.5배)
  - 게시글 카드 및 상세페이지에 표시

**구현 우선순위:** ⭐⭐⭐⭐⭐
**예상 작업 시간:** 2-3시간
**기술 스택:** React hooks (useScrollProgress), Intersection Observer API

**장점:**
- 사용자 engagement 증가 (진행 상황 가시성)
- 낮은 bounce rate (Google SEO 긍정적 신호)
- 긴 세션 시간 (평균 8분 → 검색 순위 상승)

---

#### 2. 🔖 Bookmarking & Reading List
**설명:** 사용자가 나중에 읽을 게시글을 저장하는 기능

**주요 기능:**
- **Bookmark 기능**
  - 게시글 카드 및 상세 페이지에 북마크 버튼
  - 로그인 없이 사용 (localStorage 저장)
  - 로그인 시 서버에 동기화 (선택사항)
  - 북마크 추가/제거 애니메이션

- **Reading List 페이지**
  - 북마크한 게시글 목록
  - 정렬: 최신순, 오래된순, 제목순
  - 일괄 삭제 기능
  - 읽음/안읽음 상태 관리

- **Browser Extension (선택사항)**
  - Chrome/Firefox 확장 프로그램
  - 외부 사이트에서도 북마크 가능

**구현 우선순위:** ⭐⭐⭐⭐
**예상 작업 시간:** 3-4시간
**기술 스택:** localStorage, React Context/Zustand, (optional) Backend API

**장점:**
- 사용자 retention 증가
- 재방문율 상승
- Pocket, DEV.to 등 표준 기능
- 오프라인 읽기 목록 (PWA와 결합 시)

---

### ⚡ Priority 2: 중요 추가 기능

#### 3. 🧠 AI-Powered Semantic Search (VectorDB + LLM)
**설명:** 게시글을 벡터 임베딩으로 변환하여 의미 기반 검색 제공

**주요 기능:**
- **Vector Database Integration**
  - **VectorDB 옵션:**
    - Pinecone (Serverless, 무료 tier)
    - Weaviate (Self-hosted, 오픈소스)
    - Qdrant (Self-hosted, Python 친화적)
    - PostgreSQL + pgvector (기존 DB 확장)

  - **Article Embedding Pipeline**
    - 게시글 발행 시 자동 임베딩 생성
    - 제목 + 내용 + 태그 결합 벡터화
    - 업데이트 시 벡터 재생성

- **Local LLM Integration (/mnt/storage/models/)**
  - **Embedding Models (로컬 무료):**
    - sentence-transformers/paraphrase-multilingual-mpnet-base-v2 (한국어 우수)
    - intfloat/multilingual-e5-large (최신, 한국어 지원)
    - BAAI/bge-m3 (다국어 최강)

  - **LLM for Q&A (로컬 추론):**
    - gemma2-9b (/mnt/storage/models/)
    - Llama-3-8B (대안)
    - Qwen2-7B (한국어 강점)

  - **Search Query Processing**
    - 자연어 검색 쿼리 → 벡터 변환 (로컬)
    - 코사인 유사도 기반 관련 게시글 검색
    - 하이브리드 검색 (키워드 + 시맨틱)

- **Search Features**
  - **Semantic Search UI**
    - "React hooks 사용법" → 관련 글 찾기
    - "성능 최적화 방법" → 유사 주제 글 추천
    - 오타 허용 (의미 기반 검색)

  - **Related Articles (추천 시스템)**
    - 현재 게시글과 유사한 글 자동 추천
    - 사이드바에 "비슷한 글" 표시
    - 벡터 유사도 상위 3-5개

  - **Ask Questions (gemma2-9b 활용)**
    - "이 블로그에서 TypeScript 관련 글은?"
    - 로컬 LLM이 검색 결과를 요약해서 답변
    - RAG (Retrieval-Augmented Generation) 패턴

- **Backend Architecture (완전 로컬, 비용 0원)**
  ```python
  # 게시글 발행 시
  POST /api/v1/articles
  ↓
  1. 게시글 저장 (PostgreSQL)
  2. 임베딩 생성 (로컬 sentence-transformers)
  3. VectorDB 저장 (Qdrant Docker or pgvector)

  # 검색 시
  GET /api/v1/search/semantic?q=query
  ↓
  1. 쿼리 임베딩 생성 (로컬 모델)
  2. VectorDB 유사도 검색 (top-k)
  3. 결과 반환 (with score)

  # Q&A 시 (optional)
  POST /api/v1/ask
  ↓
  1. 쿼리 임베딩 생성
  2. VectorDB에서 관련 글 검색
  3. gemma2-9b로 답변 생성 (RAG)
  4. 생성된 답변 + 출처 반환
  ```

- **Hybrid Search (최고의 방식)**
  - 키워드 검색 (PostgreSQL Full-text)
  - 시맨틱 검색 (VectorDB)
  - 결과 병합 (Reciprocal Rank Fusion)
  - 정확도 + 의미 모두 고려

**구현 우선순위:** ⭐⭐⭐⭐⭐
**예상 작업 시간:** 6-8시간
**기술 스택 (완전 로컬, 비용 0원):**
- **VectorDB:** Qdrant (Docker) or pgvector (PostgreSQL 확장)
- **Embedding:** sentence-transformers (multilingual-e5-large)
- **LLM:** gemma2-9b (/mnt/storage/models/)
- **Backend:** FastAPI async endpoints
- **추론:** llama-cpp-python or vLLM

**하드웨어 요구사항:**
- **임베딩 모델:** CPU 가능 (512MB RAM)
- **gemma2-9b 추론:**
  - GPU: RTX 3060 이상 (12GB VRAM 권장)
  - CPU: 가능하지만 느림 (16GB+ RAM)
  - 양자화 (4-bit): 5-6GB VRAM으로 가능

**비용:** **완전 무료** (로컬 인프라 활용)

**장점:**
- ✅ 키워드 검색보다 월등히 우수
- ✅ "React state management" 검색 시 "useState", "Redux", "Zustand" 글 모두 검색
- ✅ 추천 시스템 자동 구현 (비슷한 글)
- ✅ RAG 기반 Q&A (gemma2-9b)
- ✅ **완전 무료** (클라우드 API 비용 0원)
- ✅ 데이터 프라이버시 (로컬 처리)
- ✅ SEO 유지 (기존 검색 병행)
- ✅ 최신 블로그 트렌드 (Notion AI, Perplexity 스타일)

**기술적 고려사항:**
- **임베딩 모델 (로컬):**
  - 한국어: intfloat/multilingual-e5-large (추천)
  - 영어: BAAI/bge-large-en-v1.5
  - 다국어: BAAI/bge-m3

- **VectorDB 선택:**
  - 소규모 (< 1만 글): pgvector (PostgreSQL 확장, 간편)
  - 중대규모 (1만-10만 글): Qdrant (Docker self-hosted)
  - 대규모 (10만+ 글): Qdrant with quantization

- **LLM 추론 최적화:**
  - vLLM (고속 추론)
  - llama-cpp-python (CPU/GPU 유연성)
  - 4-bit 양자화 (GPTQ/AWQ)

- **검색 속도 (로컬):**
  - VectorDB 쿼리: ~50ms (Qdrant)
  - 임베딩 생성: ~100-200ms (CPU/GPU)
  - LLM 답변 생성 (optional): ~2-5초 (gemma2-9b)
  - 총 응답 시간: < 300ms (검색만) / < 5s (Q&A 포함)

---

#### 4. 👍 Reactions & Emoji Responses
**설명:** DEV.to 스타일의 이모지 리액션 기능

**주요 기능:**
- **Multiple Reaction Types**
  - ❤️ Like (좋아요)
  - 🦄 Unicorn (Amazing!)
  - 🔖 Bookmark (저장)
  - 🔥 Fire (핫한 글!)
  - 💯 100 (완벽!)

- **Reaction 집계**
  - 게시글별 리액션 카운트
  - 인기 게시글 정렬 (리액션 기준)
  - 실시간 업데이트 (WebSocket or Polling)

- **사용자 리액션 기록**
  - 로그인 없이 가능 (익명)
  - IP 기반 중복 방지
  - 로그인 시 프로필에 기록

**구현 우선순위:** ⭐⭐⭐⭐
**예상 작업 시간:** 3-4시간
**기술 스택:** Backend API, Redis (rate limiting), React animations

**장점:**
- 댓글보다 낮은 진입 장벽
- 빠른 피드백 루프
- 커뮤니티 engagement 증가
- DEV.to 검증된 UX 패턴

---

#### 5. 📱 Social Share Buttons (Advanced)
**설명:** 강화된 소셜 미디어 공유 기능

**주요 기능:**
- **Share Targets**
  - Twitter/X (자동 해시태그 추가)
  - LinkedIn (프로페셔널 네트워크)
  - Facebook
  - Reddit (subreddit 추천)
  - Hacker News
  - Dev.to
  - Copy link (클립보드)

- **Share Analytics**
  - 공유 횟수 추적
  - 플랫폼별 분석
  - 인기 게시글 식별

- **Native Share API**
  - 모바일 브라우저 네이티브 공유 메뉴
  - Web Share API 활용

**구현 우선순위:** ⭐⭐⭐⭐
**예상 작업 시간:** 2-3시간
**기술 스택:** Web Share API, Social meta tags, Analytics

**장점:**
- 트래픽 증가 (소셜 북마킹 11% 기여)
- 백링크 생성 (SEO)
- 바이럴 가능성
- 평균 세션 8분 유지

---

#### 6. 🎨 Syntax Highlighting Themes
**설명:** 코드 블록 테마 선택 기능

**주요 기능:**
- **Multiple Themes**
  - VS Code Dark+ (기본)
  - GitHub Light/Dark
  - Dracula
  - One Dark Pro
  - Nord
  - Monokai

- **User Preference**
  - 테마 선택 저장 (localStorage)
  - 다크모드 자동 매칭
  - 게시글별 커스텀 테마 (작성자 선택)

- **Line Highlighting**
  - 특정 라인 하이라이트 (예: `{3-5}`)
  - 주석 강조
  - Diff 표시 (추가/삭제)

**구현 우선순위:** ⭐⭐⭐
**예상 작업 시간:** 2-3시간
**기술 스택:** Shiki themes, remark-code-titles

**장점:**
- 가독성 향상
- 개인화 경험
- 개발자 친화적

---

### 🚀 Priority 3: 고급 기능

#### 7. 🗨️ Comments System (Giscus)
**설명:** GitHub Discussions 기반 댓글 시스템

**주요 기능:**
- **Giscus Integration**
  - GitHub 계정으로 로그인
  - Markdown 지원
  - 스레드/대댓글
  - 리액션 (👍👎❤️😄 등)

- **Moderation**
  - GitHub Discussions 관리 도구 활용
  - 스팸 필터링
  - 댓글 신고 기능

- **Alternatives**
  - Utterances (simpler, issues-based)
  - Disqus (popular but ads)
  - Commento (privacy-focused)

**구현 우선순위:** ⭐⭐⭐
**예상 작업 시간:** 2-3시간
**기술 스택:** Giscus, GitHub API

**장점:**
- 무료 (GitHub 인프라)
- 스팸 최소화 (GitHub 계정 필요)
- 데이터 소유권 (GitHub repo)
- SEO 긍정적 (댓글 = 콘텐츠)

---

#### 8. 📧 Newsletter Subscription
**설명:** 이메일 뉴스레터 구독 기능

**주요 기능:**
- **Subscription Form**
  - 푸터 또는 게시글 하단 위치
  - 이메일 입력 및 검증
  - Double opt-in 확인 이메일

- **Email Service Integration**
  - Mailchimp
  - ConvertKit
  - Buttondown (개발자 친화적)
  - Substack (embeddable)

- **Newsletter Types**
  - 새 게시글 알림
  - 주간 다이제스트
  - 인기 게시글 요약

**구현 우선순위:** ⭐⭐⭐
**예상 작업 시간:** 3-4시간
**기술 스택:** Email service API, Backend subscription endpoint

**장점:**
- 직접 커뮤니케이션 채널
- 재방문 유도
- Audience building
- Medium, Hashnode 표준 기능

---

#### 9. 🏆 Series & Article Collections
**설명:** 연속된 게시글을 시리즈로 묶는 기능

**주요 기능:**
- **Series Management**
  - 시리즈 생성 (제목, 설명)
  - 게시글 순서 지정
  - 시리즈 커버 이미지

- **Series Navigation**
  - 이전/다음 게시글 링크
  - 시리즈 목차 (TOC)
  - 진행률 표시 (3/10)

- **Series Page**
  - 시리즈 랜딩 페이지
  - 완독률 통계
  - 시리즈별 구독 (선택사항)

**구현 우선순위:** ⭐⭐⭐
**예상 작업 시간:** 4-5시간
**기술 스택:** Backend series model, Series navigation component

**장점:**
- 긴 튜토리얼 구조화
- Binge reading 유도
- DEV.to, Hashnode 검증된 기능
- 세션 시간 증가

---

#### 10. 🔔 Web Push Notifications (PWA)
**설명:** 새 게시글 알림 푸시 (Progressive Web App)

**주요 기능:**
- **Push Notifications**
  - 브라우저 알림 권한 요청
  - 새 게시글 발행 시 푸시
  - 태그별 구독 (선택적 알림)

- **PWA Features**
  - Service Worker
  - 오프라인 읽기
  - 홈 화면 추가
  - 앱처럼 실행

- **Notification Preferences**
  - 알림 ON/OFF
  - 빈도 설정 (즉시, 일간, 주간)
  - 관심 태그 선택

**구현 우선순위:** ⭐⭐
**예상 작업 시간:** 6-8시간
**기술 스택:** Service Worker, Web Push API, Notification API, Backend push service

**장점:**
- 모바일 앱 수준 경험
- 재방문율 대폭 증가
- 오프라인 지원
- 트렌드: PWA 표준화

---

### 💡 Priority 4: Nice-to-Have 기능

#### 11. 📈 Article Analytics Dashboard
**설명:** 게시글별 상세 분석 대시보드 (작성자용)

**주요 기능:**
- **View Statistics**
  - 일일/주간/월간 조회수
  - 실시간 활성 독자 수
  - 평균 읽기 시간
  - Bounce rate

- **Engagement Metrics**
  - 리액션 수 (타입별)
  - 댓글 수
  - 공유 횟수
  - 북마크 수

- **Traffic Sources**
  - Referrer 분석 (Google, Twitter, Direct 등)
  - 검색 키워드 (Google Search Console 연동)
  - 지역별 분포

- **Charts & Graphs**
  - 시계열 차트 (Chart.js/Recharts)
  - 히트맵 (시간대별 활동)
  - Comparison view (게시글 간 비교)

**구현 우선순위:** ⭐⭐
**예상 작업 시간:** 8-10시간
**기술 스택:** Backend analytics service, Chart.js, Google Analytics API

**장점:**
- 콘텐츠 최적화 인사이트
- 작성자 동기부여
- Medium, Hashnode 제공 기능

---

#### 12. 🤖 AI-Powered Features
**설명:** AI 기반 콘텐츠 보강 기능

**주요 기능:**
- **Auto-Generate Summary**
  - GPT API로 게시글 요약 자동 생성
  - Meta description 제안
  - 트위터 길이 요약 (140자)

- **Smart Tag Suggestions**
  - 콘텐츠 분석 후 태그 추천
  - 기존 태그와 매칭

- **Grammar & Style Checker**
  - Grammarly 스타일 체크
  - 가독성 점수
  - SEO 개선 제안

- **Code Explanation**
  - 코드 블록 설명 자동 생성
  - 초보자 친화적 주석

**구현 우선순위:** ⭐
**예상 작업 시간:** 10-15시간
**기술 스택:** OpenAI API, Anthropic Claude API, NLP libraries

**장점:**
- 작성 시간 단축
- 품질 향상
- SEO 최적화
- 미래 트렌드

---

#### 13. 🎤 Text-to-Speech (Audio Version)
**설명:** 게시글 음성 버전 제공

**주요 기능:**
- **TTS Engine**
  - Google Cloud TTS or Amazon Polly
  - 자연스러운 음성 합성
  - 여러 언어/음성 지원

- **Audio Player**
  - 게시글 상단에 오디오 플레이어
  - 재생/일시정지/속도 조절
  - 백그라운드 재생

- **Accessibility**
  - 시각 장애인 접근성
  - 멀티태스킹 (운전 중 청취 등)

**구현 우선순위:** ⭐
**예상 작업 시간:** 5-6시간
**기술 스택:** Google Cloud TTS API, Audio player component

**장점:**
- 접근성 향상
- 새로운 소비 방식 제공
- Premium 기능 (Hashnode 제공)

---

## 📊 기능 우선순위 요약표

| 우선순위 | 기능 | 예상 시간 | 구현 난이도 | 사용자 가치 | ROI |
|---------|------|-----------|------------|------------|-----|
| P1 | Reading Progress Bar | 2-3h | Low | ⭐⭐⭐⭐⭐ | 높음 |
| P1 | Bookmarking & Reading List | 3-4h | Low | ⭐⭐⭐⭐ | 높음 |
| P2 | **AI Semantic Search (VectorDB)** | 6-8h | Medium | ⭐⭐⭐⭐⭐ | **매우 높음** |
| P2 | Reactions & Emoji | 3-4h | Medium | ⭐⭐⭐⭐ | 높음 |
| P2 | Social Share (Advanced) | 2-3h | Low | ⭐⭐⭐⭐ | 높음 |
| P2 | Syntax Highlight Themes | 2-3h | Low | ⭐⭐⭐ | 중간 |
| P3 | Comments (Giscus) | 2-3h | Low | ⭐⭐⭐ | 중간 |
| P3 | Newsletter Subscription | 3-4h | Medium | ⭐⭐⭐ | 중간 |
| P3 | Series & Collections | 4-5h | Medium | ⭐⭐⭐ | 중간 |
| P3 | PWA Push Notifications | 6-8h | High | ⭐⭐ | 낮음 |
| P4 | Analytics Dashboard | 8-10h | High | ⭐⭐ | 낮음 |
| P4 | AI Content Generation | 10-15h | High | ⭐⭐ | 낮음 |
| P4 | Text-to-Speech | 5-6h | Medium | ⭐ | 낮음 |

---

## 🎯 추천 구현 순서

### Phase A: MVP 완료 후 즉시 추가 (필수)
1. **Reading Progress Bar** (2-3h) - SEO 및 engagement에 즉시 효과
2. **Bookmarking** (3-4h) - 사용자 retention 핵심
3. **Social Share** (2-3h) - 트래픽 증대

**총 작업 시간:** 7-10시간

---

### Phase B: AI & 커뮤니티 기능 강화
4. **AI Semantic Search (VectorDB + LLM)** (6-8h) - 최고의 차별화 포인트, 추천 시스템 포함
5. **Reactions** (3-4h) - 빠른 피드백 루프
6. **Comments (Giscus)** (2-3h) - 커뮤니티 형성

**총 작업 시간:** 11-15시간

---

### Phase C: 콘텐츠 조직화
7. **Series & Collections** (4-5h) - 긴 튜토리얼 구조화
8. **Syntax Themes** (2-3h) - 가독성 향상
9. **Newsletter** (3-4h) - Audience building

**총 작업 시간:** 9-12시간

---

### Phase D: Advanced (선택적)
10. **PWA & Push** (6-8h)
11. **Analytics Dashboard** (8-10h)
12. **AI Features** (10-15h)
13. **Text-to-Speech** (5-6h)

**총 작업 시간:** 29-39시간

---

## 🔍 경쟁 플랫폼 비교

| 기능 | DEV.to | Medium | 우리 블로그 (계획) |
|------|--------|--------|-------------------|
| Reading Progress | ❌ | ✅ | ✅ (P1) |
| **AI Semantic Search** | ❌ | ❌ | **✅ (P2)** |
| Bookmarking | ✅ | ✅ | ✅ (P1) |
| Reactions | ✅ | ❌ | ✅ (P2) |
| Social Share | ✅ | ✅ | ✅ (P2) |
| Comments | ✅ | ✅ | ✅ (P3) |
| Series | ✅ | ❌ | ✅ (P3) |
| Newsletter | ✅ | ✅ | ✅ (P3) |
| Custom Domain | ❌ | ❌ | ✅ |
| Full Ownership | ❌ | ❌ | ✅ |
| Multimedia | 기본 | 기본 | **고급** |

---

## 💰 비용 고려사항

### 무료 옵션 (완전 로컬)
- **AI Semantic Search:** ⭐⭐⭐⭐⭐
  - pgvector (PostgreSQL 확장, 무료)
  - sentence-transformers (로컬 임베딩, 무료)
  - Qdrant (Docker self-hosted, 무료)
  - gemma2-9b (/mnt/storage/models/, 무료)
  - **총 비용: 0원** (전기세 제외)
- **Comments:** Giscus (GitHub 무료)
- **Analytics:** Google Analytics (무료)
- **Bookmarking:** localStorage (무료)

### 유료 옵션 (선택사항, 불필요)
- **AI Semantic Search (Cloud):**
  - OpenAI Embeddings ($0.02/1M tokens)
  - Pinecone Serverless ($0.096/GB/월)
  - ⚠️ 로컬 솔루션으로 충분하므로 불필요
- **Newsletter:**
  - Buttondown ($9/월, 1000 구독자)
  - Mailchimp (2000 구독자까지 무료)
- **Push Notifications:**
  - OneSignal (10,000 subscribers 무료)
  - Firebase Cloud Messaging (무료)
- **AI Content Generation:**
  - OpenAI API ($0.002/1k tokens)
  - Claude API (유사 가격)
- **TTS:**
  - Google Cloud TTS ($4/1M characters)

---

## 📚 참고 자료

### 조사한 플랫폼
1. **DEV.to** - 커뮤니티 중심, 리액션 시스템
2. **Medium** - 클린 UI, reading time, social sharing
3. **Pocket** - Reading list, 나중에 읽기
4. **VectorDB 솔루션** - Qdrant, Pinecone, pgvector
5. **Embedding 모델** - OpenAI, sentence-transformers, Cohere

### 트렌드 키워드 (2025)
- **AI Semantic Search** (VectorDB + LLM)
- Progressive Web Apps (PWA)
- AI-powered content creation
- Privacy-first analytics
- Community-driven platforms
- Ownership & custom domains
- Hybrid search (키워드 + 의미 기반)

---

## ✅ 결론 및 추천

### 즉시 구현 추천 (Phase A)
1. **Reading Progress Bar** - 최소 노력으로 최대 효과
2. **Bookmarking** - 재방문율 증가 핵심
3. **Social Share** - 트래픽 확보

### 차별화 핵심 (Phase B) ⭐⭐⭐⭐⭐
4. **AI Semantic Search (VectorDB + 로컬 LLM)** - 최고의 차별화 포인트
   - DEV.to, Medium에도 없는 기능
   - 키워드 검색보다 월등히 우수
   - 추천 시스템 자동 구현
   - **완전 무료** (pgvector + sentence-transformers + gemma2-9b)
   - RAG 기반 Q&A 기능 포함

### 장기 투자 (Phase C-D)
- Series, Newsletter, Analytics는 콘텐츠가 충분히 쌓인 후 추가
- AI Content Generation/TTS는 예산과 필요성 검토 후 결정

**총 추가 개발 시간:** 18-25시간 (Phase A-B, Code Playground 제외)
**ROI:** 매우 높음 (사용자 engagement, retention, traffic 모두 증대)

### 🎯 핵심 추천: AI Semantic Search (로컬 LLM)
- **차별화:** DEV.to, Medium, Hashnode 모두 제공하지 않음
- **사용자 가치:**
  - 의미 기반 검색 (오타 허용, 유사 주제 자동 검색)
  - 자동 추천 시스템 (비슷한 글)
  - RAG 기반 Q&A (gemma2-9b로 답변 생성)
- **비용:** **0원** (pgvector + sentence-transformers + gemma2-9b 로컬)
- **구현 난이도:** Medium (6-8시간)
- **ROI:** ⭐⭐⭐⭐⭐ (매우 높음)
- **추가 장점:** 데이터 프라이버시, API 제한 없음
