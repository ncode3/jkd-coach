/**
 * SAMMO Fight IQ - Validation Utilities
 * Helper functions for form validation
 */

import { RoundData } from '@/lib/api';

/**
 * Validation result interface
 */
export interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
}

/**
 * Validate email format
 */
export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate password strength
 */
export const validatePassword = (password: string): ValidationResult => {
  const errors: Record<string, string> = {};

  if (password.length < 8) {
    errors.length = 'Password must be at least 8 characters long';
  }

  if (!/[A-Z]/.test(password)) {
    errors.uppercase = 'Password must contain at least one uppercase letter';
  }

  if (!/[a-z]/.test(password)) {
    errors.lowercase = 'Password must contain at least one lowercase letter';
  }

  if (!/[0-9]/.test(password)) {
    errors.number = 'Password must contain at least one number';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
};

/**
 * Validate username
 */
export const validateUsername = (username: string): ValidationResult => {
  const errors: Record<string, string> = {};

  if (username.length < 3) {
    errors.length = 'Username must be at least 3 characters long';
  }

  if (username.length > 20) {
    errors.maxLength = 'Username must not exceed 20 characters';
  }

  if (!/^[a-zA-Z0-9_]+$/.test(username)) {
    errors.format = 'Username can only contain letters, numbers, and underscores';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
};

/**
 * Validate round data
 */
export const validateRoundData = (data: Partial<RoundData>): ValidationResult => {
  const errors: Record<string, string> = {};

  // Required fields
  if (data.pressure_score === undefined) {
    errors.pressure_score = 'Pressure score is required';
  } else if (data.pressure_score < 0 || data.pressure_score > 10) {
    errors.pressure_score = 'Pressure score must be between 0 and 10';
  }

  if (data.ring_control_score === undefined) {
    errors.ring_control_score = 'Ring control score is required';
  } else if (data.ring_control_score < 0 || data.ring_control_score > 10) {
    errors.ring_control_score = 'Ring control score must be between 0 and 10';
  }

  if (data.defense_score === undefined) {
    errors.defense_score = 'Defense score is required';
  } else if (data.defense_score < 0 || data.defense_score > 10) {
    errors.defense_score = 'Defense score must be between 0 and 10';
  }

  if (data.clean_shots_taken === undefined) {
    errors.clean_shots_taken = 'Clean shots taken is required';
  } else if (data.clean_shots_taken < 0) {
    errors.clean_shots_taken = 'Clean shots taken must be non-negative';
  }

  // Optional fields validation
  if (
    data.guard_down_ratio !== undefined &&
    (data.guard_down_ratio < 0 || data.guard_down_ratio > 1)
  ) {
    errors.guard_down_ratio = 'Guard down ratio must be between 0 and 1';
  }

  if (
    data.avg_hip_rotation !== undefined &&
    (data.avg_hip_rotation < 0 || data.avg_hip_rotation > 180)
  ) {
    errors.avg_hip_rotation = 'Hip rotation must be between 0 and 180 degrees';
  }

  if (
    data.avg_stance_width !== undefined &&
    (data.avg_stance_width < 0 || data.avg_stance_width > 1)
  ) {
    errors.avg_stance_width = 'Stance width must be between 0 and 1';
  }

  if (data.notes && data.notes.length > 500) {
    errors.notes = 'Notes must not exceed 500 characters';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
};

/**
 * Validate score (0-10)
 */
export const validateScore = (score: number): boolean => {
  return score >= 0 && score <= 10;
};

/**
 * Validate ratio (0-1)
 */
export const validateRatio = (ratio: number): boolean => {
  return ratio >= 0 && ratio <= 1;
};

/**
 * Validate angle (0-180)
 */
export const validateAngle = (angle: number): boolean => {
  return angle >= 0 && angle <= 180;
};

/**
 * Sanitize input string
 */
export const sanitizeInput = (input: string): string => {
  return input.trim().replace(/[<>]/g, '');
};

/**
 * Check if value is within range
 */
export const isInRange = (
  value: number,
  min: number,
  max: number
): boolean => {
  return value >= min && value <= max;
};
