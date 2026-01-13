# Changelog

All notable changes to the TruEditor project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Phase 5: ORCID Integration & UI Redesign
  - ORCID OAuth2 production integration
  - ORCIDService class for OAuth flow management
  - Login/Callback/Sync API endpoints
  - Modern UI redesign for all pages
  - Responsive mobile-first design
  - Gradient backgrounds and animations
  - Database migration fixes for Render free tier

- Phase 4: Deployment to Production
  - Frontend deployed to Vercel (https://trueditor.vercel.app)
  - Backend deployed to Render.com (https://trueditor-api.onrender.com)
  - Neon PostgreSQL serverless database connected
  - Upstash Redis serverless cache connected
  - Health check endpoints verified
  
- Phase 3: Database Models
  - CustomUser model with ORCID integration
  - Submission model with FSM state management
  - ManuscriptFile model with file metadata
  - Author model with CRediT taxonomy support
  - SubmissionStatusHistory for audit trail

- Phase 2: Production-Ready Architecture
  - Environment separation (development, staging, production)
  - Docker multi-stage build configuration
  - Docker Compose for local development
  - CI/CD pipeline with GitHub Actions
  - Health check endpoints (liveness/readiness)
  - Stateless backend design
  - Platform-agnostic configuration

- Phase 1.5: Vue.js Frontend Setup
  - Vue 3 with Composition API and TypeScript
  - Pinia state management with persistence
  - TailwindCSS v4 for styling
  - Vue Router with authentication guards
  - Axios HTTP client with interceptors
  - Modern landing page with animations
  - ORCID login button component

- Phase 1: Django Backend Setup
  - Django 5.x with Django REST Framework
  - Modular settings (base, development, staging, production)
  - Custom exception handler for consistent API responses
  - Celery integration for async tasks
  - JWT authentication configuration

- Phase 0: Project Foundation
  - `.cursorrules` - Cursor AI development guidelines
  - `README.md` - Project documentation
  - `CHANGELOG.md` - Change log
  - `.gitignore` - Git ignore rules
  - `env.example` - Environment variables template

### Changed
- All UI text converted from Turkish to English
- All code comments and docstrings converted to English
- Commit messages now in English (reports remain in Turkish)

### Fixed
- TypeScript path alias configuration in tsconfig.app.json
- Unused router variable in LoginPage.vue
- Potential undefined access in NewSubmission.vue
- Docker package name for newer Debian (libgdk-pixbuf-2.0-0)

---

## Version History

### [1.0.0] - Planned
#### To Be Added
- Author Module
  - Mandatory ORCID authentication
  - 6-step manuscript submission wizard
  - Drag-and-drop file upload
  - Auto-save functionality
  - PDF generation (Celery + WeasyPrint)
  - Submission tracking
  
- Backend Infrastructure
  - Django 5.x + DRF
  - PostgreSQL database
  - Redis cache and message broker
  - Celery async tasks
  - AWS S3 file storage
  
- Frontend Interface
  - Vue.js 3 + TypeScript
  - Pinia state management
  - TailwindCSS styling
  - Modern animations
  - Responsive design
  
- Brand Identity
  - TruEditor logo
  - Landing page
  - Color palette and typography

---

## Future Versions (Planned)

### [1.1.0] - Reviewer Module
- Reviewer invitation system
- Review forms
- Evaluation reports
- Reviewer dashboard

### [1.2.0] - Editor Module
- Editor assignment
- Decision-making interface
- Workflow management
- Editor dashboard

### [1.3.0] - Admin Module
- User management
- System settings
- Advanced reporting
- Analytics dashboard

### [2.0.0] - Advanced Features
- Multi-language support
- Dark mode
- Mobile application (PWA)
- Advanced notification system
- Integration APIs

---

## Contributors

- Project Owner and Lead Developer: Abdullah Doğan

---

[Unreleased]: https://github.com/AbdullahProgrammerX/TruEditor/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/AbdullahProgrammerX/TruEditor/releases/tag/v1.0.0
