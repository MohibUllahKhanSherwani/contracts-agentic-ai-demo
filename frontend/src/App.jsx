import { useState, useEffect } from 'react';
import { RefreshCw, AlertCircle, Zap, Brain, TrendingUp, ShieldCheck } from 'lucide-react';
import ContractTable from './components/ContractTable';
import StatsCard from './components/StatsCard';
import PerformanceChart from './components/PerformanceChart';
import RiskHeatmap from './components/RiskHeatmap';
import ReasoningChain from './components/ReasoningChain';
import { fetchEvaluations, evaluateSample } from './services/api';

function App() {
    const [contracts, setContracts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [analyzingId, setAnalyzingId] = useState(null);
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

    /**
     * TRIGGER REASONING ON SELECTION
     */
    const handleSelectContract = async (contract) => {
        // Set basic selection immediately
        setSelectedContract(contract);

        const nameMap = {
            "ABC IT Solutions": "vendor_abc_it_solutions",
            "XYZ Tech Services": "vendor_xyz_tech",
            "Problematic IT Corp": "vendor_problematic_corp"
        };

        const sampleName = nameMap[contract.vendor_name];
        if (!sampleName) return;

        try {
            setAnalyzingId(contract.contract_id);
            setError(null);
            const updatedData = await evaluateSample(sampleName);
            setContracts(prev => prev.map(c =>
                c.contract_id === contract.contract_id ? updatedData : c
            ));
            setSelectedContract(updatedData);
            setLastUpdate(new Date());
        } catch (err) {
            setError(`Analysis for ${contract.vendor_name} failed: ${err.message}`);
        } finally {
            setAnalyzingId(null);
        }
    };

    // Load contracts on mount
    useEffect(() => {
        loadContracts();
    }, []);

    // Auto-refresh every 60 seconds (only if not analyzing)
    useEffect(() => {
        const interval = setInterval(() => {
            if (!analyzingId) loadContracts();
        }, 60000);

        return () => clearInterval(interval);
    }, [analyzingId]);

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 pb-20">
            {/* Header */}
            <header className="bg-slate-900/50 backdrop-blur-md border-b border-slate-800 sticky top-0 z-20">
                <div className="container mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-daleel-500 p-1.5 rounded-lg">
                                <ShieldCheck className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-white tracking-tight">Daleel Petroleum</h1>
                                <p className="text-slate-400 text-xs font-medium uppercase tracking-wider">Contract Intelligence Hub</p>
                            </div>
                        </div>

                        <div className="flex items-center gap-3">
                            <button
                                onClick={loadContracts}
                                disabled={loading || analyzingId}
                                className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-all disabled:opacity-30"
                                title="Refresh data"
                            >
                                <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
                            </button>

                            <div className="px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-slate-400 text-xs font-mono">
                                {analyzingId ? (
                                    <span className="flex items-center gap-2">
                                        <Brain className="w-3 h-3 text-daleel-400 animate-pulse" />
                                        Reasoning Over {analyzingId}...
                                    </span>
                                ) : (
                                    <span className="flex items-center gap-2">
                                        <Zap className="w-3 h-3 text-yellow-400" />
                                        Select vendor to trigger AI
                                    </span>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-6 py-8">
                {/* Error State */}
                {error && (
                    <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-6 flex items-start gap-3">
                        <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                        <div>
                            <h3 className="text-red-400 font-semibold">System Alert</h3>
                            <p className="text-red-300 text-sm mt-1">{error}</p>
                        </div>
                    </div>
                )}

                {/* Dashboard Grid */}
                {!loading || contracts.length > 0 ? (
                    <div className="space-y-6">
                        {/* Stats Cards */}
                        <StatsCard contracts={contracts} />

                        {/* Charts Row */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            <PerformanceChart contracts={contracts} />
                            <RiskHeatmap contracts={contracts} />
                        </div>

                        {/* Contracts Table */}
                        <ContractTable
                            contracts={contracts}
                            onSelectContract={handleSelectContract}
                            selectedContractId={selectedContract?.contract_id}
                        />

                        {/* Reasoning Detail View */}
                        <div className="pt-4 scroll-mt-24" id="reasoning-report">
                            {selectedContract ? (
                                <ReasoningChain
                                    reasoning={{
                                        vendor_name: selectedContract.vendor_name,
                                        reasoning_chain: selectedContract.reasoning_chain,
                                        confidence_level: selectedContract.confidence_level,
                                        justification: selectedContract.justification,
                                        recommendation: selectedContract.recommendation
                                    }}
                                    isAnalyzing={analyzingId === selectedContract.contract_id}
                                />
                            ) : (
                                <div className="card text-center py-12 border-dashed border-slate-700">
                                    <TrendingUp className="w-10 h-10 text-slate-600 mx-auto mb-4" />
                                    <h3 className="text-lg font-semibold text-slate-400">Select a vendor for on-demand deep reasoning</h3>
                                    <p className="text-slate-500 text-sm">LLM analysis triggers automatically upon selection</p>
                                </div>
                            )}
                        </div>
                    </div>
                ) : (
                    loading && (
                        <div className="text-center py-40">
                            <div className="relative inline-block">
                                <div className="w-16 h-16 border-4 border-daleel-500/20 border-t-daleel-500 rounded-full animate-spin"></div>
                                <ShieldCheck className="w-6 h-6 text-daleel-400 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
                            </div>
                            <p className="text-slate-400 mt-6 font-medium">Initializing Intelligence Hub...</p>
                        </div>
                    )
                )}
            </main>
        </div>
    );
}

export default App;
