/**
 * SAMMO Fight IQ - Dashboard Page
 * Main dashboard displaying boxing statistics and recent rounds
 */

import React, { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useDashboard } from '@/hooks/useDashboard';
import { useRounds } from '@/hooks/useRounds';
import { RoundLogger } from '@/components/RoundLogger';
import { LogRoundResponse } from '@/lib/api';

/**
 * Dashboard Component
 * Displays user stats, recent rounds, and round logger
 */
export const Dashboard: React.FC = () => {
  const { user, token, logout } = useAuth();
  const { stats, isLoading: statsLoading, error: statsError, refresh: refreshStats } = useDashboard(token);
  const {
    rounds,
    total,
    isLoading: roundsLoading,
    error: roundsError,
    deleteRound,
    refresh: refreshRounds
  } = useRounds(token);

  const [showLogger, setShowLogger] = useState(false);
  const [deletingRoundId, setDeletingRoundId] = useState<string | null>(null);

  /**
   * Handle successful round logging
   */
  const handleLogSuccess = (response: LogRoundResponse) => {
    // Close logger
    setShowLogger(false);

    // Refresh both stats and rounds
    refreshStats();
    refreshRounds();
  };

  /**
   * Handle round deletion
   */
  const handleDeleteRound = async (roundId: string) => {
    if (!confirm('Are you sure you want to delete this round?')) {
      return;
    }

    setDeletingRoundId(roundId);
    try {
      await deleteRound(roundId);
      // Refresh stats after deletion
      refreshStats();
    } catch (error) {
      console.error('Failed to delete round:', error);
    } finally {
      setDeletingRoundId(null);
    }
  };

  /**
   * Format date
   */
  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  /**
   * Get danger score color
   */
  const getDangerScoreColor = (score: number): string => {
    if (score < 0.3) return 'text-green-600';
    if (score < 0.5) return 'text-yellow-600';
    if (score < 0.7) return 'text-orange-600';
    return 'text-red-600';
  };

  /**
   * Get danger score badge
   */
  const getDangerScoreBadge = (score: number): string => {
    if (score < 0.3) return 'bg-green-100 text-green-800';
    if (score < 0.5) return 'bg-yellow-100 text-yellow-800';
    if (score < 0.7) return 'bg-orange-100 text-orange-800';
    return 'bg-red-100 text-red-800';
  };

  return (
    <div className="dashboard min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">SAMMO Fight IQ</h1>
              <p className="text-gray-600 mt-1">
                Welcome back, {user?.username || 'Fighter'}
              </p>
            </div>
            <div className="flex gap-4">
              <button
                onClick={() => setShowLogger(!showLogger)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700"
              >
                {showLogger ? 'Hide Logger' : 'Log Round'}
              </button>
              <button
                onClick={logout}
                className="px-4 py-2 border border-gray-300 rounded-lg font-medium hover:bg-gray-50"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Round Logger */}
        {showLogger && (
          <div className="mb-8 bg-white rounded-lg shadow-md p-6">
            <RoundLogger onSuccess={handleLogSuccess} />
          </div>
        )}

        {/* Stats Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Your Statistics</h2>

          {statsError && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
              {statsError}
            </div>
          )}

          {statsLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
                  <div className="h-8 bg-gray-200 rounded w-3/4"></div>
                </div>
              ))}
            </div>
          ) : stats ? (
            <>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                {/* Total Rounds */}
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-sm text-gray-600 mb-2">Total Rounds</div>
                  <div className="text-3xl font-bold text-gray-900">
                    {stats.total_rounds}
                  </div>
                  {stats.most_recent_round_date && (
                    <div className="text-xs text-gray-500 mt-2">
                      Last: {formatDate(stats.most_recent_round_date)}
                    </div>
                  )}
                </div>

                {/* Average Danger Score */}
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-sm text-gray-600 mb-2">Avg Danger Score</div>
                  <div className={`text-3xl font-bold ${getDangerScoreColor(stats.avg_danger_score)}`}>
                    {stats.avg_danger_score.toFixed(2)}
                  </div>
                  <div className="text-xs text-gray-500 mt-2">
                    {stats.avg_danger_score < 0.5 ? 'Good control!' : 'Room for improvement'}
                  </div>
                </div>

                {/* Average Scores */}
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-sm text-gray-600 mb-2">Average Scores</div>
                  {stats.averages ? (
                    <div className="space-y-1 text-sm">
                      {stats.averages.pressure_score !== undefined && (
                        <div className="flex justify-between">
                          <span>Pressure:</span>
                          <span className="font-semibold">{stats.averages.pressure_score.toFixed(1)}</span>
                        </div>
                      )}
                      {stats.averages.ring_control_score !== undefined && (
                        <div className="flex justify-between">
                          <span>Ring Control:</span>
                          <span className="font-semibold">{stats.averages.ring_control_score.toFixed(1)}</span>
                        </div>
                      )}
                      {stats.averages.defense_score !== undefined && (
                        <div className="flex justify-between">
                          <span>Defense:</span>
                          <span className="font-semibold">{stats.averages.defense_score.toFixed(1)}</span>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="text-gray-400">No data yet</div>
                  )}
                </div>
              </div>

              {/* Game Plan */}
              {stats.next_game_plan && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-blue-900 mb-2">
                    Next Game Plan
                  </h3>
                  <p className="text-blue-800 whitespace-pre-wrap">{stats.next_game_plan}</p>
                </div>
              )}
            </>
          ) : (
            <div className="bg-gray-100 rounded-lg p-8 text-center text-gray-600">
              No statistics available yet. Log your first round to get started!
            </div>
          )}
        </div>

        {/* Recent Rounds Section */}
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold">Recent Rounds</h2>
            <button
              onClick={refreshRounds}
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              Refresh
            </button>
          </div>

          {roundsError && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
              {roundsError}
            </div>
          )}

          {roundsLoading ? (
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
                  <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                </div>
              ))}
            </div>
          ) : rounds.length > 0 ? (
            <div className="space-y-4">
              {rounds.map((round) => (
                <div
                  key={round.id}
                  className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
                >
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <div className="text-sm text-gray-500">
                        {formatDate(round.created_at)}
                      </div>
                      <div className="mt-1">
                        <span
                          className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getDangerScoreBadge(
                            round.danger_score
                          )}`}
                        >
                          Danger: {round.danger_score.toFixed(2)}
                        </span>
                      </div>
                    </div>
                    <button
                      onClick={() => handleDeleteRound(round.id)}
                      disabled={deletingRoundId === round.id}
                      className="text-red-600 hover:text-red-800 font-medium disabled:opacity-50"
                    >
                      {deletingRoundId === round.id ? 'Deleting...' : 'Delete'}
                    </button>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                    <div>
                      <div className="text-xs text-gray-500">Pressure</div>
                      <div className="text-lg font-semibold">{round.pressure_score.toFixed(1)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500">Ring Control</div>
                      <div className="text-lg font-semibold">{round.ring_control_score.toFixed(1)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500">Defense</div>
                      <div className="text-lg font-semibold">{round.defense_score.toFixed(1)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500">Clean Shots</div>
                      <div className="text-lg font-semibold">{round.clean_shots_taken}</div>
                    </div>
                  </div>

                  {/* Advanced Metrics */}
                  {(round.guard_down_ratio !== undefined ||
                    round.avg_hip_rotation !== undefined ||
                    round.avg_stance_width !== undefined) && (
                    <div className="grid grid-cols-3 gap-4 mb-4 pt-4 border-t">
                      {round.guard_down_ratio !== undefined && (
                        <div>
                          <div className="text-xs text-gray-500">Guard Down</div>
                          <div className="text-sm font-medium">
                            {(round.guard_down_ratio * 100).toFixed(0)}%
                          </div>
                        </div>
                      )}
                      {round.avg_hip_rotation !== undefined && (
                        <div>
                          <div className="text-xs text-gray-500">Hip Rotation</div>
                          <div className="text-sm font-medium">{round.avg_hip_rotation.toFixed(1)}°</div>
                        </div>
                      )}
                      {round.avg_stance_width !== undefined && (
                        <div>
                          <div className="text-xs text-gray-500">Stance Width</div>
                          <div className="text-sm font-medium">{round.avg_stance_width.toFixed(2)}</div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Strategy */}
                  {round.strategy && (
                    <div className="pt-4 border-t">
                      <div className="text-xs text-gray-500 mb-1">Strategy</div>
                      <div className="text-sm text-gray-700">{round.strategy}</div>
                    </div>
                  )}

                  {/* Notes */}
                  {round.notes && (
                    <div className="pt-4 border-t mt-4">
                      <div className="text-xs text-gray-500 mb-1">Notes</div>
                      <div className="text-sm text-gray-700">{round.notes}</div>
                    </div>
                  )}
                </div>
              ))}

              {/* Pagination Info */}
              {total > rounds.length && (
                <div className="text-center text-gray-500 text-sm">
                  Showing {rounds.length} of {total} rounds
                </div>
              )}
            </div>
          ) : (
            <div className="bg-gray-100 rounded-lg p-8 text-center text-gray-600">
              No rounds logged yet. Click "Log Round" to get started!
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
