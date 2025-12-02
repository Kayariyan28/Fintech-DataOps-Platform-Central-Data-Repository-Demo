import React, { useEffect, useState } from 'react';
import { getFraudAlerts } from '../api';
import { AlertTriangle, ShieldAlert, CheckCircle } from 'lucide-react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

const FraudDashboard = () => {
    const [alerts, setAlerts] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const res = await getFraudAlerts();
            setAlerts(res.data);
        };
        fetchData();
        const interval = setInterval(fetchData, 3000);
        return () => clearInterval(interval);
    }, []);

    const highRiskCount = alerts.filter(a => a.severity === 'HIGH').length;
    const mediumRiskCount = alerts.filter(a => a.severity === 'MEDIUM').length;

    const data = [
        { name: 'High Risk', value: highRiskCount, color: '#f87171' },
        { name: 'Medium Risk', value: mediumRiskCount, color: '#fbbf24' },
        { name: 'Safe (Simulated)', value: 100 - alerts.length, color: '#4ade80' },
    ];

    return (
        <div className="grid grid-cols-2">
            <div className="card">
                <h2>Fraud Monitor</h2>
                <div style={{ display: 'flex', gap: '2rem', marginBottom: '2rem' }}>
                    <div style={{ textAlign: 'center' }}>
                        <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--error)' }}>{highRiskCount}</div>
                        <div style={{ color: 'var(--text-secondary)' }}>High Risk Alerts</div>
                    </div>
                    <div style={{ textAlign: 'center' }}>
                        <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#fbbf24' }}>{mediumRiskCount}</div>
                        <div style={{ color: 'var(--text-secondary)' }}>Medium Risk Alerts</div>
                    </div>
                </div>

                <div style={{ height: '200px' }}>
                    <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                            <Pie
                                data={data}
                                innerRadius={60}
                                outerRadius={80}
                                paddingAngle={5}
                                dataKey="value"
                            >
                                {data.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.color} />
                                ))}
                            </Pie>
                            <Tooltip
                                contentStyle={{ background: 'var(--bg-secondary)', border: '1px solid var(--border)' }}
                                itemStyle={{ color: 'var(--text-primary)' }}
                            />
                        </PieChart>
                    </ResponsiveContainer>
                </div>
            </div>

            <div className="card">
                <h2>Recent Alerts</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxHeight: '400px', overflowY: 'auto' }}>
                    {alerts.map((alert, i) => (
                        <div key={i} style={{
                            background: 'rgba(255, 255, 255, 0.03)',
                            padding: '1rem',
                            borderRadius: '0.5rem',
                            borderLeft: `4px solid ${alert.severity === 'HIGH' ? 'var(--error)' : '#fbbf24'}`
                        }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 'bold' }}>
                                    <ShieldAlert size={16} color={alert.severity === 'HIGH' ? 'var(--error)' : '#fbbf24'} />
                                    {alert.reason}
                                </div>
                                <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                                    {new Date(alert.timestamp).toLocaleTimeString()}
                                </span>
                            </div>
                            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                                Transaction ID: {alert.transaction_id}
                            </div>
                        </div>
                    ))}
                    {alerts.length === 0 && (
                        <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                            <CheckCircle size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
                            <div>No fraud alerts detected. System secure.</div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default FraudDashboard;
