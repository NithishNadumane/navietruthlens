/**
 * TruthLens API Client
 * Handles communication with the Python Flask backend.
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export type InputMode = 'headline' | 'article';

export interface DbVerification {
  verified: boolean;
  match_score: number;       // 0-100
  best_match: string | null;
  status: 'VERIFIED' | 'PARTIAL' | 'UNVERIFIED' | 'NO_DB' | 'ERROR';
  db_count: number;
  similar_count: number;     // # of headlines loosely related (score >= 0.15)
}

export interface PredictionResult {
  prediction: 'REAL' | 'FAKE' | 'SUSPICIOUS';
  confidence: number;
  probability_fake: number;
  probability_real: number;
  preprocessing_steps: PreprocessingSteps;
  model_used: string;
  input_mode: InputMode;
  detected_language: string;
  translated_text: string | null;
  note?: string;
  db_verification?: DbVerification;
}

export interface PreprocessingSteps {
  original: string;
  after_cleaning: string;
  tokens: string[];
  after_stopword_removal: string[];
  after_lemmatization: string[];
  final_text: string;
  original_word_count: number;
  final_word_count: number;
  words_removed: number;
}

export interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  confusion_matrix: {
    true_positive: number;
    true_negative: number;
    false_positive: number;
    false_negative: number;
  };
  training_samples: number;
  test_samples: number;
  model_architecture: {
    type: string;
    embedding_dim?: number;
    hidden_dim?: number;
    num_layers?: number;
    dropout?: number;
    max_sequence_length?: number;
  };
  dataset: string;
  mode: string;
}

export interface TrainingHistory {
  epochs: number[];
  train_loss: number[];
  val_loss: number[];
  train_accuracy: number[];
  val_accuracy: number[];
  mode?: string;
}

export interface HealthStatus {
  status: string;
  model_loaded: boolean;
  model_type: string;
  translation_enabled: boolean;
  news_db_count: number;
}

/**
 * Send news text for fake/real classification.
 */
export async function predictNews(
  text: string,
  inputMode: InputMode = 'article'
): Promise<PredictionResult> {
  const response = await fetch(`${API_URL}/api/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, input_mode: inputMode }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Prediction failed');
  }

  return response.json();
}



/**
 * Fetch model evaluation metrics.
 */
export async function getModelMetrics(): Promise<ModelMetrics> {
  const response = await fetch(`${API_URL}/api/metrics`);
  if (!response.ok) throw new Error('Failed to fetch metrics');
  return response.json();
}

/**
 * Fetch training history for loss/accuracy curves.
 */
export async function getTrainingHistory(): Promise<TrainingHistory> {
  const response = await fetch(`${API_URL}/api/training-history`);
  if (!response.ok) throw new Error('Failed to fetch training history');
  return response.json();
}

/**
 * Check backend health status.
 */
export async function checkHealth(): Promise<HealthStatus> {
  const response = await fetch(`${API_URL}/api/health`);
  if (!response.ok) throw new Error('Backend unavailable');
  return response.json();
}
