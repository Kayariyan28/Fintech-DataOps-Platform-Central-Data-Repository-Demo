import React, { useEffect, useState } from 'react';
import { Activity, CheckCircle, AlertTriangle, Play, Square } from 'lucide-react';
import { getMetrics, getPipelineStatus, startPipeline, stopPipeline } from '../api';

const Dashboard = () => {
    const [metrics, setMetrics] = useState(null);
    const [status, setStatus] = useState({ ingestion_running: false, processing_running: false });
    const [loading, setLoading] = useState(true);

    const fetchData = async () => {
        try {
            const [metricsRes, statusRes] = await Promise.all([getMetrics(), getPipelineStatus()]);
            setMetrics(metricsRes.data);
            setStatus(statusRes.data);
        } catch (error) {
            console.error("Error fetching dashboard data", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 2000);
        return () => clearInterval(interval);
    }, []);

    const handleStart = async () => {
        await startPipeline();
        fetchData();
    };

    const handleStop = async () => {
        await stopPipeline();
        fetchData();
    };

    if (loading && !metrics) return <div>Loading Dashboard...</div>;

    return (
        <div className="grid grid-cols-2">
            <div className="card">
                <h2>Pipeline Control</h2>
                <div className="grid grid-cols-2">
                    <div>
                        <h3>Ingestion Status</h3>
                        <div className={`status-badge ${status.ingestion_running ? 'status-success' : 'status-error'}`}>
                            {status.ingestion_running ? 'Running' : 'Stopped'}
                        </div>
                    </div>
                    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                        <button className="btn btn-primary" onClick={handleStart} disabled={status.ingestion_running}>
                            <Play size={16} style={{ marginRight: '0.5rem' }} /> Start Ingestion
                        </button>
                        <button className="btn btn-danger" onClick={handleStop} disabled={!status.ingestion_running}>
                            <Square size={16} style={{ marginRight: '0.5rem' }} /> Stop
                        </button>
                    </div>
                </div>
            </div>

            <div className="card">
                <h2>Data Quality Health</h2>
                {metrics?.checks.map((check, index) => (
                    <div key={index} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            {check.passed ? <CheckCircle color="var(--success)" size={20} /> : <AlertTriangle color="var(--error)" size={20} />}
                            <span>{check.name}</span>
                        </div>
                        <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>{check.details}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Dashboard;
