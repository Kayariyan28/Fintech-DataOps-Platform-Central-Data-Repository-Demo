import React, { useEffect, useState } from 'react';
import { getConsumerData, getTransactionData } from '../api';

const DataRepository = () => {
    const [consumerData, setConsumerData] = useState([]);
    const [transactionData, setTransactionData] = useState([]);
    const [activeTab, setActiveTab] = useState('consumer');

    useEffect(() => {
        const fetchData = async () => {
            if (activeTab === 'consumer') {
                const res = await getConsumerData();
                setConsumerData(res.data);
            } else {
                const res = await getTransactionData();
                setTransactionData(res.data);
            }
        };
        fetchData();
        const interval = setInterval(fetchData, 5000);
        return () => clearInterval(interval);
    }, [activeTab]);

    return (
        <div className="card">
            <div className="nav-tabs">
                <button
                    className={`nav-tab ${activeTab === 'consumer' ? 'active' : ''}`}
                    onClick={() => setActiveTab('consumer')}
                >
                    Consumer Behavior
                </button>
                <button
                    className={`nav-tab ${activeTab === 'transactions' ? 'active' : ''}`}
                    onClick={() => setActiveTab('transactions')}
                >
                    Transactions
                </button>
            </div>

            <div style={{ overflowX: 'auto' }}>
                <table>
                    <thead>
                        {activeTab === 'consumer' ? (
                            <tr>
                                <th>User ID</th>
                                <th>Event</th>
                                <th>Amount</th>
                                <th>Timestamp</th>
                                <th>Details</th>
                            </tr>
                        ) : (
                            <tr>
                                <th>Transaction ID</th>
                                <th>Category</th>
                                <th>Amount</th>
                                <th>Timestamp</th>
                                <th>Buyer ID</th>
                            </tr>
                        )}
                    </thead>
                    <tbody>
                        {activeTab === 'consumer' ? (
                            consumerData.map((row, i) => (
                                <tr key={i}>
                                    <td>{row.user_id.substring(0, 8)}...</td>
                                    <td>{row.event_type}</td>
                                    <td>${row.amount}</td>
                                    <td>{new Date(row.timestamp).toLocaleString()}</td>
                                    <td>{JSON.stringify(row.details)}</td>
                                </tr>
                            ))
                        ) : (
                            transactionData.map((row, i) => (
                                <tr key={i}>
                                    <td>{row.transaction_id.substring(0, 8)}...</td>
                                    <td>{row.item_category}</td>
                                    <td>${row.amount}</td>
                                    <td>{new Date(row.timestamp).toLocaleString()}</td>
                                    <td>{row.buyer_id.substring(0, 8)}...</td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default DataRepository;
