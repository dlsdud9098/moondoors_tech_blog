# Tech Blog - Issue Breakdown & Implementation Plan

## Overview

This document contains the complete breakdown of the tech blog project into manageable, testable issues following TDD principles. Each issue is designed to be completed in 1-2 hours and has clear acceptance criteria.

## Issue Summary

Total issues: 24 (grouped into 4 phases)

- **Phase 1 - Foundation:** 5 issues (Setup & Infrastructure)
- **Phase 2 - Core Features:** 7 issues (Essential Blog Functionality)
- **Phase 3 - Essential Features:** 6 issues (Enhanced User Experience)
- **Phase 4 - Polish & Enhancement:** 6 issues (Advanced Features)

---

## Phase 1: Foundation (Issues #1-#5)

### Issue #1: Project Setup with Next.js, TypeScript, and Testing Infrastructure

**Type:** feature
**Area:** infrastructure
**Complexity:** low
**Estimated Time:** 1-2 hours

#### Description
Initialize Next.js 15 project with TypeScript, configure essential development tools (ESLint, Prettier), and set up testing infrastructure with Vitest and Playwright. This provides the foundation for TDD development.

#### Completion Criteria
- [ ] Next.js 15+ project initialized with TypeScript
- [ ] Tailwind CSS 4 configured
- [ ] ESLint and Prettier configured
- [ ] Vitest configured for unit/integration tests
- [ ] Playwright configured for E2E tests
- [ ] Git hooks configured with Husky and lint-staged
- [ ] All configuration tests pass
- [ ] README.md documents setup process

#### Implementation Notes

**Files to Create:**
- `package.json` - Dependencies and scripts
- `next.config.ts` - Next.js configuration
- `tsconfig.json` - TypeScript configuration
- `vitest.config.ts` - Vitest test configuration
- `playwright.config.ts` - Playwright E2E configuration
- `.eslintrc.json` - ESLint rules
- `.prettierrc` - Prettier configuration
- `.gitignore` - Git ignore patterns
- `README.md` - Project documentation

**Key Dependencies:**
```json
{
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@playwright/test": "^1.40.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/user-event": "^14.5.0",
    "@vitejs/plugin-react": "^4.2.0",
    "vitest": "^1.0.0",
    "typescript": "^5.3.0",
    "tailwindcss": "^4.0.0",
    "eslint": "^8.55.0",
    "prettier": "^3.1.0",
    "husky": "^8.0.0",
    "lint-staged": "^15.2.0"
  }
}
```

**Patterns from Research:**
- Use Vitest instead of Jest (3.8x faster, better ESM support)
- Enable TypeScript strict mode from the start
- Configure Playwright for cross-browser E2E testing
- Set up pre-commit hooks to enforce code quality

**Testing Strategy:**
- Verify all tools run without errors
- Test that TypeScript compilation works
- Ensure ESLint and Prettier can run
- Confirm git hooks execute on commit

#### Dependencies
- [ ] None (first issue)

---

### Issue #2: Directory Structure and Project Organization

**Type:** feature
**Area:** infrastructure
**Complexity:** low
**Estimated Time:** 1 hour

#### Description
Create the complete project directory structure following Next.js App Router conventions and TDD best practices. Establish clear separation between source code, tests, content, and documentation.

#### Completion Criteria
- [ ] All required directories created
- [ ] Directory structure documented
- [ ] TypeScript path aliases configured
- [ ] Import resolution tests pass
- [ ] Directory structure validation tests pass

#### Implementation Notes

**Directories to Create:**
```
src/
├── app/                    # Next.js App Router
├── components/             # React components
├── lib/                    # Utilities and helpers
└── types/                  # TypeScript type definitions

tests/
├── unit/                   # Unit tests
├── integration/            # Integration tests
└── e2e/                    # End-to-end tests

content/
└── posts/                  # Markdown blog posts

public/
├── images/                 # Static images
└── fonts/                  # Custom fonts

docs/                       # TDD plans and documentation
```

**Files to Modify:**
- `tsconfig.json` - Add path aliases (@/components, @/lib, @/types)
- `vitest.config.ts` - Configure test file patterns
- `docs/02-directory-structure.md` - Document structure

**Patterns from Research:**
- Separate concerns (app, components, lib, types)
- Dedicated test directories by type
- Content in separate directory for clear separation
- Use TypeScript path aliases for clean imports

**Testing Strategy:**
- Test that imports resolve correctly with aliases
- Verify directory structure matches documentation
- Test file organization conventions

#### Dependencies
- [ ] Issue #1 (Project setup must be complete)

---

### Issue #3: Markdown Processing Pipeline with Security

**Type:** feature
**Area:** content
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Implement secure markdown processing using react-markdown with remark/rehype plugins. Include XSS prevention through proper sanitization and secure link handling.

#### Completion Criteria
- [ ] Markdown to HTML conversion works correctly
- [ ] Frontmatter parsing implemented
- [ ] XSS prevention measures in place
- [ ] External links handled securely
- [ ] GitHub Flavored Markdown supported
- [ ] All security tests pass
- [ ] Markdown rendering tests pass with various edge cases

#### Implementation Notes

**Files to Create:**
- `src/lib/markdown.ts` - Markdown processing utilities
- `src/types/post.ts` - Post type definitions
- `tests/unit/markdown.test.ts` - Markdown processing tests

**Key Dependencies:**
```json
{
  "dependencies": {
    "react-markdown": "^9.0.0",
    "remark-gfm": "^4.0.0",
    "remark-frontmatter": "^5.0.0",
    "gray-matter": "^4.0.3",
    "rehype-sanitize": "^6.0.0",
    "remark-external-links": "^9.0.0"
  }
}
```

**Security Patterns from Research:**
- Use react-markdown (secure by default - escapes HTML)
- Apply sanitization AFTER markdown processing
- Use remark-external-links for secure link handling
- Validate and filter dangerous protocols (javascript:, vbscript:)
- Implement server-side validation

**Functions to Implement:**
```typescript
// Parse markdown file with frontmatter
function parseMarkdown(content: string): { data: FrontMatter; content: string }

// Convert markdown to safe HTML
function markdownToHtml(markdown: string): string

// Sanitize links and remove dangerous protocols
function sanitizeContent(html: string): string
```

**Testing Strategy:**
- Test XSS attack vectors (script tags, event handlers)
- Test dangerous protocols (javascript:, vbscript:, file:)
- Test GitHub Flavored Markdown features (tables, task lists)
- Test frontmatter parsing with various formats
- Test edge cases (empty content, malformed markdown)

#### Dependencies
- [ ] Issue #1 (Testing infrastructure needed)

---

### Issue #4: File System Content Loading

**Type:** feature
**Area:** content
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Implement file system utilities to read and parse markdown blog posts from the content directory. Include sorting, filtering, and caching for optimal performance.

#### Completion Criteria
- [ ] Read all posts from content directory
- [ ] Parse frontmatter from markdown files
- [ ] Sort posts by date (newest first)
- [ ] Filter draft posts in production
- [ ] Cache parsed content for performance
- [ ] All file system tests pass
- [ ] Error handling for missing/malformed files

#### Implementation Notes

**Files to Create:**
- `src/lib/posts.ts` - Post loading utilities
- `src/types/post.ts` - Enhanced post types
- `tests/unit/posts.test.ts` - Post loading tests
- `tests/fixtures/sample-posts.md` - Test fixtures

**Functions to Implement:**
```typescript
// Get all published posts
function getAllPosts(): Post[]

// Get single post by slug
function getPostBySlug(slug: string): Post | null

// Get posts filtered by tag
function getPostsByTag(tag: string): Post[]

// Get recent posts (limit N)
function getRecentPosts(limit: number): Post[]
```

**Frontmatter Schema:**
```yaml
---
title: "Post Title"
date: "2025-01-15"
description: "Brief description"
tags: ["nextjs", "typescript", "testing"]
author: "Author Name"
draft: false
---
```

**Patterns from Research:**
- Use Node.js fs module for file reading
- Implement caching to avoid repeated file reads
- Sort by date for consistent ordering
- Handle edge cases (missing files, malformed frontmatter)

**Testing Strategy:**
- Test with sample markdown files
- Test sorting and filtering logic
- Test error handling for invalid files
- Test caching behavior
- Test draft post filtering

#### Dependencies
- [ ] Issue #3 (Markdown processing needed)

---

### Issue #5: Basic SEO Meta Tags Component

**Type:** feature
**Area:** seo
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Create reusable SEO component for managing meta tags, Open Graph tags, and Twitter Cards. Implement with Next.js Metadata API for optimal SEO.

#### Completion Criteria
- [ ] SEO component generates correct meta tags
- [ ] Open Graph tags implemented
- [ ] Twitter Card tags implemented
- [ ] JSON-LD structured data for BlogPosting
- [ ] All SEO tests pass
- [ ] Validates with SEO testing tools

#### Implementation Notes

**Files to Create:**
- `src/lib/seo.ts` - SEO utilities
- `src/types/seo.ts` - SEO type definitions
- `tests/unit/seo.test.ts` - SEO generation tests

**Functions to Implement:**
```typescript
// Generate metadata for blog post
function generatePostMetadata(post: Post): Metadata

// Generate JSON-LD structured data
function generateBlogPostingSchema(post: Post): WithContext<BlogPosting>

// Generate sitemap data
function generateSitemapData(posts: Post[]): SitemapItem[]
```

**Meta Tags to Include:**
- Basic meta tags (title, description)
- Open Graph (og:title, og:description, og:image, og:type)
- Twitter Cards (twitter:card, twitter:title, twitter:description)
- Canonical URLs
- Language tags

**Patterns from Research:**
- Use Next.js Metadata API (not next-seo for App Router)
- Implement BlogPosting schema with JSON-LD
- Include all required Open Graph tags
- Test meta tags in various social platforms

**Testing Strategy:**
- Test metadata generation for various post types
- Test JSON-LD schema validation
- Test Open Graph tag completeness
- Test Twitter Card formatting
- Verify canonical URLs are correct

#### Dependencies
- [ ] Issue #4 (Post data structure needed)

---

## Phase 2: Core Features (Issues #6-#12)

### Issue #6: Home Page with Article Listing

**Type:** feature
**Area:** ui
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Create home page that displays list of recent blog posts with title, excerpt, date, and tags. Implement responsive grid layout using Tailwind CSS.

#### Completion Criteria
- [ ] Home page displays all published posts
- [ ] Posts sorted by date (newest first)
- [ ] Each post card shows: title, date, excerpt, tags
- [ ] Responsive grid layout (1 col mobile, 2-3 cols desktop)
- [ ] Loading states handled
- [ ] All component tests pass
- [ ] Playwright E2E test verifies listing

#### Implementation Notes

**Files to Create:**
- `src/app/page.tsx` - Home page
- `src/components/PostCard.tsx` - Post card component
- `src/components/PostList.tsx` - Post list component
- `tests/unit/PostCard.test.tsx` - Component tests
- `tests/e2e/home.spec.ts` - E2E tests

**Components to Build:**
```typescript
// Post card showing preview
<PostCard post={post} />

// Post list container
<PostList posts={posts} />
```

**Patterns from Research:**
- Mobile-first responsive design
- Use semantic HTML for SEO
- Implement proper heading hierarchy
- Lazy load images below fold

**Testing Strategy:**
- Test post card renders all required data
- Test list renders correct number of posts
- Test responsive breakpoints
- Test empty state (no posts)
- E2E test navigation from list to post

#### Dependencies
- [ ] Issue #4 (Post loading)
- [ ] Issue #5 (SEO metadata)

---

### Issue #7: Article Detail Page with Markdown Rendering

**Type:** feature
**Area:** ui
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Implement individual article detail pages with full markdown rendering, including typography, images, and content layout. Use dynamic routing with slug parameter.

#### Completion Criteria
- [ ] Dynamic route `/blog/[slug]` works
- [ ] Full markdown content renders correctly
- [ ] Typography styles applied
- [ ] Images render with proper sizing
- [ ] 404 page for invalid slugs
- [ ] All rendering tests pass
- [ ] E2E test verifies full article display

#### Implementation Notes

**Files to Create:**
- `src/app/blog/[slug]/page.tsx` - Article page
- `src/components/MarkdownContent.tsx` - Markdown renderer
- `src/components/ArticleHeader.tsx` - Article header component
- `tests/unit/MarkdownContent.test.tsx` - Rendering tests
- `tests/e2e/article.spec.ts` - E2E tests

**Components to Build:**
```typescript
// Article header with metadata
<ArticleHeader title={post.title} date={post.date} tags={post.tags} />

// Markdown content renderer
<MarkdownContent content={post.content} />
```

**Patterns from Research:**
- Use Next.js generateStaticParams for SSG
- Implement proper typography scale
- Use semantic HTML (article, header, time)
- Optimize images with Next.js Image component

**Testing Strategy:**
- Test markdown renders various elements correctly
- Test 404 handling for invalid slugs
- Test metadata display
- Test image rendering and optimization
- E2E test complete read flow

#### Dependencies
- [ ] Issue #3 (Markdown processing)
- [ ] Issue #4 (Post loading)
- [ ] Issue #5 (SEO metadata)

---

### Issue #8: Syntax Highlighting for Code Blocks

**Type:** feature
**Area:** content
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Implement syntax highlighting for code blocks using Shiki with support for multiple languages and themes. Include copy-to-clipboard functionality.

#### Completion Criteria
- [ ] Code blocks highlight syntax correctly
- [ ] Support for 20+ languages (JS, TS, Python, Go, Rust, etc.)
- [ ] Light and dark theme support
- [ ] Copy button for code blocks
- [ ] Line numbers optional
- [ ] All highlighting tests pass
- [ ] Visual regression tests pass

#### Implementation Notes

**Files to Create:**
- `src/components/CodeBlock.tsx` - Code block component
- `src/lib/shiki.ts` - Shiki configuration
- `tests/unit/CodeBlock.test.tsx` - Component tests

**Key Dependencies:**
```json
{
  "dependencies": {
    "shiki": "^1.0.0",
    "rehype-shiki": "^1.0.0"
  }
}
```

**Components to Build:**
```typescript
// Code block with syntax highlighting
<CodeBlock code={code} language={language} showLineNumbers={true} />

// Copy button
<CopyButton code={code} />
```

**Patterns from Research:**
- Use Shiki for accurate highlighting (VS Code grammar)
- Support theme switching (light/dark)
- Implement copy button with visual feedback
- Test with various programming languages

**Testing Strategy:**
- Test highlighting for multiple languages
- Test theme switching
- Test copy functionality
- Test line numbers display
- Test edge cases (empty code, invalid language)

#### Dependencies
- [ ] Issue #7 (Article rendering)

---

### Issue #9: Responsive Design and Mobile Optimization

**Type:** feature
**Area:** ui
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Ensure entire blog is fully responsive across all device sizes. Optimize for mobile-first indexing with proper viewport configuration and touch interactions.

#### Completion Criteria
- [ ] All pages responsive on mobile, tablet, desktop
- [ ] Mobile-first CSS approach
- [ ] Touch-friendly tap targets (min 44x44px)
- [ ] Proper viewport meta tags
- [ ] Mobile navigation menu works
- [ ] All responsive tests pass
- [ ] Lighthouse mobile score > 90

#### Implementation Notes

**Files to Modify:**
- `src/app/layout.tsx` - Add viewport meta tags
- `src/components/Navigation.tsx` - Mobile menu
- All existing components - Add responsive styles

**Breakpoints (Tailwind):**
```typescript
{
  sm: '640px',   // Small tablets
  md: '768px',   // Tablets
  lg: '1024px',  // Laptops
  xl: '1280px',  // Desktops
  '2xl': '1536px' // Large desktops
}
```

**Patterns from Research:**
- Mobile-first CSS (base styles for mobile, media queries for larger)
- Test on real devices, not just browser dev tools
- Ensure tap targets meet accessibility guidelines (44x44px minimum)
- Optimize images for different screen sizes

**Testing Strategy:**
- Test all breakpoints in Playwright
- Test mobile menu functionality
- Test touch interactions
- Lighthouse mobile audit
- Visual regression tests at different viewports

#### Dependencies
- [ ] Issue #6 (Home page)
- [ ] Issue #7 (Article page)

---

### Issue #10: Navigation and Site Layout

**Type:** feature
**Area:** ui
**Complexity:** low
**Estimated Time:** 1-2 hours

#### Description
Create main site navigation, header, and footer components. Implement consistent layout across all pages with proper semantic HTML.

#### Completion Criteria
- [ ] Header with logo and navigation links
- [ ] Footer with copyright and social links
- [ ] Sticky navigation on scroll
- [ ] Active link highlighting
- [ ] Mobile hamburger menu
- [ ] All navigation tests pass
- [ ] Keyboard navigation works

#### Implementation Notes

**Files to Create:**
- `src/components/Header.tsx` - Site header
- `src/components/Navigation.tsx` - Navigation component
- `src/components/Footer.tsx` - Site footer
- `src/app/layout.tsx` - Root layout
- `tests/unit/Navigation.test.tsx` - Component tests

**Components to Build:**
```typescript
// Site header
<Header />

// Main navigation
<Navigation links={navigationLinks} />

// Site footer
<Footer />
```

**Navigation Links:**
- Home
- Blog
- About (future)
- Tags (future)

**Patterns from Research:**
- Use semantic HTML (header, nav, footer)
- Implement ARIA labels for accessibility
- Sticky header for better UX
- Test keyboard navigation

**Testing Strategy:**
- Test navigation link active states
- Test mobile menu toggle
- Test keyboard navigation (Tab, Enter)
- Test sticky header behavior
- E2E test navigation flows

#### Dependencies
- [ ] Issue #6 (Home page layout)

---

### Issue #11: Reading Time Estimation

**Type:** feature
**Area:** content
**Complexity:** low
**Estimated Time:** 1 hour

#### Description
Calculate and display estimated reading time for each article based on word count. Use industry-standard reading speed (200-250 words per minute).

#### Completion Criteria
- [ ] Reading time calculated correctly
- [ ] Displayed on article cards and detail pages
- [ ] Handles edge cases (very short/long articles)
- [ ] All calculation tests pass
- [ ] Visual display is intuitive

#### Implementation Notes

**Files to Create:**
- `src/lib/reading-time.ts` - Reading time calculation
- `src/components/ReadingTime.tsx` - Display component
- `tests/unit/reading-time.test.ts` - Calculation tests

**Function to Implement:**
```typescript
// Calculate reading time in minutes
function calculateReadingTime(content: string): number {
  const wordsPerMinute = 200;
  const wordCount = content.split(/\s+/).length;
  return Math.ceil(wordCount / wordsPerMinute);
}
```

**Display Format:**
- "X min read" for articles
- Show on post cards and article headers

**Patterns from Research:**
- Use 200 words per minute (industry standard)
- Round up to nearest minute
- Consider code blocks differently (slower reading)

**Testing Strategy:**
- Test with various article lengths
- Test edge cases (empty content, very short)
- Test word counting accuracy
- Test display formatting

#### Dependencies
- [ ] Issue #6 (Post cards)
- [ ] Issue #7 (Article page)

---

### Issue #12: Date Formatting and Display

**Type:** feature
**Area:** content
**Complexity:** low
**Estimated Time:** 1 hour

#### Description
Implement consistent date formatting across the site using locale-aware formatting. Display dates in human-readable format with proper time tags for SEO.

#### Completion Criteria
- [ ] Dates formatted consistently
- [ ] Locale-aware formatting (e.g., "January 15, 2025")
- [ ] ISO 8601 format for machine reading
- [ ] Proper HTML time tags
- [ ] All date tests pass
- [ ] Timezone handling correct

#### Implementation Notes

**Files to Create:**
- `src/lib/date.ts` - Date formatting utilities
- `src/components/FormattedDate.tsx` - Date component
- `tests/unit/date.test.ts` - Formatting tests

**Functions to Implement:**
```typescript
// Format date for display
function formatDate(date: string | Date, locale: string = 'en-US'): string

// Format date for ISO 8601
function formatDateISO(date: string | Date): string

// Get relative time (e.g., "2 days ago")
function getRelativeTime(date: string | Date): string
```

**Component:**
```typescript
<FormattedDate date={post.date} format="long" />
```

**Patterns from Research:**
- Use Intl.DateTimeFormat for locale support
- Always use semantic time tags with datetime attribute
- Provide both human-readable and machine-readable formats

**Testing Strategy:**
- Test various date formats
- Test locale formatting
- Test ISO 8601 output
- Test edge cases (invalid dates)

#### Dependencies
- [ ] Issue #6 (Post cards)
- [ ] Issue #7 (Article page)

---

## Phase 3: Essential Features (Issues #13-#18)

### Issue #13: Tag System with Filtering

**Type:** feature
**Area:** content
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Implement tag system to categorize posts. Create tag pages showing all posts with specific tag. Include tag cloud/list on sidebar or footer.

#### Completion Criteria
- [ ] Tags extracted from post frontmatter
- [ ] Tag page route `/tags/[tag]` works
- [ ] All tags page `/tags` lists all tags
- [ ] Post filtering by tag works correctly
- [ ] Tag count displayed
- [ ] All tag tests pass
- [ ] E2E test verifies tag filtering

#### Implementation Notes

**Files to Create:**
- `src/app/tags/page.tsx` - All tags page
- `src/app/tags/[tag]/page.tsx` - Single tag page
- `src/components/TagList.tsx` - Tag display component
- `src/lib/tags.ts` - Tag utilities
- `tests/unit/tags.test.ts` - Tag logic tests
- `tests/e2e/tags.spec.ts` - E2E tests

**Functions to Implement:**
```typescript
// Get all unique tags with counts
function getAllTags(): TagWithCount[]

// Get posts by tag
function getPostsByTag(tag: string): Post[]

// Normalize tag (lowercase, trim)
function normalizeTag(tag: string): string
```

**Patterns from Research:**
- Normalize tags (lowercase, trim whitespace)
- Sort tags by frequency or alphabetically
- Generate static pages for each tag
- Implement tag cloud with size based on frequency

**Testing Strategy:**
- Test tag extraction from frontmatter
- Test tag normalization
- Test filtering logic
- Test tag counting
- E2E test tag navigation flow

#### Dependencies
- [ ] Issue #4 (Post loading)
- [ ] Issue #6 (Post listing)

---

### Issue #14: Search Functionality

**Type:** feature
**Area:** content
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Implement client-side search functionality using Fuse.js for fuzzy searching. Search across post titles, descriptions, content, and tags.

#### Completion Criteria
- [ ] Search input component works
- [ ] Search results displayed in real-time
- [ ] Search across title, description, content, tags
- [ ] Fuzzy matching implemented
- [ ] Search highlights matched text
- [ ] All search tests pass
- [ ] Keyboard shortcuts work (Cmd/Ctrl+K)

#### Implementation Notes

**Files to Create:**
- `src/components/Search.tsx` - Search component
- `src/components/SearchResults.tsx` - Results display
- `src/lib/search.ts` - Search utilities
- `tests/unit/search.test.ts` - Search logic tests
- `tests/e2e/search.spec.ts` - E2E tests

**Key Dependencies:**
```json
{
  "dependencies": {
    "fuse.js": "^7.0.0"
  }
}
```

**Search Configuration:**
```typescript
const fuseOptions = {
  keys: [
    { name: 'title', weight: 0.4 },
    { name: 'description', weight: 0.3 },
    { name: 'content', weight: 0.2 },
    { name: 'tags', weight: 0.1 }
  ],
  threshold: 0.3,
  includeScore: true
};
```

**Patterns from Research:**
- Use Fuse.js for client-side fuzzy search
- Implement keyboard shortcuts for better UX
- Debounce search input to reduce computations
- Highlight matched terms in results

**Testing Strategy:**
- Test search with various queries
- Test fuzzy matching behavior
- Test keyboard shortcuts
- Test empty and no-results states
- E2E test complete search flow

#### Dependencies
- [ ] Issue #4 (Post loading)
- [ ] Issue #6 (Post listing)

---

### Issue #15: Dark Mode Support

**Type:** feature
**Area:** ui
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Implement dark mode with theme switching. Persist user preference in localStorage. Support system preference detection.

#### Completion Criteria
- [ ] Dark mode toggle works
- [ ] Theme persisted in localStorage
- [ ] System preference detected
- [ ] All components styled for both themes
- [ ] Smooth theme transition
- [ ] No flash of wrong theme on load
- [ ] All theme tests pass

#### Implementation Notes

**Files to Create:**
- `src/components/ThemeToggle.tsx` - Theme switcher
- `src/lib/theme.ts` - Theme utilities
- `src/app/providers.tsx` - Theme provider
- `tests/unit/theme.test.ts` - Theme logic tests

**Key Dependencies:**
```json
{
  "dependencies": {
    "next-themes": "^0.2.1"
  }
}
```

**Theme Configuration:**
```typescript
// tailwind.config.ts
{
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Define color palette for both themes
      }
    }
  }
}
```

**Patterns from Research:**
- Use next-themes for Next.js integration
- Prevent flash of unstyled content (FOUC)
- Support system preference (prefers-color-scheme)
- Use Tailwind dark: variant for styling

**Testing Strategy:**
- Test theme toggle functionality
- Test localStorage persistence
- Test system preference detection
- Test all components in both themes
- Visual regression tests for both themes

#### Dependencies
- [ ] All UI components (Issues #6-#10)

---

### Issue #16: Table of Contents for Articles

**Type:** feature
**Area:** content
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Generate automatic table of contents from article headings. Implement sticky sidebar navigation with scroll highlighting of current section.

#### Completion Criteria
- [ ] TOC generated from markdown headings
- [ ] Sticky sidebar on desktop
- [ ] Active section highlighted on scroll
- [ ] Smooth scroll to sections
- [ ] Collapsed on mobile (expandable)
- [ ] All TOC tests pass
- [ ] Accessibility features work

#### Implementation Notes

**Files to Create:**
- `src/components/TableOfContents.tsx` - TOC component
- `src/lib/toc.ts` - TOC generation utilities
- `tests/unit/toc.test.ts` - TOC logic tests

**Functions to Implement:**
```typescript
// Extract headings from markdown
function extractHeadings(content: string): Heading[]

// Generate nested TOC structure
function generateTOC(headings: Heading[]): TOCNode[]
```

**Heading Structure:**
```typescript
interface Heading {
  id: string;
  text: string;
  level: number; // 1-6
}
```

**Patterns from Research:**
- Use Intersection Observer for scroll detection
- Generate unique IDs for headings (slugified)
- Nest headings based on level hierarchy
- Smooth scroll with scroll-behavior or JS

**Testing Strategy:**
- Test heading extraction accuracy
- Test nested structure generation
- Test scroll highlighting
- Test smooth scroll behavior
- Test mobile collapse/expand

#### Dependencies
- [ ] Issue #7 (Article rendering)

---

### Issue #17: RSS Feed Generation

**Type:** feature
**Area:** content
**Complexity:** low
**Estimated Time:** 1-2 hours

#### Description
Generate RSS feed for blog posts automatically. Include full content or excerpts based on configuration. Follow RSS 2.0 specification.

#### Completion Criteria
- [ ] RSS feed generated at `/rss.xml`
- [ ] Valid RSS 2.0 XML format
- [ ] Includes all published posts
- [ ] Contains required RSS elements
- [ ] RSS feed validates with feed validator
- [ ] All RSS tests pass
- [ ] Auto-discovery link in HTML head

#### Implementation Notes

**Files to Create:**
- `src/app/rss.xml/route.ts` - RSS route handler
- `src/lib/rss.ts` - RSS generation utilities
- `tests/unit/rss.test.ts` - RSS generation tests

**Key Dependencies:**
```json
{
  "dependencies": {
    "rss": "^1.2.2"
  }
}
```

**RSS Elements to Include:**
- Channel title, description, link
- Item title, description, link, pubDate
- Item GUID (unique identifier)
- Item content (optional: full content)

**Patterns from Research:**
- Use RSS library for proper formatting
- Include auto-discovery link tag
- Validate with W3C Feed Validation Service
- Set proper Content-Type header (application/rss+xml)

**Testing Strategy:**
- Test RSS XML structure
- Test all required elements present
- Test date formatting (RFC 822)
- Validate with feed validator
- Test with RSS readers

#### Dependencies
- [ ] Issue #4 (Post loading)
- [ ] Issue #5 (SEO metadata)

---

### Issue #18: Social Share Buttons

**Type:** feature
**Area:** content
**Complexity:** low
**Estimated Time:** 1 hour

#### Description
Add social sharing buttons for Twitter, LinkedIn, Facebook, and copy link. Implement without external tracking scripts for privacy.

#### Completion Criteria
- [ ] Share buttons for Twitter, LinkedIn, Facebook
- [ ] Copy link button with visual feedback
- [ ] No external tracking scripts
- [ ] Mobile-friendly button sizes
- [ ] All share tests pass
- [ ] Share URLs correctly formatted

#### Implementation Notes

**Files to Create:**
- `src/components/ShareButtons.tsx` - Share buttons component
- `src/lib/share.ts` - Share URL generation
- `tests/unit/share.test.ts` - Share logic tests

**Share URL Formats:**
```typescript
// Twitter
`https://twitter.com/intent/tweet?text=${title}&url=${url}`

// LinkedIn
`https://www.linkedin.com/sharing/share-offsite/?url=${url}`

// Facebook
`https://www.facebook.com/sharer/sharer.php?u=${url}`
```

**Component:**
```typescript
<ShareButtons title={post.title} url={postUrl} />
```

**Patterns from Research:**
- Use Web Share API where supported (mobile)
- Fallback to share URLs for desktop
- No third-party tracking scripts
- Copy link with Clipboard API

**Testing Strategy:**
- Test share URL generation
- Test copy to clipboard
- Test fallback behavior
- Test on mobile and desktop
- Test accessibility

#### Dependencies
- [ ] Issue #7 (Article page)

---

## Phase 4: Polish & Enhancement (Issues #19-#24)

### Issue #19: Performance Optimization

**Type:** refactor
**Area:** performance
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Optimize bundle size, implement code splitting, lazy loading, and image optimization. Achieve Lighthouse score of 95+ across all metrics.

#### Completion Criteria
- [ ] Bundle size optimized (< 200KB initial JS)
- [ ] Code splitting implemented
- [ ] Images optimized (WebP, lazy loading)
- [ ] Fonts optimized (self-hosted, font-display: swap)
- [ ] Lighthouse score > 95 (all categories)
- [ ] Core Web Vitals in "Good" range
- [ ] All performance tests pass

#### Implementation Notes

**Files to Modify:**
- `next.config.ts` - Bundle optimization config
- All image usages - Convert to Next.js Image
- `src/app/layout.tsx` - Font optimization

**Optimizations:**
```typescript
// next.config.ts
{
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200],
  },
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['lucide-react'],
  }
}
```

**Patterns from Research:**
- Use Next.js Image for automatic optimization
- Implement dynamic imports for heavy components
- Self-host fonts with font-display: swap
- Remove unused CSS and JS
- Enable compression (gzip/brotli)

**Testing Strategy:**
- Lighthouse CI in test suite
- Bundle analyzer to identify large dependencies
- Test Core Web Vitals (LCP, FID, CLS)
- Monitor with Vercel Analytics
- Test on slow 3G connection

#### Dependencies
- [ ] All features implemented (Issues #6-#18)

---

### Issue #20: Advanced SEO Optimization

**Type:** feature
**Area:** seo
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Implement advanced SEO features including automatic sitemap generation, robots.txt, canonical URLs, and enhanced structured data. Submit to Google Search Console.

#### Completion Criteria
- [ ] Automatic sitemap.xml generation
- [ ] robots.txt configured
- [ ] Canonical URLs on all pages
- [ ] Enhanced JSON-LD (BreadcrumbList, Organization)
- [ ] Open Graph images generated
- [ ] All SEO validation tests pass
- [ ] Google Search Console verified

#### Implementation Notes

**Files to Create:**
- `src/app/sitemap.ts` - Dynamic sitemap
- `src/app/robots.ts` - Robots.txt
- `src/lib/og-image.ts` - OG image generation
- `tests/unit/sitemap.test.ts` - Sitemap tests

**Key Dependencies:**
```json
{
  "dependencies": {
    "@vercel/og": "^0.6.0"
  }
}
```

**Structured Data to Add:**
- BreadcrumbList for navigation
- Organization for site identity
- Person for author profiles

**Patterns from Research:**
- Use Next.js sitemap.ts for dynamic generation
- Generate OG images with @vercel/og
- Implement proper canonical URLs
- Test with Google Rich Results Test

**Testing Strategy:**
- Test sitemap generation
- Test robots.txt configuration
- Validate structured data
- Test OG image generation
- Verify in Search Console

#### Dependencies
- [ ] Issue #5 (Basic SEO)
- [ ] All content pages (Issues #6-#7)

---

### Issue #21: Analytics and Web Vitals Tracking

**Type:** feature
**Area:** analytics
**Complexity:** low
**Estimated Time:** 1-2 hours

#### Description
Implement privacy-friendly analytics using Vercel Analytics and track Core Web Vitals. Monitor performance metrics without compromising user privacy.

#### Completion Criteria
- [ ] Vercel Analytics integrated
- [ ] Core Web Vitals tracked
- [ ] Privacy-compliant (no cookies for EU visitors)
- [ ] Custom events tracked
- [ ] Analytics dashboard accessible
- [ ] All tracking tests pass

#### Implementation Notes

**Files to Create:**
- `src/app/layout.tsx` - Add Analytics component
- `src/lib/analytics.ts` - Custom event tracking
- `tests/unit/analytics.test.ts` - Tracking tests

**Key Dependencies:**
```json
{
  "dependencies": {
    "@vercel/analytics": "^1.1.0",
    "@vercel/speed-insights": "^1.0.0"
  }
}
```

**Events to Track:**
- Page views (automatic)
- Search queries
- Theme toggles
- Share button clicks
- External link clicks

**Patterns from Research:**
- Use Vercel Analytics (privacy-friendly, no cookies)
- Track Core Web Vitals automatically
- Implement custom events sparingly
- Respect DNT (Do Not Track) header

**Testing Strategy:**
- Test analytics integration
- Test custom event firing
- Test privacy compliance
- Verify data in Vercel dashboard

#### Dependencies
- [ ] All features implemented

---

### Issue #22: Comments System with Giscus

**Type:** feature
**Area:** community
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Integrate Giscus (GitHub Discussions) for blog comments. Provides moderation through GitHub, no backend needed, and privacy-friendly.

#### Completion Criteria
- [ ] Giscus comments appear on article pages
- [ ] Comments load lazily (not blocking content)
- [ ] Theme matches site (light/dark)
- [ ] GitHub Discussions created per article
- [ ] All comments tests pass
- [ ] Accessible comment section

#### Implementation Notes

**Files to Create:**
- `src/components/Comments.tsx` - Comments component
- `tests/unit/Comments.test.tsx` - Component tests
- `.env.example` - Environment variables template

**Key Dependencies:**
```json
{
  "dependencies": {
    "@giscus/react": "^2.3.0"
  }
}
```

**Configuration:**
```typescript
<Giscus
  repo="username/repo"
  repoId="..."
  category="Announcements"
  categoryId="..."
  mapping="pathname"
  reactionsEnabled="1"
  emitMetadata="0"
  theme={theme}
  loading="lazy"
/>
```

**Patterns from Research:**
- Use GitHub Discussions (free, no backend)
- Load comments lazily (Intersection Observer)
- Match theme with site
- Respect user privacy (no tracking)

**Testing Strategy:**
- Test component renders
- Test lazy loading behavior
- Test theme synchronization
- Test accessibility
- Manual test GitHub Discussion creation

#### Dependencies
- [ ] Issue #7 (Article page)
- [ ] Issue #15 (Dark mode)

---

### Issue #23: Newsletter Subscription

**Type:** feature
**Area:** community
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Add newsletter subscription form using ConvertKit or similar service. Include validation, loading states, and success/error handling.

#### Completion Criteria
- [ ] Subscription form component works
- [ ] Email validation implemented
- [ ] API integration with email service
- [ ] Loading and error states handled
- [ ] Success confirmation displayed
- [ ] GDPR-compliant (double opt-in)
- [ ] All form tests pass

#### Implementation Notes

**Files to Create:**
- `src/components/NewsletterForm.tsx` - Subscription form
- `src/app/api/subscribe/route.ts` - API route
- `tests/unit/NewsletterForm.test.tsx` - Component tests
- `tests/integration/subscribe.test.ts` - API tests

**Key Dependencies:**
```json
{
  "dependencies": {
    "@convertkit/react": "^1.0.0"
  }
}
```

**Form Validation:**
```typescript
// Email validation
function validateEmail(email: string): boolean

// Sanitize input
function sanitizeInput(input: string): string
```

**Patterns from Research:**
- Use server-side API route for security
- Implement rate limiting
- Double opt-in for GDPR compliance
- Clear privacy policy link

**Testing Strategy:**
- Test email validation
- Test form submission
- Test error handling
- Test success state
- Integration test with API

#### Dependencies
- [ ] None (standalone feature)

---

### Issue #24: Enhanced 404 and Error Pages

**Type:** feature
**Area:** ui
**Complexity:** low
**Estimated Time:** 1 hour

#### Description
Create custom 404 and error pages with helpful navigation and search functionality. Improve user experience when encountering errors.

#### Completion Criteria
- [ ] Custom 404 page with search
- [ ] Custom error page for 500 errors
- [ ] Popular posts suggested
- [ ] Search bar included
- [ ] Proper HTTP status codes
- [ ] All error page tests pass
- [ ] Accessibility compliant

#### Implementation Notes

**Files to Create:**
- `src/app/not-found.tsx` - 404 page
- `src/app/error.tsx` - Error page
- `tests/e2e/errors.spec.ts` - E2E tests

**404 Page Features:**
- Search bar to find content
- Links to popular posts
- Link to home page
- Friendly error message

**Error Page Features:**
- Friendly error message
- Reload button
- Link to home
- Error tracking (optional)

**Patterns from Research:**
- Use Next.js not-found.tsx convention
- Provide helpful navigation options
- Track 404s to identify broken links
- Make errors actionable

**Testing Strategy:**
- Test 404 page renders
- Test error page renders
- Test navigation links work
- Test proper status codes
- E2E test error scenarios

#### Dependencies
- [ ] Issue #14 (Search functionality)
- [ ] Issue #6 (Home page)

---

## Implementation Strategy

### TDD Workflow for Each Issue

1. **RED Phase**: Write failing test
   - Create test file based on issue requirements
   - Write test cases covering all completion criteria
   - Commit: `test(#N): add test for [feature]`

2. **GREEN Phase**: Implement minimum code to pass tests
   - Write simplest implementation
   - Make all tests pass
   - Commit: `feat(#N): implement [feature]`

3. **REFACTOR Phase**: Improve code quality
   - Clean up implementation
   - Optimize performance
   - Commit: `refactor(#N): improve [aspect]`

4. **DOCUMENT Phase**: Mark completion
   - Check off items in TDD plan
   - Update documentation
   - Commit: `docs(#N): mark [feature] complete`

### Issue Dependencies Graph

```
Phase 1 (Foundation)
#1 → #2, #3
#3 → #4
#4 → #5

Phase 2 (Core Features)
#4, #5 → #6
#3, #4, #5 → #7
#7 → #8
#6, #7 → #9, #10
#6, #7 → #11, #12

Phase 3 (Essential Features)
#4, #6 → #13, #14
#6-#10 → #15
#7 → #16
#4, #5 → #17
#7 → #18

Phase 4 (Polish & Enhancement)
#6-#18 → #19
#5, #6, #7 → #20
All features → #21
#7, #15 → #22
None → #23
#6, #14 → #24
```

### Parallel Work Opportunities

Issues that can be worked on in parallel (no dependencies):

**After Foundation Complete:**
- #6, #7 can be developed in parallel
- #11, #12 are independent utilities

**After Core Features:**
- #13, #14, #17, #18 can be developed in parallel
- #22, #23 are independent features

### Estimated Timeline

- **Phase 1 (Foundation):** 8-10 hours
- **Phase 2 (Core Features):** 12-14 hours
- **Phase 3 (Essential Features):** 10-12 hours
- **Phase 4 (Polish):** 9-11 hours

**Total Estimated Time:** 39-47 hours (1-2 weeks for single developer)

## Next Steps

1. Review and approve this issue breakdown
2. Create GitHub issues using the issue-creator agent
3. Generate individual TDD plans for each issue
4. Begin implementation starting with Phase 1, Issue #1
