import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_URL,
});

export const startPipeline = () => api.post('/pipeline/start');
export const stopPipeline = () => api.post('/pipeline/stop');
export const getPipelineStatus = () => api.get('/pipeline/status');
export const getMetrics = () => api.get('/dataops/metrics');
export const getConsumerData = () => api.get('/data/consumer');
export const getTransactionData = () => api.get('/data/transactions');
export const getCreditScores = () => api.get('/data/scores');
export const getFraudAlerts = () => api.get('/data/fraud-alerts');
