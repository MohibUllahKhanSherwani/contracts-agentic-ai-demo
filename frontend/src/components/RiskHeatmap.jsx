/**
 * Risk Heatmap Component
 * Visualizes risk distribution across vendors
 */
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const RiskHeatmap = ({ contracts }) => {
    // Count by risk level
    const riskCounts = {
        low: contracts.filter(c => (c.risk_level || '').toLowerCase() === 'low').length,
        medium: contracts.filter(c => (c.risk_level || '').toLowerCase() === 'medium').length,
        high: contracts.filter(c => (c.risk_level || '').toLowerCase() === 'high').length,
    };

    const data = [
        { name: 'Low Risk', value: riskCounts.low, color: '#10b981' },
        { name: 'Medium Risk', value: riskCounts.medium, color: '#f59e0b' },
        { name: 'High Risk', value: riskCounts.high, color: '#ef4444' },
    ].filter(item => item.value > 0);

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            const data = payload[0];
            return (
                <div className="bg-slate-800 border border-slate-700 rounded-lg p-3 shadow-xl">
                    <p className="font-bold text-white">{data.name}</p>
                    <p className="text-slate-300 text-sm">{data.value} contracts</p>
                    <p className="text-slate-300 text-sm">
                        {((data.value / contracts.length) * 100).toFixed(1)}%
                    </p>
                </div>
            );
        }
        return null;
    };

    if (contracts.length === 0) {
        return (
            <div className="card">
                <h3 className="text-xl font-bold mb-4 text-white">Risk Distribution</h3>
                <p className="text-slate-400 text-center py-12">No data available</p>
            </div>
        );
    }

    return (
        <div className="card">
            <h3 className="text-xl font-bold mb-6 text-white">Risk Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                    <Pie
                        data={data}
                        dataKey="value"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        outerRadius={100}
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    >
                        {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ color: '#94a3b8' }} />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
};

export default RiskHeatmap;
