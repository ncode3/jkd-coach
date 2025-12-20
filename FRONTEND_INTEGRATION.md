# SAMMO Fight IQ - Frontend Integration Guide

Complete Lovable frontend integration for SAMMO Fight IQ with TypeScript, React hooks, and modern patterns.

## Overview

This frontend integration provides a complete React/TypeScript client for the SAMMO Fight IQ backend API, including authentication, dashboard statistics, and round logging functionality.

## Files Created

### 1. API Client (`src/lib/api.ts`)

**Purpose**: Central API client for all backend communication

**Features**:
- TypeScript interfaces for all API requests/responses
- Singleton API client instance
- Error handling with typed responses
- Environment-based API URL configuration

**Methods**:
- `register(email, password, username?)` - Register new user
- `login(username, password)` - User authentication
- `getMe(token)` - Get current user profile
- `logRound(token, roundData)` - Log boxing round with metrics
- `getDashboardStats(token)` - Get user statistics
- `getRoundsHistory(token, limit?)` - Fetch rounds history
- `deleteRound(token, roundId)` - Delete a round
- `uploadVideo(token, videoFile)` - Upload video for future pose detection

**TypeScript Types**:
```typescript
interface RoundData {
  pressure_score: number;
  ring_control_score: number;
  defense_score: number;
  clean_shots_taken: number;
  guard_down_ratio?: number;
  avg_hip_rotation?: number;
  avg_stance_width?: number;
  notes?: string;
}

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

### 2. Authentication Hook (`src/hooks/useAuth.ts`)

**Purpose**: Manage user authentication state and token persistence

**Features**:
- Token storage in localStorage with expiry tracking
- Automatic token validation on mount
- Session persistence across page refreshes
- Loading and error states

**State**:
```typescript
{
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}
```

**Methods**:
- `login(username, password)` - Authenticate user
- `register(email, password, username?)` - Register and auto-login
- `logout()` - Clear session
- `clearError()` - Clear error messages

**Usage**:
```typescript
const { user, token, isAuthenticated, login, logout, isLoading, error } = useAuth();

// Login
await login('username', 'password');

// Register
await register('user@example.com', 'password', 'username');

// Logout
logout();
```

### 3. Dashboard Hook (`src/hooks/useDashboard.ts`)

**Purpose**: Fetch and manage dashboard statistics with auto-refresh

**Features**:
- Auto-refresh every 30 seconds (configurable)
- Manual refresh capability
- Loading and error states
- Automatic cleanup on unmount

**State**:
```typescript
{
  stats: DashboardStats | null;
  isLoading: boolean;
  error: string | null;
}
```

**Methods**:
- `fetchStats()` - Fetch statistics manually
- `refresh()` - Trigger immediate refresh
- `clearError()` - Clear error messages

**Usage**:
```typescript
const { stats, isLoading, error, refresh } = useDashboard(token);

// Auto-refreshes every 30 seconds
// Disable auto-refresh:
const { stats } = useDashboard(token, false);

// Manual refresh
refresh();
```

### 4. Rounds Management Hook (`src/hooks/useRounds.ts`)

**Purpose**: Manage rounds history with optimistic updates

**Features**:
- Optimistic UI updates for better UX
- Automatic rollback on errors
- Background data synchronization
- Loading and error states

**State**:
```typescript
{
  rounds: Round[];
  total: number;
  isLoading: boolean;
  error: string | null;
  isSubmitting: boolean;
}
```

**Methods**:
- `fetchHistory(limit?)` - Fetch rounds history
- `logRound(roundData)` - Log new round (optimistic update)
- `deleteRound(roundId)` - Delete round (optimistic update)
- `refresh()` - Refresh rounds list
- `clearError()` - Clear error messages

**Usage**:
```typescript
const { rounds, total, logRound, deleteRound, isLoading } = useRounds(token);

// Log a new round
await logRound({
  pressure_score: 7.5,
  ring_control_score: 8.0,
  defense_score: 6.5,
  clean_shots_taken: 12,
  notes: 'Great session!'
});

// Delete a round
await deleteRound('round-id');
```

### 5. Round Logger Component (`src/components/RoundLogger.tsx`)

**Purpose**: Form component for logging round data

**Features**:
- Required core metrics (pressure, ring control, defense, clean shots)
- Optional advanced metrics (guard down ratio, hip rotation, stance width)
- Collapsible advanced section
- Form validation
- Success/error feedback
- Reset functionality

**Props**:
```typescript
interface RoundLoggerProps {
  onSuccess?: (response: LogRoundResponse) => void;
  onError?: (error: Error) => void;
}
```

**Usage**:
```typescript
<RoundLogger
  onSuccess={(response) => {
    console.log('Round logged:', response);
    // Handle success
  }}
  onError={(error) => {
    console.error('Failed to log round:', error);
  }}
/>
```

### 6. Dashboard Page (`src/pages/Dashboard.tsx`)

**Purpose**: Main dashboard displaying statistics and rounds

**Features**:
- User welcome header with logout
- Statistics cards (total rounds, avg danger score, averages)
- Game plan display
- Recent rounds list with details
- Integrated round logger
- Delete functionality with confirmation
- Auto-refresh for stats
- Loading states and error handling
- Color-coded danger scores

**Sections**:
1. **Header**: User info, Log Round button, Logout
2. **Stats Section**: Total rounds, average danger score, score averages, game plan
3. **Recent Rounds**: List of logged rounds with all metrics and actions

## Environment Configuration

Create a `.env` file in your frontend root:

```env
VITE_API_URL=http://localhost:8080
```

For production:
```env
VITE_API_URL=https://your-production-api.com
```

## TypeScript Configuration

Ensure your `tsconfig.json` includes path aliases:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

If using Vite, add to `vite.config.ts`:

```typescript
import path from 'path';
import { defineConfig } from 'vite';

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

## Backend API Endpoints

The frontend integrates with these backend endpoints:

### Authentication
- `POST /auth/register` - Register new user
  - Body: `{username, email, password}`
  - Response: `{status, user}`

- `POST /auth/login` - User login
  - Body: `{username, password}`
  - Response: `{access_token, token_type, expires_in}`

- `GET /auth/me` - Get current user
  - Headers: `Authorization: Bearer {token}`
  - Response: User object

### Boxing Data
- `POST /api/log_round` - Log sparring round
  - Headers: `Authorization: Bearer {token}`
  - Body: `{pressure_score, ring_control_score, defense_score, clean_shots_taken, notes, ...}`
  - Response: `{status, id, danger_score, strategy}`

- `GET /api/dashboard_stats` - Get user statistics
  - Headers: `Authorization: Bearer {token}`
  - Response: `{total_rounds, avg_danger_score, next_game_plan, averages, most_recent_round_date}`

- `GET /api/rounds_history?limit=100` - Get rounds history
  - Headers: `Authorization: Bearer {token}`
  - Response: `{rounds, total}`

- `DELETE /api/rounds/{id}` - Delete round
  - Headers: `Authorization: Bearer {token}`
  - Response: `{status, message}`

## Integration Example

### Complete App Setup

```typescript
// App.tsx
import React from 'react';
import { useAuth } from '@/hooks/useAuth';
import Dashboard from '@/pages/Dashboard';
import Login from '@/pages/Login'; // You'll need to create this

function App() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return isAuthenticated ? <Dashboard /> : <Login />;
}

export default App;
```

### Login Page Example

```typescript
// src/pages/Login.tsx
import React, { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';

export const Login: React.FC = () => {
  const { login, register, error, isLoading } = useAuth();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (mode === 'login') {
        await login(username, password);
      } else {
        await register(email, password, username);
      }
    } catch (err) {
      console.error('Auth error:', err);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white rounded-lg shadow-md p-8">
        <h2 className="text-2xl font-bold mb-6">
          {mode === 'login' ? 'Login' : 'Register'}
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === 'register' && (
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2 border rounded-lg"
            />
          )}
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="w-full px-4 py-2 border rounded-lg"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full px-4 py-2 border rounded-lg"
          />

          {error && (
            <div className="text-red-600 text-sm">{error}</div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
          >
            {isLoading ? 'Please wait...' : mode === 'login' ? 'Login' : 'Register'}
          </button>
        </form>

        <button
          onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
          className="w-full mt-4 text-blue-600 hover:text-blue-800"
        >
          {mode === 'login' ? 'Need an account? Register' : 'Have an account? Login'}
        </button>
      </div>
    </div>
  );
};

export default Login;
```

## Error Handling

All hooks and components include comprehensive error handling:

- **Network errors**: Caught and displayed to user
- **Authentication errors**: Token validation and automatic logout
- **Validation errors**: Form-level validation with user feedback
- **API errors**: Parsed from backend and displayed with context

## Loading States

All data fetching includes loading indicators:

- `isLoading` - Initial data fetch
- `isSubmitting` - Form submission in progress
- Skeleton loaders in Dashboard for better UX

## Optimistic Updates

The `useRounds` hook implements optimistic updates for better UX:

1. **Log Round**: Immediately adds round to list, syncs in background
2. **Delete Round**: Immediately removes from list, rolls back on error

## Auto-Refresh

The `useDashboard` hook auto-refreshes every 30 seconds:

- Keeps statistics current
- Configurable via `autoRefresh` parameter
- Automatic cleanup prevents memory leaks

## Security Features

- Token stored in localStorage with expiry tracking
- Automatic token validation on app load
- Token included in all authenticated requests
- Logout clears all authentication data

## Styling

The components use Tailwind CSS classes. Ensure Tailwind is configured in your project:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## Next Steps

1. **Create Login/Register pages** - Use the example above
2. **Add routing** - Use React Router for navigation
3. **Customize styling** - Adjust Tailwind classes to match your design
4. **Add video upload UI** - Integrate with `api.uploadVideo()`
5. **Add more visualizations** - Charts for progress tracking
6. **Add notifications** - Toast messages for actions
7. **Add profile page** - User settings and preferences

## Testing

Test the integration:

```bash
# Start backend (in deployments/fastapi-auth/)
python api_server.py

# Start frontend (in your Lovable project)
npm run dev

# Visit http://localhost:5173 (or your Vite port)
```

## Troubleshooting

### CORS Issues
If you see CORS errors, ensure your backend allows the frontend origin:

```python
# In your FastAPI app
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Import Path Issues
If you see module not found errors, check:
1. TypeScript path aliases in `tsconfig.json`
2. Vite alias configuration in `vite.config.ts`

### Token Expiry
Tokens expire after the duration set by backend. The hook handles this automatically by:
1. Checking expiry on mount
2. Validating with `/auth/me` endpoint
3. Clearing expired tokens

## API Client Usage

You can also use the API client directly without hooks:

```typescript
import { api } from '@/lib/api';

// Direct API calls
const response = await api.login('username', 'password');
const stats = await api.getDashboardStats(token);
const rounds = await api.getRoundsHistory(token, 50);
```

## Type Safety

All API responses are fully typed. TypeScript will catch:
- Missing required fields
- Incorrect data types
- Invalid method signatures

Example:
```typescript
// TypeScript error: missing required fields
await logRound({ pressure_score: 7 }); // Error!

// Correct
await logRound({
  pressure_score: 7,
  ring_control_score: 8,
  defense_score: 6,
  clean_shots_taken: 10
}); // ✓
```

## Performance Considerations

- **Memoization**: Hooks use `useCallback` to prevent unnecessary re-renders
- **Cleanup**: All intervals and subscriptions properly cleaned up
- **Optimistic Updates**: Immediate UI feedback without waiting for server
- **Auto-refresh**: Configurable to reduce unnecessary API calls

## Future Enhancements

1. **WebSocket Support**: Real-time updates for multi-device usage
2. **Offline Support**: Local storage and sync when online
3. **Video Upload Progress**: Track upload progress with progress bars
4. **Advanced Analytics**: Charts and graphs for trend analysis
5. **Social Features**: Share rounds and compare with others

## Support

For issues or questions:
1. Check backend API is running and accessible
2. Verify environment variables are set correctly
3. Check browser console for detailed error messages
4. Ensure token hasn't expired

---

**Built for SAMMO Fight IQ** - AI-Powered Boxing Coach
