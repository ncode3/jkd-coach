/**
 * SAMMO Fight IQ - Formatting Utilities
 * Helper functions for formatting data in the UI
 */

/**
 * Format a date string to a readable format
 */
export const formatDate = (
  dateString: string,
  options?: Intl.DateTimeFormatOptions
): string => {
  const date = new Date(dateString);
  const defaultOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  };
  return date.toLocaleDateString('en-US', options || defaultOptions);
};

/**
 * Format a date to relative time (e.g., "2 hours ago")
 */
export const formatRelativeTime = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffSecs < 60) return 'just now';
  if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
  if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
  return formatDate(dateString);
};

/**
 * Format a number to a fixed decimal place
 */
export const formatNumber = (
  num: number,
  decimals: number = 2
): string => {
  return num.toFixed(decimals);
};

/**
 * Format a score with optional color coding
 */
export const formatScore = (score: number, outOf: number = 10): string => {
  return `${formatNumber(score, 1)}/${outOf}`;
};

/**
 * Get danger level from danger score
 */
export const getDangerLevel = (
  score: number
): 'low' | 'moderate' | 'high' | 'critical' => {
  if (score < 0.3) return 'low';
  if (score < 0.5) return 'moderate';
  if (score < 0.7) return 'high';
  return 'critical';
};

/**
 * Get color class for danger score
 */
export const getDangerScoreColor = (score: number): string => {
  const level = getDangerLevel(score);
  const colorMap = {
    low: 'text-green-600',
    moderate: 'text-yellow-600',
    high: 'text-orange-600',
    critical: 'text-red-600',
  };
  return colorMap[level];
};

/**
 * Get background color class for danger score badge
 */
export const getDangerScoreBadge = (score: number): string => {
  const level = getDangerLevel(score);
  const badgeMap = {
    low: 'bg-green-100 text-green-800',
    moderate: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    critical: 'bg-red-100 text-red-800',
  };
  return badgeMap[level];
};

/**
 * Get danger level label
 */
export const getDangerLevelLabel = (score: number): string => {
  const level = getDangerLevel(score);
  const labelMap = {
    low: 'Low Risk',
    moderate: 'Moderate Risk',
    high: 'High Risk',
    critical: 'Critical Risk',
  };
  return labelMap[level];
};

/**
 * Format percentage
 */
export const formatPercentage = (value: number): string => {
  return `${(value * 100).toFixed(0)}%`;
};

/**
 * Format angle in degrees
 */
export const formatDegrees = (value: number): string => {
  return `${formatNumber(value, 1)}°`;
};

/**
 * Truncate text with ellipsis
 */
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Get initials from name
 */
export const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map((word) => word[0])
    .join('')
    .toUpperCase()
    .substring(0, 2);
};
