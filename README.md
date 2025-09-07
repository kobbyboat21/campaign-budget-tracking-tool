# Campaign Budget Tracking Tool

A full-stack web application for tracking marketing campaign budgets, spend, and statuses.

## Table of Contents
- [Installation](#installation)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Installation

### Prerequisites
- Docker and Docker Compose
- Git

### Quick Start
1. Clone the repository
   ```bash
   git clone https://github.com/kobbyboat21/campaign-budget-tracking-tool.git
   cd campaign-budget-tracking-tool
   ```

2. Set up environment variables
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. Start with Docker Compose
   ```bash
   docker-compose up -d
   ```

4. Access the application
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/

## Architecture

### System Architecture
```
+-------------------+        HTTP (REST API)        +-------------------+
|   Frontend        |  <--------------------------> |     Backend       |
| - Vue/ Nuxt.js 4.x|                               | - Django 4.x      |
| - Tailwind CSS    |                               | - SQLite          |
+-------------------+                               +-------------------+
          |                                                    |
          | Docker Container                                   | Docker Container
          +----------------------------+-----------------------+
                                       |
                                docker-compose.yml
```

### Backend Architecture
```
┌───────────────────────────────────────────────────────────┐
│                    Django Application                     │
│                                                           │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│  │   Models    │◄────┤  ViewSets   │◄────┤ Serializers │  │
│  │ - Campaign  │     │ - CRUD API  │     │ - JSON data │  │
│  └─────────────┘     └──────┬──────┘     └─────────────┘  │
│                             │                             │
│  ┌─────────────┐     ┌──────▼──────┐                      │
│  │    Admin    │     │  URL Routes │                      │
│  │ - Dashboard │     │ - /api/     │                      │
│  └─────────────┘     └─────────────┘                      │
└───────────────────────────────────────────────────────────┘
```

### Frontend Architecture
```
┌───────────────────────────────────────────────────────────┐
│                   Nuxt.js Application                     │
│                                                           │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│  │    Pages    │◄────┤ Components  │◄────┤ Composables │  │
│  │ - index.vue │     │ - campaigns │     │ - API calls │  │
│  └─────────────┘     └──────┬──────┘     └─────────────┘  │
│                             │                             │
│  ┌─────────────┐     ┌──────▼──────┐                      │
│  │   Assets    │     │    Utils    │                      │
│  │ - Tailwind  │     │ - Formatters│                      │
│  └─────────────┘     └─────────────┘                      │
└───────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
┌──────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────┐
│          │  1  │               │  2  │               │  3  │           │
│  User    │────►│  Vue/Nuxt.js  │────►│  Django REST  │────►│  SQLite   │
│ Interface│     │  Components   │     │  API          │     │  Database │
│          │◄────│               │◄────│               │◄────│           │
└──────────┘  6  └───────────────┘  5  └───────────────┘  4  └───────────┘
                       │                                        
                       │                                        
                       ▼                                        
                 ┌───────────────┐                              
                 │ Campaign Data │                              
                 │ - name        │                              
                 │ - budget      │                              
                 │ - spend       │                              
                 │ - status      │                              
                 └───────────────┘                              
```

1. User interacts with the interface (clicks, form submissions)
2. Vue/Nuxt components send HTTP requests to the backend API
3. Django API processes requests and performs database operations
4. Database returns requested data or confirms changes
5. API formats response as JSON and returns to frontend
6. UI updates with new data

## Tech Stack
- **Frontend**: Nuxt.js 4.x, Tailwind CSS 4.x, Nuxt UI
- **Backend**: Django 4.x, Django REST Framework
- **Database**: SQLite (development)
- **DevOps**: Docker & Docker Compose

## API Endpoints
- `GET /api/campaigns/` - List campaigns
- `POST /api/campaigns/` - Create campaign
- `GET /api/campaigns/{id}/` - Get campaign
- `PUT /api/campaigns/{id}/` - Update campaign
- `DELETE /api/campaigns/{id}/` - Delete campaign

## License
MIT License
