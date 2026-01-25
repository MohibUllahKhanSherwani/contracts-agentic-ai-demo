/**
 * Statistics Cards Component
 * Displays key metrics and summary statistics
 */
import { Activity, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

const StatsCard = ({ contracts }) => {
    const total = contracts.length;
    const lowRisk = contracts.filter(c => (c.risk_level || '').toLowerCase() === 'low').length;
    const mediumRisk = contracts.filter(c => (c.risk_level || '').toLowerCase() === 'medium').length;
    const highRisk = contracts.filter(c => (c.risk_level || '').toLowerCase() === 'high').length;

    const avgScore = total > 0
        ? (contracts.reduce((sum, c) => sum + parseFloat(c.performance_score || 0), 0) / total).toFixed(1)
        : 0;

    const stats = [
        {
            label: 'Total Contracts',
            value: total,
            icon: Activity,
            color: 'text-daleel-400',
            bgColor: 'bg-daleel-500/10'
        },
        {
            label: 'Low Risk',
            value: lowRisk,
            icon: CheckCircle,
            color: 'text-green-400',
            bgColor: 'bg-green-500/10'
        },
        {
            label: 'Medium Risk',
            value: mediumRisk,
            icon: AlertTriangle,
            color: 'text-yellow-400',
            bgColor: 'bg-yellow-500/10'
        },
        {
            label: 'High Risk',
            value: highRisk,
            icon: XCircle,
            color: 'text-red-400',
            bgColor: 'bg-red-500/10'
        }
    ];

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
            {stats.map((stat, idx) => {
                const Icon = stat.icon;
                return (
                    <div key={idx} className="card">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-slate-400 text-sm mb-1">{stat.label}</p>
                                <p className={`text-3xl font-bold ${stat.color}`}>{stat.value}</p>
                            </div>
                            <div className={`${stat.bgColor} p-3 rounded-lg`}>
                                <Icon className={`w-6 h-6 ${stat.color}`} />
                            </div>
                        </div>
                    </div>
                );
            })}

            <div className="card">
                <div className="flex items-center justify-between">
                    <div>
                        <p className="text-slate-400 text-sm mb-1">Avg Score</p>
                        <p className="text-3xl font-bold text-white">{avgScore}</p>
                    </div>
                    <div className="bg-purple-500/10 p-3 rounded-lg">
                        <Activity className="w-6 h-6 text-purple-400" />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default StatsCard;
