# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Safety Copilot** is a full-stack HSE (Health, Safety & Environment) analytics platform for analyzing safety data (incidents, hazards, audits, inspections) with AI-powered insights.

**Architecture**: Monorepo with separate client and server directories
- **Client**: React + TypeScript + Vite + shadcn/ui
- **Server**: FastAPI + Python with AI agent capabilities

## Common Commands

### Server (FastAPI Backend)

**Setup & Run**:
```powershell
# Navigate to server directory
cd server

# Create virtual environment (first time only)
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies (from project root - requirements.txt expected there or in server/)
pip install -r requirements.txt

# Run the API server from project root
uvicorn server.app.main:app --reload --port 8000

# Alternative: run from server/app directory
cd server/app
uvicorn main:app --reload --port 8000
```

**Environment Variables**:
- Create `.env` file in `server/app/` directory
- Required: `OPENAI_API_KEY=sk-...` for AI agent endpoints
- The server auto-loads environment variables from `server/app/.env`

**API Documentation**:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Client (React Frontend)

**Setup & Run**:
```powershell
# Navigate to client directory
cd client

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Build for development mode
npm run build:dev

# Lint code
npm run lint

# Preview production build
npm run preview
```

**Environment Variables**:
- Create `.env` file in `client/` directory
- Default backend URL: `VITE_API_BASE_URL=http://127.0.0.1:8000`
- The client runs on port 8080 by default

## Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────────┐
│                    Client (Port 8080)                    │
│  React Router → Pages → Components → API Calls          │
│  - Landing Page (public)                                │
│  - Dashboard/Overview (analytics)                       │
│  - Incidents/Hazards/Audits/Inspections               │
│  - Agent (AI chat interface)                           │
│  - Maps, Wordclouds, Analytics, Data Health           │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP/WebSocket
┌──────────────────▼──────────────────────────────────────┐
│                   Server (Port 8000)                     │
│  FastAPI → Routers → Services → Analytics              │
│  - Excel data loading & caching                        │
│  - Analytics endpoints (Plotly charts)                 │
│  - AI Agent (OpenRouter/OpenAI streaming)              │
│  - WebSocket streaming                                 │
│  - Filter options                                      │
└─────────────────────────────────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  Excel Data Source   │
        │  EPCL_VEHS_Data_     │
        │  Processed.xlsx      │
        └─────────────────────┘
```

### Data Flow

1. **Data Source**: `server/app/EPCL_VEHS_Data_Processed.xlsx` contains all safety data
2. **Data Loading**: `server/app/services/excel.py` loads and caches Excel sheets on first request
3. **Analytics Generation**: `server/app/services/analytics_general.py` and `server/app/analytics/` generate Plotly visualizations
4. **API Layer**: FastAPI routers expose analytics as JSON endpoints
5. **Frontend Rendering**: React components fetch JSON and render charts using Plotly.js/Recharts

### Key Architectural Patterns

**Backend (FastAPI)**:
- **Router-Service Pattern**: Routers in `app/routers/` delegate to services in `app/services/`
- **Lazy Loading**: Excel data loaded and cached on first request (performance optimization)
- **Streaming Architecture**: Real-time AI responses via Server-Sent Events (SSE) and WebSocket
- **CORS**: Wide-open CORS for local development (`allow_origins=["*"]`)

**Frontend (React)**:
- **React Router v6**: Client-side routing with `<BrowserRouter>`
- **AppLayout Wrapper**: Shared sidebar layout for authenticated pages
- **TanStack Query**: Data fetching with caching (`@tanstack/react-query`)
- **shadcn/ui**: Component library with Radix UI primitives
- **Path Aliases**: `@/` maps to `src/` directory

### Agent System Architecture

The AI agent has multiple implementations with different capabilities:

**Agent Endpoints**:
- `GET /agent/run` - Synchronous response with code generation, execution, and analysis
- `GET /agent/stream` - Server-Sent Events (SSE) streaming with real-time progress
- `WebSocket /ws/agent` - Ultra-fast streaming with bidirectional communication

**Agent Flow**:
1. User asks question in natural language
2. Agent generates pandas code using LLM (OpenRouter/OpenAI)
3. Code executes in sandboxed environment with restricted builtins
4. Results analyzed and formatted
5. Plotly charts generated if applicable
6. Prescriptive analysis provided

**Security**: Agent executes in restricted sandbox with no filesystem/network access

### Excel Data Structure

The Excel file contains the following sheets:
- **Incident**: Incidents with 72 columns (severity, root cause, corrective actions, PSM, etc.)
- **Hazard ID**: Hazards with 35 columns (violation types, worst case consequences, etc.)
- **Audit**: Audit records with 36 columns
- **Audit Findings**: Detailed audit findings (34 columns)
- **Inspection**: Inspection records
- **Inspection Findings**: Detailed inspection findings
- **Relationships**: Links between incidents/hazards/audits
- **Location_Summary**: Aggregated location data
- **Department_Summary**: Aggregated department data

**Key Derived Fields** (calculated in backend):
- `severity_score`: Numerical severity (1-5)
- `risk_score`: Combined risk metric
- `reporting_delay_days`: Days between occurrence and reporting
- `resolution_time_days`: Days to close
- `estimated_cost_impact`: Financial impact estimation
- `estimated_manhours_impact`: Labor impact estimation
- `compliance_systems_involved`: PSM/compliance count

## Development Workflows

### Adding a New Analytics Endpoint

1. Create analytics function in `server/app/services/analytics_general.py` or create new service file
2. Add router endpoint in appropriate router file (e.g., `server/app/routers/analytics_general.py`)
3. Add API function in `client/src/lib/api.ts` (TypeScript)
4. Create or update page component in `client/src/pages/`
5. Update routing in `client/src/App.tsx` if new page

### Modifying the AI Agent

- **Prompts**: System prompts in `server/app/services/agent.py` or `streaming_agent.py`
- **Model Selection**: Configurable via `model` query parameter (default: `x-ai/grok-4-fast:free`)
- **Streaming**: Use `agent_ws.py` for WebSocket or `agent.py` for SSE streaming
- **Personas**: User personas stored in `server/app/services/personas.py` for dynamic system prompts

### Working with Filters

**Backend**:
- Filter options endpoint: `/analytics/filter-options/combined`
- Implementation: `server/app/routers/filters.py` and `server/app/services/filter_options.py`
- Returns unique values with counts for all filterable fields

**Frontend**:
- Custom hook: `client/src/hooks/useFilterOptions.ts` (5-minute caching)
- Filter components in pages apply filters to chart data
- Per-chart date filters supported on Overview page

### Adding New UI Components

1. For shadcn/ui components: Check `client/components.json` for configuration
2. Component path alias: `@/components` → `client/src/components`
3. UI primitives: `client/src/components/ui/`
4. Custom components: Organize by feature (e.g., `charts/`, `chat/`, `dashboard/`)

## Important Technical Details

### Excel Data Loading
- File path: `server/app/EPCL_VEHS_Data_Processed.xlsx`
- Auto-loaded and cached on first request
- **Restart server to reload after replacing Excel file**
- Loading logic in `server/app/services/excel.py`

### API Integration
- Base URL configured in `client/.env`: `VITE_API_BASE_URL`
- API client: `client/src/lib/api.ts`
- CORS must allow client origin (currently open for local dev)

### Styling System
- **Tailwind CSS** with custom configuration in `client/tailwind.config.ts`
- **CSS Variables** for theming (defined in `client/src/index.css`)
- **Dark Mode**: Supported via `next-themes` package
- **Fonts**: IBM Plex Mono, Lora, Plus Jakarta Sans (loaded via @fontsource)

### State Management
- **TanStack Query**: Server state and caching
- **React Hooks**: Local component state (useState, useEffect)
- **No global state library**: Props and context for shared state

### WebSocket Streaming
- Endpoint: `ws://127.0.0.1:8000/ws/agent`
- Implementation: `server/app/routers/agent_ws.py`
- Supports real-time thinking, streaming responses, and tool calls

## File Structure

```
safteycopilot/
├── client/                       # React frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── ui/             # shadcn/ui components
│   │   │   ├── charts/         # Chart components
│   │   │   ├── chat/           # Chat interface
│   │   │   └── layout/         # Layout components
│   │   ├── pages/              # Page components (routes)
│   │   ├── hooks/              # Custom React hooks
│   │   ├── lib/                # Utilities (api.ts, utils.ts)
│   │   ├── utils/              # Helper functions
│   │   └── data/               # Static data
│   ├── components.json         # shadcn/ui configuration
│   ├── vite.config.ts         # Vite configuration
│   └── package.json           # Dependencies
├── server/                      # FastAPI backend
│   └── app/
│       ├── routers/            # API endpoints
│       │   ├── agent.py        # AI agent endpoints
│       │   ├── agent_ws.py     # WebSocket streaming
│       │   ├── analytics_*.py  # Analytics endpoints
│       │   ├── filters.py      # Filter options
│       │   └── data.py         # Data endpoints
│       ├── services/           # Business logic
│       │   ├── excel.py        # Excel data loading
│       │   ├── agent.py        # Agent logic
│       │   ├── streaming_agent.py  # Streaming agent
│       │   ├── filter_options.py   # Filter generation
│       │   └── analytics_general.py # Analytics
│       ├── analytics/          # Analytics functions (legacy)
│       ├── models/             # Pydantic schemas
│       ├── core/               # Core utilities
│       ├── main.py            # FastAPI app entry
│       ├── .env               # Environment variables
│       └── EPCL_VEHS_Data_Processed.xlsx  # Data source
└── WARP.md                     # This file
```

## Troubleshooting

### Server Issues
- **Import errors**: Ensure server is run from project root with `uvicorn server.app.main:app`
- **Excel file not found**: Check `server/app/EPCL_VEHS_Data_Processed.xlsx` exists
- **Agent errors**: Verify `OPENAI_API_KEY` in `server/app/.env`
- **Port in use**: Change port with `--port 8001`

### Client Issues
- **API connection failed**: Verify server is running on port 8000
- **Environment variable not loaded**: Vite env vars must start with `VITE_`
- **Build errors**: Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- **Type errors**: Check `tsconfig.json` - some strict checks are disabled for flexibility

### Data Issues
- **Stale data after Excel update**: Restart the FastAPI server
- **Missing filter options**: Check `/analytics/filter-options/combined` endpoint
- **Empty charts**: Verify data exists in Excel sheets and column names match expected schema

## Development Best Practices

### Backend
- Use existing service layer patterns (router → service → analytics)
- Return Plotly JSON format for all visualizations
- Cache expensive computations in services
- Use Pydantic models for request/response validation
- Maintain CORS configuration for security

### Frontend  
- Use TanStack Query for all API calls with appropriate stale times
- Follow shadcn/ui patterns for new components
- Use Tailwind classes, avoid custom CSS
- Implement loading and error states for all data fetching
- Use path aliases (`@/`) for cleaner imports

### Code Quality
- Backend: Follow FastAPI conventions and Python type hints
- Frontend: Use TypeScript strictly where possible (some checks relaxed for pragmatism)
- Keep components focused and composable
- Document complex business logic
- Use descriptive variable names for safety domain concepts

## Related Documentation
# Claude Rules for shadcn MCP Integration

## Core Principles

When working with UI components and design tasks, ALWAYS follow these rules to ensure proper component usage and best practices.

---

## 1. MCP Component Discovery (CRITICAL)

### Before ANY UI Work:
- **ALWAYS check shadcn MCP tools first** before suggesting or implementing components
- Run: "Show me all available components in the shadcn registry"
- Verify component availability in configured registries
- Check for namespaced components if using custom registries (@acme, @internal, etc.)

### Component Verification:
```
✓ DO: Query MCP for actual component list
✓ DO: Check component configuration in the registry
✓ DO: Verify component dependencies and variants
✗ DON'T: Assume component availability without checking
✗ DON'T: Use generic shadcn components without MCP verification
```

---

## 2. Component Installation Protocol

### Installation Order:
1. **Search First**: "Find me a [component type] from the shadcn registry"
2. **Verify Match**: Confirm the component matches requirements
3. **Install Properly**: "Add the [component-name] component to my project"
4. **Wait for Confirmation**: Ensure installation succeeds before usage

### Multi-Component Projects:
```bash
# Install all required components at once
"Add the button, dialog, card, and form components to my project"
```

---

## 3. UI Best Practices

### Component Selection:
- **Prefer Existing Components**: Always use MCP registry components over custom builds
- **Check Variants**: Query component variants and configurations from registry
- **Semantic HTML**: Ensure components use proper semantic structure
- **Accessibility**: Verify ARIA labels, keyboard navigation, and screen reader support

### Design Principles:
```
✓ Consistent spacing (use Tailwind spacing scale: p-4, gap-6, etc.)
✓ Proper contrast ratios (WCAG AA minimum)
✓ Responsive design (mobile-first approach)
✓ Loading states and error handling
✓ Smooth transitions and animations
✓ Clear visual hierarchy
```

---

## 4. Registry Management

### Multiple Registry Workflow:
```
1. Check which registries are configured: components.json
2. Search across all registries for best component fit
3. Specify namespace when installing: "@acme/hero-section"
4. Verify authentication for private registries
```

### Registry Prompts:
- "Show me components from [registry-name] registry"
- "Find authentication components from @internal registry"
- "Install @acme/landing-hero for the homepage"

---

## 5. Component Implementation Standards

### When Using Components:

```typescript
// ✓ CORRECT: Use imported components with proper props
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>Proper Structure</CardTitle>
  </CardHeader>
  <CardContent>
    <Button variant="default" size="lg">Action</Button>
  </CardContent>
</Card>

// ✗ INCORRECT: Don't create custom components without checking MCP first
<div className="custom-card">
  <div className="custom-button">Click me</div>
</div>
```

### Props and Variants:
- Check component documentation from registry
- Use defined variant props (variant, size, etc.)
- Don't override component styles excessively
- Follow the component's intended API

---

## 6. Project Setup Checklist

Before starting UI work, verify:
- [ ] MCP server is configured and running
- [ ] Can access shadcn registry tools
- [ ] components.json exists with proper registry configuration
- [ ] Authentication configured for private registries (.env.local)
- [ ] Target directories exist for component installation

---

## 7. Composition Patterns

### Building Complex UIs:

```typescript
// ✓ GOOD: Compose from registry components
"Build a landing page using hero, features, and testimonials 
sections from the shadcn registry"

// ✓ GOOD: Specific component composition
"Create a contact form using input, textarea, and button 
components from shadcn"

// ✗ AVOID: Vague requests without registry check
"Make me a landing page" (without checking available blocks)
```

---

## 8. Troubleshooting Protocol

### If Components Don't Work:
1. Verify MCP connection: Check for "Connected" status
2. Clear npx cache: `npx clear-npx-cache`
3. Check components.json for registry configuration
4. Verify authentication tokens in .env.local
5. Ensure write permissions in component directories

### If MCP Not Responding:
- Restart MCP client
- Re-enable shadcn MCP server
- Check logs (View -> Output -> MCP in Cursor)
- Verify network access to registries

---

## 9. Code Quality Standards

### Styling Rules:
- Use Tailwind utility classes from core library only
- Follow Tailwind's spacing scale (4px increments)
- Maintain consistent color scheme from theme
- Use CSS variables for theme colors (hsl(var(--primary)))

### Component Organization:
```
components/
├── ui/           # Registry components (managed by shadcn)
├── custom/       # Project-specific components
└── layouts/      # Layout components
```

---

## 10. Example Workflows

### Starting a New Feature:
```
1. "Show me all available components in the shadcn registry"
2. Identify required components
3. "Add button, card, dialog, and form components to my project"
4. Wait for installation confirmation
5. Import and use components with proper props
6. Test accessibility and responsiveness
```

### Using Custom Registry:
```
1. Verify registry in components.json
2. "Show me components from @acme registry"
3. "Install @acme/hero-section and @acme/cta-block"
4. Use namespace imports: @/components/acme/hero-section
```

---

## 11. Pre-Implementation Checklist

Before writing ANY UI code:

- [ ] Queried MCP for available components
- [ ] Verified component matches requirements
- [ ] Installed all required components
- [ ] Checked component variants and props
- [ ] Confirmed accessibility features
- [ ] Planned responsive behavior
- [ ] Considered loading and error states

---

## 12. Quality Assurance

Every UI implementation must have:

- **Semantic HTML**: Proper heading hierarchy, landmarks, form labels
- **Keyboard Navigation**: Tab order, focus states, shortcuts
- **Screen Reader Support**: ARIA labels, descriptions, live regions
- **Responsive Design**: Mobile, tablet, desktop breakpoints
- **Performance**: Optimized rendering, lazy loading where appropriate
- **Error Handling**: Validation, error messages, recovery flows
- **Loading States**: Skeletons, spinners, disabled states

---

## Remember:

> **"MCP First, Code Second"**
> 
> Always check the shadcn MCP for component availability and configuration before suggesting or implementing UI components. The registry is the source of truth for component structure, variants, and best practices.

---

## Quick Reference Commands

```bash
# Discovery
"Show me all available components in the shadcn registry"
"Find me a [component-type] from the shadcn registry"
"Show me components from @[namespace] registry"

# Installation
"Add the [component-name] component to my project"
"Add button, card, and dialog components to my project"
"Install @acme/hero-section"

# Building
"Create a [feature] using components from the shadcn registry"
"Build a [page] using [components] from the @[namespace] registry"
```

---

## Anti-Patterns to Avoid

❌ Installing components without checking MCP first
❌ Creating custom components when registry alternatives exist
❌ Ignoring component variants and using custom styling
❌ Skipping accessibility attributes
❌ Hard-coding values instead of using theme variables
❌ Inconsistent spacing and sizing
❌ Missing loading and error states
❌ Poor mobile responsiveness
❌ Excessive DOM nesting
❌ Inline styles instead of Tailwind classes

- Client README: `client/README.md` (Lovable project info)
- Server README: `server/README.md` (API endpoints reference)
- Excel Data Analysis: `server/excel_data_analysis.md` (data schema)
- Feature Docs: `client/*.md` files (implementation summaries)
