import React, { useEffect, useState } from 'react';
import { getCreditScores } from '../api';
import { TrendingUp, User } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const ProductView = () => {
    const [scores, setScores] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const res = await getCreditScores();
            setScores(res.data);
        };
        fetchData();
        const interval = setInterval(fetchData, 5000);
        return () => clearInterval(interval);
    }, []);

    // Prepare data for chart (Score Distribution)
    const chartData = [
        { range: '300-500', count: scores.filter(s => s.score >= 300 && s.score < 500).length },
        { range: '500-650', count: scores.filter(s => s.score >= 500 && s.score < 650).length },
        { range: '650-750', count: scores.filter(s => s.score >= 650 && s.score < 750).length },
        { range: '750-850', count: scores.filter(s => s.score >= 750).length },
    ];

    return (
        <div className="grid grid-cols-2">
            <div className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                    <h2>Customer Credit Insights</h2>
                    <div className="status-badge status-success">
                        <TrendingUp size={14} style={{ marginRight: '0.5rem' }} /> Live Updates
                    </div>
                </div>

                <div style={{ height: '250px', marginBottom: '2rem' }}>
                    <h3>Score Distribution</h3>
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                            <XAxis dataKey="range" stroke="var(--text-secondary)" />
                            <YAxis stroke="var(--text-secondary)" />
                            <Tooltip
                                contentStyle={{ background: 'var(--bg-secondary)', border: '1px solid var(--border)' }}
                                cursor={{ fill: 'rgba(255, 255, 255, 0.05)' }}
                            />
                            <Bar dataKey="count" fill="var(--accent)" radius={[4, 4, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                <div className="grid grid-cols-2">
                    {scores.slice(0, 4).map((score, i) => (
                        <div key={i} style={{
                            background: 'rgba(255, 255, 255, 0.03)',
                            padding: '1rem',
                            borderRadius: '0.5rem',
                            border: '1px solid var(--border)'
                        }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                <User size={16} color="var(--accent)" />
                                <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                                    User {score.user_id.substring(0, 8)}
                                </span>
                            </div>
                            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: score.score > 700 ? 'var(--success)' : 'var(--text-primary)' }}>
                                {score.score}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="card">
                <h3>Detailed Score Analysis</h3>
                <div style={{ overflowY: 'auto', maxHeight: '600px' }}>
                    <table>
                        <thead>
                            <tr>
                                <th>User ID</th>
                                <th>Score</th>
                                <th>Factors</th>
                            </tr>
                        </thead>
                        <tbody>
                            {scores.map((row, i) => (
                                <tr key={i}>
                                    <td>{row.user_id.substring(0, 8)}...</td>
                                    <td style={{ fontWeight: 'bold', color: row.score > 700 ? 'var(--success)' : undefined }}>
                                        {row.score}
                                    </td>
                                    <td style={{ fontSize: '0.75rem' }}>
                                        {row.factors && Object.entries(JSON.parse(row.factors)).map(([k, v]) => (
                                            <div key={k} style={{ display: 'flex', justifyContent: 'space-between', gap: '1rem' }}>
                                                <span style={{ color: 'var(--text-secondary)' }}>{k}:</span>
                                                <span>{v}</span>
                                            </div>
                                        ))}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default ProductView;
