/**
 * Reasoning Chain Component
 * Displays the AI's step-by-step reasoning process and final judgment
 */
import React from 'react';
import { Brain, Shield, Target, AlertCircle, TrendingUp, Info, CheckCircle2, Search, XCircle, Sparkles } from 'lucide-react';

const ReasoningChain = ({ reasoning, isAnalyzing }) => {
    if (isAnalyzing) {
        return (
            <div className="card mt-2 border-t-2 border-t-daleel-500 animate-pulse">
                <div className="flex items-center gap-4 mb-8 pb-6 border-b border-slate-700/50">
                    <div className="bg-daleel-500/20 p-3 rounded-xl border border-daleel-500/30">
                        <Sparkles className="w-8 h-8 text-daleel-400 animate-spin-slow" />
                    </div>
                    <div className="space-y-2">
                        <div className="h-3 w-32 bg-slate-700 rounded"></div>
                        <div className="h-6 w-48 bg-slate-700 rounded"></div>
                    </div>
                </div>
                <div className="space-y-6">
                    {[1, 2, 3].map(i => (
                        <div key={i} className="flex gap-4">
                            <div className="w-8 h-8 bg-slate-800 rounded-full"></div>
                            <div className="flex-1 space-y-2">
                                <div className="h-4 bg-slate-800 rounded w-full"></div>
                                <div className="h-4 bg-slate-800 rounded w-3/4"></div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    if (!reasoning || !reasoning.reasoning_chain) return null;

    const getStepIcon = (index) => {
        const icons = [TrendingUp, AlertCircle, Info, Shield, Target];
        const Icon = icons[index] || Brain;
        return <Icon className="w-5 h-5 text-daleel-400" />;
    };

    const getRecommendationStyle = (rec) => {
        switch (rec) {
            case 'RENEW': return { color: 'text-green-400', bg: 'bg-green-500/10', border: 'border-green-500/30', icon: CheckCircle2 };
            case 'TERMINATE': return { color: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/30', icon: XCircle };
            case 'RENEGOTIATE': return { color: 'text-yellow-400', bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', icon: Search };
            default: return { color: 'text-slate-400', bg: 'bg-slate-500/10', border: 'border-slate-500/30', icon: Info };
        }
    };

    const style = getRecommendationStyle(reasoning.recommendation);
    const RecIcon = style.icon;

    return (
        <div className="card mt-2 border-t-2 border-t-daleel-500 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Judgment Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8 pb-6 border-b border-slate-700/50">
                <div className="flex items-center gap-4">
                    <div className="bg-daleel-500/20 p-3 rounded-xl border border-daleel-500/30">
                        <Brain className="w-8 h-8 text-daleel-400" />
                    </div>
                    <div>
                        <span className="text-[10px] font-bold text-daleel-500 uppercase tracking-[0.2em]">Deep Intelligence Report</span>
                        <h3 className="text-2xl font-bold text-white leading-tight">
                            {reasoning.vendor_name || 'AI Reasoning Analysis'}
                        </h3>
                    </div>
                </div>

                <div className={`flex items-center gap-3 px-6 py-4 rounded-xl border ${style.bg} ${style.border}`}>
                    <RecIcon className={`w-6 h-6 ${style.color}`} />
                    <div>
                        <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest leading-none mb-1">AI Judgment</p>
                        <p className={`text-xl font-black ${style.color} leading-none tracking-tight`}>
                            {reasoning.recommendation || 'PENDING EVALUATION'}
                        </p>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Col: Reasoning Chain */}
                <div className="lg:col-span-2">
                    <div className="flex items-center gap-2 mb-6 text-slate-400">
                        <Target className="w-4 h-4" />
                        <h4 className="text-sm font-bold uppercase tracking-widest">Logic Pathway</h4>
                    </div>

                    <div className="space-y-4">
                        {reasoning.reasoning_chain.map((step, idx) => (
                            <div key={idx} className="flex gap-4 group">
                                <div className="flex flex-col items-center">
                                    <div className="flex-shrink-0 w-8 h-8 bg-slate-800 border border-slate-700 rounded-full flex items-center justify-center group-hover:border-daleel-500/50 transition-colors">
                                        {getStepIcon(idx)}
                                    </div>
                                    {idx < reasoning.reasoning_chain.length - 1 && (
                                        <div className="w-0.5 h-full bg-slate-700 mt-2"></div>
                                    )}
                                </div>
                                <div className="flex-1 bg-slate-800/20 rounded-lg p-4 border border-slate-700/30 group-hover:bg-slate-800/40 transition-colors">
                                    <p className="text-slate-300 leading-relaxed text-sm">{step}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Right Col: Metadata & Alternative Views */}
                <div className="space-y-6">
                    <div className="p-5 bg-slate-800/50 rounded-xl border border-slate-700/50">
                        <div className="flex items-center justify-between mb-4">
                            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Confidence Metrics</p>
                            <span className={`px-2 py-0.5 rounded text-[10px] font-black border ${reasoning.confidence_level === 'HIGH' ? 'bg-green-500/20 text-green-400 border-green-500/30' :
                                reasoning.confidence_level === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30' :
                                    'bg-red-500/20 text-red-400 border-red-500/30'
                                }`}>
                                {reasoning.confidence_level}
                            </span>
                        </div>
                        <p className="text-slate-300 text-sm leading-relaxed italic border-l-2 border-slate-600 pl-4 py-1">
                            "{reasoning.justification}"
                        </p>
                    </div>

                    <div className="p-5 bg-daleel-500/5 rounded-xl border border-daleel-500/10">
                        <h4 className="text-[10px] font-bold text-daleel-400 uppercase tracking-widest mb-3">System Note</h4>
                        <p className="text-slate-500 text-[11px] leading-relaxed">
                            This analysis was synthesized across multi-source data vectors using Gemini-2.5-Flash reasoning.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ReasoningChain;
