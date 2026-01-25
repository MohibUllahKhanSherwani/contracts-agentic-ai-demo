/**
 * Main App Component
 * Dashboard for Contract Evaluation System
 * 
 * THIS IS WHERE API CALLS HAPPEN:
 * - fetchEvaluations() is called on component mount
 * - Auto-refresh every 30 seconds
 * - Manual refresh button available
 */
import { useState, useEffect } from 'react';
import { RefreshCw, AlertCircle } from 'lucide-react';
import ContractTable from './components/ContractTable';
import StatsCard from './components/StatsCard';
import PerformanceChart from './components/PerformanceChart';
import RiskHeatmap from './components/RiskHeatmap';
import ReasoningChain from './components/ReasoningChain';
import { fetchEvaluations } from './services/api';

function App() {
    const [contracts, setContracts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [lastUpdate, setLastUpdate] = useState(null);
    const [selectedContract, setSelectedContract] = useState(null);

    /**
     * MAIN API CALL FUNCTION
     * Fetches contract evaluations from backend
     */
    const loadContracts = async () => {
        try {
            setLoading(true);
            setError(null);

            // **API CALL HERE** - Fetches from GET /results endpoint
            const data = await fetchEvaluations();

            setContracts(data);
            setLastUpdate(new Date());
        } catch (err) {
            setError(err.message);
            console.error('Error loading contracts:', err);
        } finally {
            setLoading(false);
        }
    };

    // Load contracts on mount
    useEffect(() => {
        loadContracts();
    }, []);

    // Auto-refresh every 30 seconds
    useEffect(() => {
        const interval = setInterval(() => {
            loadContracts();
        }, 30000); // 30 seconds

        return () => clearInterval(interval);
    }, []);

    const handleSelectContract = (contract) => {
        // Find full contract data if needed, but for now we have reasoning data in the object
        setSelectedContract(contract);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
            {/* Header */}
            <header className="bg-slate-900/50 backdrop-blur-sm border-b border-slate-800 sticky top-0 z-10">
                <div className="container mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold text-white">Daleel Petroleum</h1>
                            <p className="text-slate-400 text-sm">Contract Evaluation Dashboard</p>
                        </div>
                        <button
                            onClick={loadContracts}
                            disabled={loading}
                            className="btn-primary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                            Refresh
                        </button>
                    </div>
                    {lastUpdate && (
                        <p className="text-slate-500 text-xs mt-2">
                            Last updated: {lastUpdate.toLocaleTimeString()}
                        </p>
                    )}
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-6 py-8">
                {/* Error State */}
                {error && (
                    <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-6 flex items-start gap-3">
                        <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                        <div>
                            <h3 className="text-red-400 font-semibold">Error Loading Data</h3>
                            <p className="text-red-300 text-sm mt-1">{error}</p>
                            <p className="text-red-300 text-sm mt-2">
                                Make sure the backend API is running on port 8000.
                            </p>
                        </div>
                    </div>
                )}

                {/* Loading State */}
                {loading && contracts.length === 0 && (
                    <div className="text-center py-20">
                        <RefreshCw className="w-12 h-12 text-daleel-500 animate-spin mx-auto mb-4" />
                        <p className="text-slate-400">Loading contract evaluations...</p>
                    </div>
                )}

                {/* Dashboard Content */}
                {!loading || contracts.length > 0 ? (
                    <>
                        {/* Stats Cards */}
                        <StatsCard contracts={contracts} />

                        {/* Charts Row */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                            <PerformanceChart contracts={contracts} />
                            <RiskHeatmap contracts={contracts} />
                        </div>

                        {/* Contracts Table */}
                        <ContractTable
                            contracts={contracts}
                            onSelectContract={handleSelectContract}
                        />

                        {/* Reasoning Chain Detail */}
                        {selectedContract && (
                            <ReasoningChain
                                reasoning={{
                                    reasoning_chain: selectedContract.reasoning_chain,
                                    confidence_level: selectedContract.confidence_level,
                                    justification: selectedContract.justification,
                                    alternative_consideration: selectedContract.alternative_consideration
                                }}
                            />
                        )}
                    </>
                ) : null}
            </main>

            {/* Footer */}
            <footer className="bg-slate-900/50 border-t border-slate-800 mt-12">
                <div className="container mx-auto px-6 py-4">
                    <p className="text-slate-500 text-sm text-center">
                        Agentic AI Contract Evaluation System • Daleel Petroleum • {new Date().getFullYear()}
                    </p>
                </div>
            </footer>
        </div>
    );
}

export default App;
