/**
 * API Service
 * Handles all backend API calls for contract evaluations
 */

const API_BASE_URL = '/api';

/**
 * Fetch all evaluation results from backend
 * Endpoint: GET /results
 */
export const fetchEvaluations = async () => {
    const response = await fetch(`${API_BASE_URL}/results`);
    if (!response.ok) {
        throw new Error('Failed to fetch evaluations');
    }
    const data = await response.json();
    return data.results || [];
};

/**
 * Evaluate a specific sample contract by name
 * Endpoint: POST /evaluate-sample/{name}
 */
export const evaluateSample = async (sampleName) => {
    const response = await fetch(`${API_BASE_URL}/evaluate-sample/${sampleName}`, {
        method: 'POST'
    });
    if (!response.ok) {
        throw new Error(`Failed to evaluate vendor: ${sampleName}`);
    }
    return await response.json();
};

/**
 * Fetch specific evaluation by contract ID
 * Endpoint: GET /results/{contract_id}
 */
export const fetchEvaluationById = async (contractId) => {
    const response = await fetch(`${API_BASE_URL}/results/${contractId}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch evaluation for ${contractId}`);
    }
    return await response.json();
};

/**
 * Fetch audit log entries
 * Endpoint: GET /audit-log
 */
export const fetchAuditLog = async (limit = 50) => {
    const response = await fetch(`${API_BASE_URL}/audit-log?limit=${limit}`);
    if (!response.ok) {
        throw new Error('Failed to fetch audit log');
    }
    const data = await response.json();
    return data.entries || [];
};

/**
 * Check API health
 * Endpoint: GET /health
 */
export const checkHealth = async () => {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
        throw new Error('API health check failed');
    }
    return await response.json();
};
