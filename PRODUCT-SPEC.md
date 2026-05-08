# PRODUCT-SPEC: Support

## Overview

**App Name:** Support
**Domain:** Ticketing, knowledge base, customer support
**Target User:** Support agents, customers

## Core Entities

### Ticket
```
Ticket
├── id: UUID (PK)
├── subject: str (required)
├── description: str (required)
├── status: enum ["open", "in_progress", "waiting", "resolved", "closed"] (default: "open")
├── priority: enum ["low", "medium", "high", "urgent"] (default: "medium")
├── customer_email: str (required)
├── customer_name: str (optional)
├── assigned_to: str (optional)
├── created_at: datetime
└── updated_at: datetime
```

### Comment
```
Comment
├── id: UUID (PK)
├── ticket_id: UUID (FK → Ticket, ondelete=CASCADE)
├── author: str (required)
├── body: str (required)
├── is_internal: bool (default false)
├── created_at: datetime
└── updated_at: datetime
```

### KnowledgeBaseArticle
```
KnowledgeBaseArticle
├── id: UUID (PK)
├── title: str (required)
├── content: str (required)
├── category: enum ["general", "billing", "technical", "account"] (required)
├── views: int (default 0)
├── created_at: datetime
└── updated_at: datetime
```

## User Stories / Screens

### Screen 1: Dashboard
- Summary cards: open tickets, resolved today, avg response time (mock), KB articles
- Tickets by priority bar chart
- Recent tickets list

### Screen 2: Tickets
- Table view with pagination, search by subject/customer
- Status and priority filters
- "Create Ticket" form

### Screen 3: Ticket Detail
- Ticket info with status/priority dropdowns, assignee input
- Comment thread (public + internal)
- "Add Comment" form
- Resolve/Close buttons

### Screen 4: Knowledge Base
- Article list with category filter, search
- Article detail view
- "Add Article" form

## AI Features

- **Auto-categorization:** Suggest category based on ticket subject (mock)
- **Response draft:** Generate a suggested response based on ticket content (mock)

## API Endpoints (v1.0)

```
GET    /api/v1/tickets            → List tickets
POST   /api/v1/tickets            → Create ticket
GET    /api/v1/tickets/{id}       → Get ticket
PUT    /api/v1/tickets/{id}       → Update ticket
DELETE /api/v1/tickets/{id}       → Delete ticket
GET    /api/v1/tickets/{id}/comments → List comments
POST   /api/v1/tickets/{id}/comments → Add comment
GET    /api/v1/articles           → List KB articles
POST   /api/v1/articles           → Create article
GET    /api/v1/articles/{id}      → Get article
PUT    /api/v1/articles/{id}      → Update article
DELETE /api/v1/articles/{id}      → Delete article
GET    /api/v1/dashboard          → Dashboard stats
```

## Non-Functional Requirements

- Backend tests: 70%+ coverage
- Frontend: Responsive, Tailwind + pre-built UI components
- Docker: All services start with `docker compose up -d`
- No mock data — everything persisted to PostgreSQL
