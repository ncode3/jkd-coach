/**
 * SAMMO Fight IQ - Round Logger Component
 * Form component to log round data with all boxing metrics
 */

import React, { useState } from 'react';
import { RoundData, LogRoundResponse } from '@/lib/api';
import { useRounds } from '@/hooks/useRounds';
import { useAuth } from '@/hooks/useAuth';

interface RoundLoggerProps {
  onSuccess?: (response: LogRoundResponse) => void;
  onError?: (error: Error) => void;
}

/**
 * RoundLogger Component
 * Form for logging sparring round data with validation
 */
export const RoundLogger: React.FC<RoundLoggerProps> = ({
  onSuccess,
  onError,
}) => {
  const { token } = useAuth();
  const { logRound, isSubmitting } = useRounds(token, false);

  // Form state
  const [formData, setFormData] = useState<RoundData>({
    pressure_score: 5,
    ring_control_score: 5,
    defense_score: 5,
    clean_shots_taken: 0,
    guard_down_ratio: 0,
    avg_hip_rotation: 0,
    avg_stance_width: 0,
    notes: '',
  });

  const [showAdvanced, setShowAdvanced] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState<string | null>(null);

  /**
   * Handle input change
   */
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;
    const numericValue = type === 'number' ? parseFloat(value) : value;

    setFormData((prev) => ({
      ...prev,
      [name]: numericValue,
    }));
  };

  /**
   * Handle form submission
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError(null);
    setSubmitSuccess(null);

    // Validation
    if (
      formData.pressure_score < 0 ||
      formData.pressure_score > 10 ||
      formData.ring_control_score < 0 ||
      formData.ring_control_score > 10 ||
      formData.defense_score < 0 ||
      formData.defense_score > 10
    ) {
      setSubmitError('Scores must be between 0 and 10');
      return;
    }

    if (formData.clean_shots_taken < 0) {
      setSubmitError('Clean shots taken must be non-negative');
      return;
    }

    try {
      const response = await logRound(formData);
      setSubmitSuccess(
        `Round logged successfully! Danger Score: ${response.danger_score.toFixed(2)}`
      );

      // Reset form
      setFormData({
        pressure_score: 5,
        ring_control_score: 5,
        defense_score: 5,
        clean_shots_taken: 0,
        guard_down_ratio: 0,
        avg_hip_rotation: 0,
        avg_stance_width: 0,
        notes: '',
      });

      if (onSuccess) {
        onSuccess(response);
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to log round';
      setSubmitError(errorMessage);

      if (onError && error instanceof Error) {
        onError(error);
      }
    }
  };

  /**
   * Reset form
   */
  const handleReset = () => {
    setFormData({
      pressure_score: 5,
      ring_control_score: 5,
      defense_score: 5,
      clean_shots_taken: 0,
      guard_down_ratio: 0,
      avg_hip_rotation: 0,
      avg_stance_width: 0,
      notes: '',
    });
    setSubmitError(null);
    setSubmitSuccess(null);
  };

  return (
    <div className="round-logger">
      <div className="round-logger-header">
        <h2 className="text-2xl font-bold mb-4">Log Sparring Round</h2>
        <p className="text-gray-600 mb-6">
          Record your sparring session metrics to track progress and get coaching feedback.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Core Metrics */}
        <div className="core-metrics space-y-4">
          <h3 className="text-lg font-semibold">Core Metrics (Required)</h3>

          {/* Pressure Score */}
          <div className="form-group">
            <label htmlFor="pressure_score" className="block text-sm font-medium mb-2">
              Pressure Score (0-10)
              <span className="text-gray-500 ml-2">How much pressure did you apply?</span>
            </label>
            <input
              type="number"
              id="pressure_score"
              name="pressure_score"
              min="0"
              max="10"
              step="0.1"
              value={formData.pressure_score}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Ring Control Score */}
          <div className="form-group">
            <label htmlFor="ring_control_score" className="block text-sm font-medium mb-2">
              Ring Control Score (0-10)
              <span className="text-gray-500 ml-2">How well did you control the ring?</span>
            </label>
            <input
              type="number"
              id="ring_control_score"
              name="ring_control_score"
              min="0"
              max="10"
              step="0.1"
              value={formData.ring_control_score}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Defense Score */}
          <div className="form-group">
            <label htmlFor="defense_score" className="block text-sm font-medium mb-2">
              Defense Score (0-10)
              <span className="text-gray-500 ml-2">How good was your defense?</span>
            </label>
            <input
              type="number"
              id="defense_score"
              name="defense_score"
              min="0"
              max="10"
              step="0.1"
              value={formData.defense_score}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Clean Shots Taken */}
          <div className="form-group">
            <label htmlFor="clean_shots_taken" className="block text-sm font-medium mb-2">
              Clean Shots Taken
              <span className="text-gray-500 ml-2">Number of clean shots you took</span>
            </label>
            <input
              type="number"
              id="clean_shots_taken"
              name="clean_shots_taken"
              min="0"
              step="1"
              value={formData.clean_shots_taken}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {/* Advanced Metrics Toggle */}
        <div className="advanced-toggle">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            {showAdvanced ? '− Hide' : '+ Show'} Advanced Metrics (Optional)
          </button>
        </div>

        {/* Advanced Metrics */}
        {showAdvanced && (
          <div className="advanced-metrics space-y-4">
            <h3 className="text-lg font-semibold">Advanced Metrics (Optional)</h3>

            {/* Guard Down Ratio */}
            <div className="form-group">
              <label htmlFor="guard_down_ratio" className="block text-sm font-medium mb-2">
                Guard Down Ratio (0-1)
                <span className="text-gray-500 ml-2">Percentage of time guard was down</span>
              </label>
              <input
                type="number"
                id="guard_down_ratio"
                name="guard_down_ratio"
                min="0"
                max="1"
                step="0.01"
                value={formData.guard_down_ratio}
                onChange={handleChange}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Average Hip Rotation */}
            <div className="form-group">
              <label htmlFor="avg_hip_rotation" className="block text-sm font-medium mb-2">
                Average Hip Rotation (degrees)
                <span className="text-gray-500 ml-2">Power generation metric</span>
              </label>
              <input
                type="number"
                id="avg_hip_rotation"
                name="avg_hip_rotation"
                min="0"
                max="180"
                step="0.1"
                value={formData.avg_hip_rotation}
                onChange={handleChange}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Average Stance Width */}
            <div className="form-group">
              <label htmlFor="avg_stance_width" className="block text-sm font-medium mb-2">
                Average Stance Width (normalized)
                <span className="text-gray-500 ml-2">Balance and mobility metric</span>
              </label>
              <input
                type="number"
                id="avg_stance_width"
                name="avg_stance_width"
                min="0"
                max="1"
                step="0.01"
                value={formData.avg_stance_width}
                onChange={handleChange}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        )}

        {/* Notes */}
        <div className="form-group">
          <label htmlFor="notes" className="block text-sm font-medium mb-2">
            Notes (Optional)
            <span className="text-gray-500 ml-2">Additional observations</span>
          </label>
          <textarea
            id="notes"
            name="notes"
            rows={3}
            value={formData.notes}
            onChange={handleChange}
            placeholder="Any additional notes about this round..."
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Error Message */}
        {submitError && (
          <div className="error-message bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {submitError}
          </div>
        )}

        {/* Success Message */}
        {submitSuccess && (
          <div className="success-message bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
            {submitSuccess}
          </div>
        )}

        {/* Form Actions */}
        <div className="form-actions flex gap-4">
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex-1 bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Logging Round...' : 'Log Round'}
          </button>
          <button
            type="button"
            onClick={handleReset}
            disabled={isSubmitting}
            className="px-6 py-3 border border-gray-300 rounded-lg font-medium hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Reset
          </button>
        </div>
      </form>
    </div>
  );
};

export default RoundLogger;
