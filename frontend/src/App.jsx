import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import DataRepository from './components/DataRepository';
import ProductView from './components/ProductView';
import FraudDashboard from './components/FraudDashboard';
import { LayoutDashboard, Database, CreditCard, ShieldAlert } from 'lucide-react';

function App() {
    const [view, setView] = useState('dashboard');

    return (
        <div className="container">
            <header style={{ marginBottom: '2rem', borderBottom: '1px solid var(--border)', paddingBottom: '1rem' }}>
                <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--accent)' }}>
                    Fintech DataOps Platform
                </h1>
                <p style={{ color: 'var(--text-secondary)' }}>
                    Central Data Repository & Intelligence Engine
                </p>
            </header>

            <div className="nav-tabs">
                <button
                    className={`nav-tab ${view === 'dashboard' ? 'active' : ''}`}
                    onClick={() => setView('dashboard')}
                >
                    <LayoutDashboard size={18} style={{ display: 'inline', marginRight: '0.5rem', verticalAlign: 'text-bottom' }} />
                    DataOps Dashboard
                </button>
                <button
                    className={`nav-tab ${view === 'repository' ? 'active' : ''}`}
                    onClick={() => setView('repository')}
                >
                    <Database size={18} style={{ display: 'inline', marginRight: '0.5rem', verticalAlign: 'text-bottom' }} />
                    Data Repository
                </button>
                <button
                    className={`nav-tab ${view === 'product' ? 'active' : ''}`}
                    onClick={() => setView('product')}
                >
                    <CreditCard size={18} style={{ display: 'inline', marginRight: '0.5rem', verticalAlign: 'text-bottom' }} />
                    Product View
                </button>
                <button
                    className={`nav-tab ${view === 'fraud' ? 'active' : ''}`}
                    onClick={() => setView('fraud')}
                >
                    <ShieldAlert size={18} style={{ display: 'inline', marginRight: '0.5rem', verticalAlign: 'text-bottom' }} />
                    Fraud Monitor
                </button>
            </div>

            <main>
                {view === 'dashboard' && <Dashboard />}
                {view === 'repository' && <DataRepository />}
                {view === 'product' && <ProductView />}
                {view === 'fraud' && <FraudDashboard />}
            </main>
        </div>
    );
}

export default App;
