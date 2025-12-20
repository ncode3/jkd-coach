# SAMMO Fight IQ - Frontend Integration Index

Complete Lovable frontend integration for SAMMO Fight IQ boxing coach application.

## What's Included

A complete, production-ready React/TypeScript frontend with:
- Authentication system with token management
- Dashboard with auto-refreshing statistics
- Round logging with form validation
- Rounds history with optimistic updates
- Utility functions for formatting and validation
- Comprehensive TypeScript types
- Full documentation and examples

## Quick Start

1. **Read the Quick Reference** (5 minutes)
   - [FRONTEND_QUICK_REFERENCE.md](FRONTEND_QUICK_REFERENCE.md)
   - Essential APIs, hooks, and examples

2. **Review the Integration Guide** (15 minutes)
   - [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md)
   - Complete setup and usage documentation

3. **Check the File Summary** (10 minutes)
   - [FRONTEND_FILES_SUMMARY.md](FRONTEND_FILES_SUMMARY.md)
   - Detailed breakdown of all files

4. **Copy files to your Lovable project**
   ```bash
   # Copy all src/ files
   cp -r src/* /path/to/your/lovable/project/src/

   # Copy environment template
   cp .env.frontend.example /path/to/your/lovable/project/.env
   ```

5. **Configure and run**
   ```bash
   cd /path/to/your/lovable/project

   # Update .env with your backend URL
   echo "VITE_API_URL=http://localhost:8080" > .env

   # Install dependencies (if needed)
   npm install

   # Start dev server
   npm run dev
   ```

## Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| **[FRONTEND_QUICK_REFERENCE.md](FRONTEND_QUICK_REFERENCE.md)** | Quick reference for developers | 5 min |
| **[FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md)** | Complete integration guide | 15 min |
| **[FRONTEND_FILES_SUMMARY.md](FRONTEND_FILES_SUMMARY.md)** | Detailed file breakdown | 10 min |
| **[FRONTEND_INDEX.md](FRONTEND_INDEX.md)** | This file - navigation hub | 2 min |

## Source Code Files

### Core Files (Required)

| File | Lines | Description |
|------|-------|-------------|
| [src/lib/api.ts](src/lib/api.ts) | 299 | API client with all backend methods |
| [src/hooks/useAuth.ts](src/hooks/useAuth.ts) | 197 | Authentication hook |
| [src/hooks/useDashboard.ts](src/hooks/useDashboard.ts) | 109 | Dashboard stats hook |
| [src/hooks/useRounds.ts](src/hooks/useRounds.ts) | 206 | Rounds management hook |
| [src/components/RoundLogger.tsx](src/components/RoundLogger.tsx) | 317 | Round logging form |
| [src/pages/Dashboard.tsx](src/pages/Dashboard.tsx) | 331 | Main dashboard page |

### Utility Files (Optional but Recommended)

| File | Lines | Description |
|------|-------|-------------|
| [src/types/index.ts](src/types/index.ts) | 35 | TypeScript type definitions |
| [src/utils/format.ts](src/utils/format.ts) | 165 | Formatting utilities |
| [src/utils/validation.ts](src/utils/validation.ts) | 194 | Validation utilities |

### Configuration Files

| File | Description |
|------|-------------|
| [.env.frontend.example](.env.frontend.example) | Environment variables template |
| [package.json.frontend.example](package.json.frontend.example) | Package.json template |
| [SETUP_FRONTEND.sh](SETUP_FRONTEND.sh) | Automated setup script |

## File Tree

```
SAMMO Fight IQ Frontend Integration
│
├── Documentation/
│   ├── FRONTEND_INDEX.md                 (This file)
│   ├── FRONTEND_QUICK_REFERENCE.md       (Quick reference)
│   ├── FRONTEND_INTEGRATION.md           (Complete guide)
│   └── FRONTEND_FILES_SUMMARY.md         (File details)
│
├── Source Code/
│   ├── src/lib/
│   │   └── api.ts                        (API client)
│   ├── src/hooks/
│   │   ├── useAuth.ts                    (Authentication)
│   │   ├── useDashboard.ts               (Dashboard stats)
│   │   └── useRounds.ts                  (Rounds management)
│   ├── src/components/
│   │   └── RoundLogger.tsx               (Form component)
│   ├── src/pages/
│   │   └── Dashboard.tsx                 (Main page)
│   ├── src/types/
│   │   └── index.ts                      (Type definitions)
│   └── src/utils/
│       ├── format.ts                     (Formatting utils)
│       └── validation.ts                 (Validation utils)
│
└── Configuration/
    ├── .env.frontend.example             (Environment template)
    ├── package.json.frontend.example     (Dependencies template)
    └── SETUP_FRONTEND.sh                 (Setup script)
```

## Key Features

### Authentication System
- Login/register/logout functionality
- Token storage with expiry tracking
- Automatic session validation
- Persistent authentication across page refreshes

### Dashboard
- Real-time statistics display
- Auto-refresh every 30 seconds
- Total rounds and average danger scores
- Personalized game plan recommendations

### Round Logging
- Form validation for all metrics
- Required core metrics (pressure, ring control, defense, shots)
- Optional advanced metrics (guard down, hip rotation, stance)
- Success/error feedback

### Rounds History
- Display all logged rounds
- Delete functionality with confirmation
- Optimistic UI updates
- Automatic background synchronization

### Type Safety
- Full TypeScript coverage
- Typed API responses
- Compile-time error checking
- Excellent IDE autocomplete

### Error Handling
- Graceful error messages
- Automatic token validation
- Network error recovery
- User-friendly feedback

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   Dashboard                     │
│  (Main UI - shows stats and rounds history)    │
└────────────┬────────────────────────┬───────────┘
             │                        │
    ┌────────▼────────┐      ┌───────▼────────┐
    │  useDashboard   │      │   useRounds    │
    │  (Auto-refresh) │      │  (Optimistic)  │
    └────────┬────────┘      └───────┬────────┘
             │                        │
    ┌────────▼────────────────────────▼────────┐
    │              useAuth                      │
    │        (Token Management)                 │
    └────────┬──────────────────────────────────┘
             │
    ┌────────▼────────┐
    │   API Client    │
    │  (HTTP calls)   │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Backend API    │
    │  (FastAPI)      │
    └─────────────────┘
```

## Data Flow

```
User Action
    ↓
Component
    ↓
Hook (useAuth, useDashboard, useRounds)
    ↓
API Client (src/lib/api.ts)
    ↓
HTTP Request → Backend API
    ↓
HTTP Response
    ↓
API Client (parse & validate)
    ↓
Hook (update state)
    ↓
Component (re-render)
    ↓
Updated UI
```

## Technology Stack

| Layer | Technology |
|-------|------------|
| Language | TypeScript 5.x |
| Framework | React 18.x |
| Build Tool | Vite 5.x |
| Styling | Tailwind CSS 3.x |
| State Management | React Hooks |
| HTTP Client | Fetch API |
| Type System | TypeScript |

## Backend API Integration

The frontend integrates with these FastAPI endpoints:

```
Authentication:
  POST   /auth/register
  POST   /auth/login
  GET    /auth/me

Boxing Data:
  POST   /api/log_round
  GET    /api/dashboard_stats
  GET    /api/rounds_history
  DELETE /api/rounds/{id}

Future:
  POST   /api/upload_video
```

## Environment Configuration

Required environment variable:

```env
VITE_API_URL=http://localhost:8080  # Development
VITE_API_URL=https://api.example.com # Production
```

## Installation Steps

### Manual Installation

1. **Copy files**
   ```bash
   cp -r src/* /your/lovable/project/src/
   ```

2. **Create .env**
   ```bash
   cp .env.frontend.example /your/lovable/project/.env
   ```

3. **Update environment**
   ```bash
   # Edit .env
   VITE_API_URL=http://localhost:8080
   ```

4. **Install dependencies**
   ```bash
   cd /your/lovable/project
   npm install
   ```

5. **Start dev server**
   ```bash
   npm run dev
   ```

### Automated Setup

Use the setup script:

```bash
cd /your/lovable/project
bash /path/to/SETUP_FRONTEND.sh
```

## Usage Examples

### Basic Authentication

```typescript
import { useAuth } from '@/hooks/useAuth';

function LoginPage() {
  const { login, isLoading, error } = useAuth();

  const handleLogin = async () => {
    await login('username', 'password');
  };

  return (
    <button onClick={handleLogin} disabled={isLoading}>
      {isLoading ? 'Logging in...' : 'Login'}
    </button>
  );
}
```

### Display Dashboard

```typescript
import Dashboard from '@/pages/Dashboard';

function App() {
  const { isAuthenticated } = useAuth();

  return isAuthenticated ? <Dashboard /> : <LoginPage />;
}
```

### Log a Round

```typescript
import { useRounds } from '@/hooks/useRounds';

function LogRoundForm() {
  const { logRound, isSubmitting } = useRounds(token);

  const handleSubmit = async () => {
    await logRound({
      pressure_score: 7.5,
      ring_control_score: 8.0,
      defense_score: 6.5,
      clean_shots_taken: 12,
    });
  };

  return (
    <button onClick={handleSubmit} disabled={isSubmitting}>
      Log Round
    </button>
  );
}
```

## Common Customizations

### Change Auto-Refresh Interval

Edit `src/hooks/useDashboard.ts`:
```typescript
const AUTO_REFRESH_INTERVAL = 60000; // 60 seconds
```

### Change Danger Score Colors

Edit `src/utils/format.ts`:
```typescript
const colorMap = {
  low: 'text-blue-600',      // Change colors
  moderate: 'text-green-600',
  high: 'text-yellow-600',
  critical: 'text-red-600',
};
```

### Add Custom Validation

Edit `src/utils/validation.ts`:
```typescript
export const validateCustomField = (value: any) => {
  // Your validation logic
};
```

## Testing

### Test API Client
```typescript
import { api } from '@/lib/api';

const response = await api.login('test', 'test');
console.log(response);
```

### Test Hooks
```typescript
import { renderHook } from '@testing-library/react';
import { useAuth } from '@/hooks/useAuth';

const { result } = renderHook(() => useAuth());
```

## Troubleshooting

### CORS Issues
Ensure backend allows frontend origin:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Import Path Issues
Check path aliases in:
- `tsconfig.json` → `"@/*": ["./src/*"]`
- `vite.config.ts` → `'@': path.resolve(__dirname, './src')`

### Token Expiry
Hook handles automatically:
- Validates token on mount
- Redirects to login if expired
- Clears expired tokens

## Performance Tips

1. Disable auto-refresh when not needed
2. Use pagination for large lists
3. Memoize expensive calculations
4. Use React.memo for static components
5. Optimize images and assets

## Security Considerations

1. Use HTTPS in production
2. Consider httpOnly cookies
3. Implement token refresh
4. Add rate limiting
5. Validate all inputs
6. Sanitize user content

## Next Steps

1. ✅ Copy files to your project
2. ✅ Configure environment
3. ✅ Start development
4. ⏭ Create Login/Register pages
5. ⏭ Add React Router
6. ⏭ Customize styling
7. ⏭ Add video upload UI
8. ⏭ Add analytics
9. ⏭ Deploy to production

## Support

### Documentation
- **Quick Start**: [FRONTEND_QUICK_REFERENCE.md](FRONTEND_QUICK_REFERENCE.md)
- **Complete Guide**: [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md)
- **File Details**: [FRONTEND_FILES_SUMMARY.md](FRONTEND_FILES_SUMMARY.md)

### Backend
- **API Server**: `deployments/fastapi-auth/`
- **API Docs**: Visit `http://localhost:8080/docs` when backend is running

### External Resources
- [React Documentation](https://react.dev)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## License

MIT License - Same as SAMMO Fight IQ project

## Credits

Built for **SAMMO Fight IQ** - AI-Powered Boxing Coach
Based on the legacy of **Jimmy Carter**, 3x World Lightweight Champion

---

**Total Package**: 12 files including 9 source code files and 3 documentation files
**Total Lines of Code**: ~1,850 lines
**Production Ready**: Yes
**Framework**: React + TypeScript + Tailwind CSS
**Compatibility**: Lovable and any modern React setup

---

## Getting Help

1. **Read the Quick Reference** first
2. **Check the Integration Guide** for detailed setup
3. **Review File Summary** for specific file details
4. **Check backend API documentation** at `/docs` endpoint
5. **Review backend README** in `deployments/fastapi-auth/`

---

**Ready to start?** Begin with [FRONTEND_QUICK_REFERENCE.md](FRONTEND_QUICK_REFERENCE.md)
