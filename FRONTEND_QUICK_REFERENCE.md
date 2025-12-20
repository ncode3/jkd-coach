# SAMMO Fight IQ - Frontend Quick Reference

Quick reference guide for developers using the SAMMO Fight IQ frontend integration.

## File Locations

```
src/lib/api.ts              → API client
src/hooks/useAuth.ts        → Authentication
src/hooks/useDashboard.ts   → Dashboard stats
src/hooks/useRounds.ts      → Rounds management
src/components/RoundLogger.tsx → Round form
src/pages/Dashboard.tsx     → Main dashboard
src/types/index.ts          → Type definitions
src/utils/format.ts         → Formatting helpers
src/utils/validation.ts     → Validation helpers
```

## Quick Imports

```typescript
// API Client
import { api } from '@/lib/api';

// Hooks
import { useAuth } from '@/hooks/useAuth';
import { useDashboard } from '@/hooks/useDashboard';
import { useRounds } from '@/hooks/useRounds';

// Components
import { RoundLogger } from '@/components/RoundLogger';
import Dashboard from '@/pages/Dashboard';

// Types
import type { User, Round, RoundData, DashboardStats } from '@/lib/api';

// Utils
import { formatDate, getDangerScoreColor } from '@/utils/format';
import { validateRoundData } from '@/utils/validation';
```

## Hook Usage

### useAuth

```typescript
const {
  user,              // User | null
  token,             // string | null
  isAuthenticated,   // boolean
  isLoading,         // boolean
  error,             // string | null
  login,             // (username, password) => Promise<void>
  register,          // (email, password, username?) => Promise<void>
  logout,            // () => void
  clearError,        // () => void
} = useAuth();

// Login
await login('username', 'password');

// Register
await register('email@example.com', 'password', 'username');

// Logout
logout();
```

### useDashboard

```typescript
const {
  stats,        // DashboardStats | null
  isLoading,    // boolean
  error,        // string | null
  fetchStats,   // () => Promise<void>
  refresh,      // () => void
  clearError,   // () => void
} = useDashboard(token);  // Auto-refresh every 30s

// Disable auto-refresh
const { stats } = useDashboard(token, false);

// Manual refresh
refresh();
```

### useRounds

```typescript
const {
  rounds,        // Round[]
  total,         // number
  isLoading,     // boolean
  error,         // string | null
  isSubmitting,  // boolean
  fetchHistory,  // (limit?) => Promise<void>
  logRound,      // (roundData) => Promise<LogRoundResponse>
  deleteRound,   // (roundId) => Promise<void>
  refresh,       // () => void
  clearError,    // () => void
} = useRounds(token);

// Log round
const response = await logRound({
  pressure_score: 7.5,
  ring_control_score: 8.0,
  defense_score: 6.5,
  clean_shots_taken: 12,
});

// Delete round
await deleteRound('round-id');

// Fetch more
await fetchHistory(50);
```

## API Client Direct Usage

```typescript
import { api } from '@/lib/api';

// Register
const { user } = await api.register('email@example.com', 'password', 'username');

// Login
const { access_token, expires_in } = await api.login('username', 'password');

// Get current user
const user = await api.getMe(token);

// Log round
const { id, danger_score, strategy } = await api.logRound(token, roundData);

// Get stats
const stats = await api.getDashboardStats(token);

// Get rounds
const { rounds, total } = await api.getRoundsHistory(token, 100);

// Delete round
await api.deleteRound(token, 'round-id');

// Upload video
await api.uploadVideo(token, videoFile);
```

## TypeScript Types

### User
```typescript
interface User {
  id: string;
  username: string;
  email: string;
  created_at?: string;
}
```

### RoundData
```typescript
interface RoundData {
  pressure_score: number;          // Required: 0-10
  ring_control_score: number;      // Required: 0-10
  defense_score: number;           // Required: 0-10
  clean_shots_taken: number;       // Required: >= 0
  guard_down_ratio?: number;       // Optional: 0-1
  avg_hip_rotation?: number;       // Optional: 0-180
  avg_stance_width?: number;       // Optional: 0-1
  notes?: string;                  // Optional
}
```

### Round
```typescript
interface Round {
  id: string;
  user_id: string;
  pressure_score: number;
  ring_control_score: number;
  defense_score: number;
  clean_shots_taken: number;
  guard_down_ratio?: number;
  avg_hip_rotation?: number;
  avg_stance_width?: number;
  danger_score: number;
  strategy?: string;
  notes?: string;
  created_at: string;
}
```

### DashboardStats
```typescript
interface DashboardStats {
  total_rounds: number;
  avg_danger_score: number;
  next_game_plan: string;
  averages?: {
    pressure_score?: number;
    ring_control_score?: number;
    defense_score?: number;
    danger_score?: number;
  };
  most_recent_round_date?: string;
}
```

## Formatting Utilities

```typescript
import {
  formatDate,              // (dateString, options?) => string
  formatRelativeTime,      // (dateString) => string
  formatNumber,            // (num, decimals?) => string
  getDangerLevel,          // (score) => 'low' | 'moderate' | 'high' | 'critical'
  getDangerScoreColor,     // (score) => string (Tailwind class)
  getDangerScoreBadge,     // (score) => string (Tailwind classes)
  formatPercentage,        // (value) => string
  formatDegrees,           // (value) => string
} from '@/utils/format';

// Examples
formatDate('2024-01-15T10:30:00Z');
// → "Jan 15, 2024, 10:30 AM"

formatRelativeTime('2024-01-15T10:30:00Z');
// → "2 hours ago"

getDangerLevel(0.65);
// → "high"

getDangerScoreColor(0.65);
// → "text-orange-600"

formatPercentage(0.38);
// → "38%"

formatDegrees(28.5);
// → "28.5°"
```

## Validation Utilities

```typescript
import {
  validateEmail,         // (email) => boolean
  validatePassword,      // (password) => ValidationResult
  validateUsername,      // (username) => ValidationResult
  validateRoundData,     // (data) => ValidationResult
  validateScore,         // (score) => boolean
  validateRatio,         // (ratio) => boolean
  validateAngle,         // (angle) => boolean
} from '@/utils/validation';

// Examples
validateEmail('user@example.com');
// → true

const { isValid, errors } = validatePassword('weak');
// → { isValid: false, errors: { ... } }

const { isValid, errors } = validateRoundData(roundData);
// → { isValid: true, errors: {} }

validateScore(7.5);  // → true (0-10)
validateRatio(0.38); // → true (0-1)
validateAngle(45);   // → true (0-180)
```

## Component Usage

### RoundLogger

```typescript
<RoundLogger
  onSuccess={(response) => {
    console.log('Danger score:', response.danger_score);
    console.log('Strategy:', response.strategy);
  }}
  onError={(error) => {
    console.error('Failed:', error.message);
  }}
/>
```

### Dashboard

```typescript
// Full page component - use as main view
<Dashboard />
```

## Environment Variables

```env
# .env file
VITE_API_URL=http://localhost:8080
```

```typescript
// Access in code
const apiUrl = import.meta.env.VITE_API_URL;
```

## Error Handling

```typescript
// All hooks return error state
const { error, clearError } = useAuth();

if (error) {
  // Display to user
  console.error(error);

  // Clear when done
  clearError();
}

// Try-catch for async operations
try {
  await login(username, password);
} catch (error) {
  if (error instanceof Error) {
    console.error(error.message);
  }
}
```

## Loading States

```typescript
// Authentication
const { isLoading } = useAuth();
if (isLoading) return <LoadingSpinner />;

// Dashboard
const { isLoading } = useDashboard(token);
if (isLoading) return <Skeleton />;

// Rounds
const { isLoading, isSubmitting } = useRounds(token);
if (isLoading) return <LoadingSpinner />;
if (isSubmitting) return <button disabled>Submitting...</button>;
```

## Token Management

```typescript
// Stored automatically by useAuth
const { token } = useAuth();

// Token is stored in localStorage as:
localStorage.getItem('sammo_auth_token');
localStorage.getItem('sammo_auth_expiry');

// Cleared on logout
logout(); // Removes from localStorage
```

## Backend Endpoints

```
POST   /auth/register      → Register user
POST   /auth/login         → Login
GET    /auth/me            → Get current user
POST   /api/log_round      → Log round
GET    /api/dashboard_stats → Get stats
GET    /api/rounds_history → Get rounds
DELETE /api/rounds/{id}    → Delete round
POST   /api/upload_video   → Upload video (future)
```

## Common Patterns

### Protected Route
```typescript
function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) return <LoadingSpinner />;
  if (!isAuthenticated) return <Navigate to="/login" />;

  return children;
}
```

### Auto-Refresh Data
```typescript
// Dashboard hook auto-refreshes every 30s
const { stats } = useDashboard(token);

// Disable auto-refresh
const { stats, refresh } = useDashboard(token, false);

// Manual refresh when needed
<button onClick={refresh}>Refresh</button>
```

### Optimistic Updates
```typescript
// Rounds hook handles optimistic updates automatically
const { logRound, deleteRound } = useRounds(token);

// UI updates immediately, syncs in background
await logRound(roundData);  // Immediate UI update
await deleteRound(id);      // Immediate removal, rollback on error
```

## Danger Score Thresholds

```typescript
// Used in getDangerLevel()
const thresholds = {
  low: 0.3,       // < 0.3 = green
  moderate: 0.5,  // 0.3-0.5 = yellow
  high: 0.7,      // 0.5-0.7 = orange
  // >= 0.7 = red
};
```

## Tailwind Color Classes

```typescript
// Text colors
'text-green-600'   // Low risk
'text-yellow-600'  // Moderate risk
'text-orange-600'  // High risk
'text-red-600'     // Critical risk

// Badge backgrounds
'bg-green-100 text-green-800'
'bg-yellow-100 text-yellow-800'
'bg-orange-100 text-orange-800'
'bg-red-100 text-red-800'
```

## localStorage Keys

```typescript
'sammo_auth_token'   // JWT token
'sammo_auth_expiry'  // Token expiry timestamp
```

## Common Issues & Solutions

### CORS Error
```typescript
// Backend needs CORS configuration
// In FastAPI:
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
```

### Import Path Not Found
```typescript
// Check tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  }
}

// Check vite.config.ts
export default defineConfig({
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') }
  }
});
```

### Token Expired
```typescript
// Hook handles automatically
// If expired, sets isAuthenticated = false
// User redirected to login
```

## Testing Quick Start

```typescript
// Test API client
import { api } from '@/lib/api';
const response = await api.login('test', 'test');
console.log(response);

// Test hook
import { renderHook } from '@testing-library/react';
import { useAuth } from '@/hooks/useAuth';
const { result } = renderHook(() => useAuth());
```

## Development Checklist

- [ ] Backend running on port 8080
- [ ] Frontend running on port 5173
- [ ] .env file created with VITE_API_URL
- [ ] CORS configured in backend
- [ ] Path aliases configured
- [ ] Tailwind CSS setup
- [ ] Test login flow
- [ ] Test round logging
- [ ] Test dashboard display

## Production Checklist

- [ ] Update VITE_API_URL to production URL
- [ ] Build frontend: `npm run build`
- [ ] Test production build: `npm run preview`
- [ ] Configure backend CORS for production domain
- [ ] Set up HTTPS
- [ ] Configure token expiry appropriately
- [ ] Set up error monitoring
- [ ] Add analytics

## Performance Tips

1. Use `autoRefresh: false` when not needed
2. Increase auto-refresh interval if needed (30s default)
3. Use pagination for large round lists
4. Memoize expensive calculations
5. Use React.memo for static components

## Security Best Practices

1. Always use HTTPS in production
2. Consider httpOnly cookies instead of localStorage
3. Implement token refresh mechanism
4. Add rate limiting on backend
5. Validate all inputs
6. Sanitize user content
7. Use CSP headers

---

**Quick Links**:
- Full Guide: `FRONTEND_INTEGRATION.md`
- File Summary: `FRONTEND_FILES_SUMMARY.md`
- Backend API: `deployments/fastapi-auth/`
