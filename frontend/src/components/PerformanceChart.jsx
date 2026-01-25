/**
 * Performance Chart Component
 * Visualizes vendor performance scores using bar chart
 */
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

const PerformanceChart = ({ contracts }) => {
    // Prepare data for chart
    const chartData = contracts.map(contract => ({
        name: contract.vendor_name || 'Unknown',
        score: parseFloat(contract.performance_score || 0),
        grade: contract.grade || 'F',
        risk: (contract.risk_level || 'unknown').toLowerCase()
    }));

    // Color based on risk level
    const getBarColor = (risk) => {
        if (risk === 'low') return '#10b981'; // green
        if (risk === 'medium') return '#f59e0b'; // yellow
        if (risk === 'high') return '#ef4444'; // red
        return '#64748b'; // gray
    };

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            const data = payload[0].payload;
            return (
                <div className="bg-slate-800 border border-slate-700 rounded-lg p-3 shadow-xl">
                    <p className="font-bold text-white">{data.name}</p>
                    <p className="text-slate-300 text-sm">Score: {data.score}/100</p>
                    <p className="text-slate-300 text-sm">Grade: {data.grade}</p>
                    <p className="text-slate-300 text-sm">Risk: {data.risk.toUpperCase()}</p>
                </div>
            );
        }
        return null;
    };

    if (contracts.length === 0) {
        return (
            <div className="card">
                <h3 className="text-xl font-bold mb-4 text-white">Performance Overview</h3>
                <p className="text-slate-400 text-center py-12">No data available</p>
            </div>
        );
    }

    return (
        <div className="card">
            <h3 className="text-xl font-bold mb-6 text-white">Performance Overview</h3>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis
                        dataKey="name"
                        stroke="#94a3b8"
                        tick={{ fill: '#94a3b8' }}
                        angle={-45}
                        textAnchor="end"
                        height={100}
                    />
                    <YAxis
                        stroke="#94a3b8"
                        tick={{ fill: '#94a3b8' }}
                        domain={[0, 100]}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ color: '#94a3b8' }} />
                    <Bar dataKey="score" name="Performance Score" radius={[8, 8, 0, 0]}>
                        {chartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={getBarColor(entry.risk)} />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default PerformanceChart;
