/**
 * Reasoning Chain Component
 * Displays the AI's step-by-step reasoning process
 */
import React from 'react';
import { Brain, Shield, Target, AlertCircle, TrendingUp, Info } from 'lucide-react';

const ReasoningChain = ({ reasoning }) => {
    if (!reasoning || !reasoning.reasoning_chain) return null;

    const getStepIcon = (index) => {
        const icons = [TrendingUp, AlertCircle, Info, Shield, Target];
        const Icon = icons[index] || Brain;
        return <Icon className="w-5 h-5 text-daleel-400" />;
    };

    return (
        <div className="card mt-6">
            <div className="flex items-center gap-3 mb-6">
                <div className="bg-daleel-500/20 p-2 rounded-lg">
                    <Brain className="w-6 h-6 text-daleel-400" />
                </div>
                <div>
                    <h3 className="text-xl font-bold text-white">AI Reasoning Process</h3>
                    <p className="text-slate-400 text-sm">Step-by-step analysis of multi-source data</p>
                </div>
            </div>

            {/* Chain of Thought */}
            <div className="space-y-4 mb-8">
                {reasoning.reasoning_chain.map((step, idx) => (
                    <div key={idx} className="flex gap-4 group">
                        <div className="flex flex-col items-center">
                            <div className="flex-shrink-0 w-10 h-10 bg-slate-800 border border-slate-700 rounded-full flex items-center justify-center group-hover:border-daleel-500/50 transition-colors">
                                {getStepIcon(idx)}
                            </div>
                            {idx < reasoning.reasoning_chain.length - 1 && (
                                <div className="w-0.5 h-full bg-slate-700 mt-2"></div>
                            )}
                        </div>
                        <div className="flex-1 bg-slate-800/30 rounded-lg p-4 border border-slate-700/50 group-hover:bg-slate-800/50 transition-colors">
                            <p className="text-slate-300 leading-relaxed text-sm md:text-base">{step}</p>
                        </div>
                    </div>
                ))}
            </div>

            {/* Risk and Confidence Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 bg-slate-800/50 rounded-lg border border-slate-700/50">
                    <div className="flex items-center justify-between mb-2">
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Confidence Level</p>
                        <span className={`px-2 py-0.5 rounded text-xs font-bold ${reasoning.confidence_level === 'HIGH' ? 'bg-green-500/20 text-green-400 border border-green-500/30' :
                                reasoning.confidence_level === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' :
                                    'bg-red-500/20 text-red-400 border border-red-500/30'
                            }`}>
                            {reasoning.confidence_level}
                        </span>
                    </div>
                    <p className="text-slate-300 text-sm italic">
                        "{reasoning.justification}"
                    </p>
                </div>

                {reasoning.alternative_consideration && (
                    <div className="p-4 bg-purple-500/5 rounded-lg border border-purple-500/20">
                        <div className="flex items-center gap-2 mb-2">
                            <p className="text-xs font-semibold text-purple-400 uppercase tracking-widest">Alternative Analysis</p>
                        </div>
                        <p className="text-slate-300 text-sm">
                            {reasoning.alternative_consideration}
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ReasoningChain;
