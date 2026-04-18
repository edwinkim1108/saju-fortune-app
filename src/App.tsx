/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { 
  User, 
  Calendar, 
  Clock, 
  Users, 
  LayoutDashboard, 
  ChevronRight, 
  Sparkles, 
  BarChart3, 
  BookOpen, 
  ShieldCheck,
  Gem
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  Radar, 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  ResponsiveContainer 
} from 'recharts';
import { format } from 'date-fns';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { cn } from './lib/utils';
import { IntegratedSajuEngine, KAN_DETAILS, STRATEGY_DETAILS } from './lib/sajuEngine';

export default function App() {
  const [formData, setFormData] = useState({
    name: '김준우',
    gender: '남성',
    birthDate: '1983-11-08',
    birthTime: '00:00'
  });

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [engineResult, setEngineResult] = useState<IntegratedSajuEngine | null>(null);
  const [aiReport, setAiReport] = useState<string>('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleRunAnalysis = async () => {
    setIsAnalyzing(true);
    setAiReport('');
    
    // 1. Local Engine & Report Generation (Zero-API)
    const result = new IntegratedSajuEngine(
      formData.name,
      formData.gender,
      formData.birthDate,
      formData.birthTime
    );
    
    // Simulate generation time for UX
    setTimeout(() => {
      setEngineResult(result);
      const report = result.generateLocalReport();
      setAiReport(report);
      setIsAnalyzing(false);
      
      if (window.innerWidth < 1024) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }, 1000);
  };

  const radarData = useMemo(() => {
    if (!engineResult) return [];
    return Object.entries(engineResult.elements).map(([key, value]) => ({
      subject: key,
      A: value,
      fullMark: 50,
    }));
  }, [engineResult]);

  return (
    <div className="min-h-screen font-sans flex flex-col lg:flex-row">
      {/* Sidebar */}
      <aside className="w-full lg:w-80 bg-white border-b lg:border-r border-slate-200 p-6 lg:h-screen lg:sticky lg:top-0 overflow-y-auto shrink-0">
        <div className="flex items-center gap-2 mb-8">
          <div className="p-2 bg-slate-900 rounded-xl">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-xl font-extrabold tracking-tight text-slate-900 uppercase">
            AI 명리 <br/><span className="text-slate-500 font-medium text-sm">기질 분석 컨설팅</span>
          </h1>
        </div>

        <div className="space-y-6">
          <section>
            <label className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              <User className="w-3.5 h-3.5" />
              성함 / 학생 이름
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-900 transition-all"
              placeholder="예: 김준우"
            />
          </section>

          <section>
            <label className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              <Users className="w-3.5 h-3.5" />
              성별
            </label>
            <div className="flex gap-2">
              {['남성', '여성'].map(g => (
                <button
                  key={g}
                  onClick={() => setFormData(prev => ({ ...prev, gender: g }))}
                  className={cn(
                    "flex-1 py-2.5 rounded-xl text-sm font-medium transition-all border",
                    formData.gender === g 
                      ? "bg-slate-900 text-white border-slate-900 shadow-lg shadow-slate-200" 
                      : "bg-white text-slate-600 border-slate-200 hover:border-slate-300"
                  )}
                >
                  {g}
                </button>
              ))}
            </div>
          </section>

          <section>
            <label className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              <Calendar className="w-3.5 h-3.5" />
              생년월일
            </label>
            <input
              type="date"
              name="birthDate"
              value={formData.birthDate}
              onChange={handleInputChange}
              className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-900 transition-all uppercase"
            />
          </section>

          <section>
            <label className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              <Clock className="w-3.5 h-3.5" />
              태어난 시간
            </label>
            <input
              type="time"
              name="birthTime"
              value={formData.birthTime}
              onChange={handleInputChange}
              className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-900 transition-all"
            />
          </section>

          <button
            onClick={handleRunAnalysis}
            disabled={isAnalyzing}
            className="w-full mt-4 flex items-center justify-center gap-2 p-4 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 transition-all active:scale-[0.98] disabled:opacity-50"
          >
            {isAnalyzing ? (
              <>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
                >
                  <Sparkles className="w-5 h-5" />
                </motion.div>
                분석 중...
              </>
            ) : (
              <>
                전문 컨설팅 리포트 발행
                <ChevronRight className="w-5 h-5" />
              </>
            )}
          </button>

          <div className="pt-6 border-t border-slate-100">
            <p className="text-[10px] text-slate-400 leading-relaxed italic text-center">
              ※ 입력하신 데이터는 철저히 암호화되어 일관된 분석 결과를 도출하는 씨앗값으로 사용되며 별도로 저장되지 않습니다.
            </p>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-6 lg:p-12 overflow-y-auto max-w-7xl mx-auto w-full">
        {!engineResult ? (
          <div className="h-full flex flex-col items-center justify-center text-center py-20">
            <div className="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mb-6 animate-pulse">
              <LayoutDashboard className="w-10 h-10 text-slate-300" />
            </div>
            <h2 className="text-2xl font-bold text-slate-900 mb-2">분석 준비 완료</h2>
            <p className="text-slate-500 max-w-md">
              왼쪽 사이드바에서 학생 정보를 입력하고 버튼을 눌러 정확한 명리학적 기질 분석 결과와 학습 처방 레포트를 확인하세요.
            </p>
          </div>
        ) : (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8"
          >
            {/* Header */}
            <header className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-slate-200 pb-8">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="px-2 py-0.5 bg-slate-900 text-white text-[10px] font-bold rounded uppercase tracking-tighter">CONFIDENTIAL</span>
                  <span className="text-xs text-slate-400 font-medium">{format(new Date(), 'yyyy. MM. dd')} 발행</span>
                </div>
                <h2 className="text-4xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
                  {formData.name} <span className="font-medium text-slate-400 text-2xl lg:text-3xl">학생 통합 기질 보고서</span>
                </h2>
              </div>
              <div className="flex gap-4">
                <div className="text-right">
                  <p className="text-[10px] text-slate-400 uppercase font-bold tracking-widest">ID SEED</p>
                  <p className="text-xs font-mono text-slate-500">{engineResult.seedHash.toString().substring(0, 16)}...</p>
                </div>
              </div>
            </header>

            <div className="grid grid-cols-1 xl:grid-cols-12 gap-8">
              {/* Left Column: Visual Data */}
              <div className="xl:col-span-4 space-y-6">
                <section className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">
                  <h3 className="flex items-center gap-2 text-sm font-bold text-slate-900 mb-6 uppercase tracking-wider">
                    <BarChart3 className="w-4 h-4" />
                    기질 에너지 맵
                  </h3>
                  <div className="h-[280px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                        <PolarGrid stroke="#E2E8F0" />
                        <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748B', fontSize: 13, fontWeight: 600 }} />
                        <PolarRadiusAxis angle={30} domain={[0, 50]} tick={false} axisLine={false} />
                        <Radar
                          name="Energy"
                          dataKey="A"
                          stroke="#0F172A"
                          strokeWidth={2}
                          fill="#0F172A"
                          fillOpacity={0.1}
                        />
                      </RadarChart>
                    </ResponsiveContainer>
                  </div>
                  
                  <div className="mt-8 space-y-4">
                    <div>
                      <div className="flex justify-between items-end mb-2">
                        <span className="text-sm font-bold text-slate-700">자아 에너지 강도</span>
                        <span className="text-xs font-bold text-slate-900">
                           {engineResult.strength > 0 ? `신강 (${engineResult.strength})` : `신약 (${engineResult.strength})`}
                        </span>
                      </div>
                      <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                        <motion.div 
                          initial={{ width: 0 }}
                          animate={{ width: `${((engineResult.strength + 30) / 60) * 100}%` }}
                          className="h-full bg-slate-900"
                        />
                      </div>
                      <p className="mt-2 text-[11px] text-slate-400 leading-relaxed">
                        {engineResult.strength > 0 
                          ? '본인의 주관이 뚜렷하고 외부 자극보다 내면의 동기로 움직이는 주도적 성향입니다.' 
                          : '주변 환경과 조화를 중요시하며 타인과의 소통과 협력을 통해 에너지를 얻는 상생적 성향입니다.'}
                      </p>
                    </div>
                  </div>
                </section>

                <section className="bg-slate-900 text-white p-6 rounded-3xl border border-slate-800 shadow-xl overflow-hidden relative">
                  <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none">
                    <Gem className="w-32 h-32" />
                  </div>
                  <h3 className="flex items-center gap-2 text-sm font-bold mb-4 uppercase tracking-wider">
                    <Sparkles className="w-4 h-4 text-amber-400" />
                    오늘의 학습 행운
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-white/10 p-4 rounded-2xl backdrop-blur-sm">
                      <p className="text-[10px] text-white/50 uppercase font-bold mb-1">Color</p>
                      <p className="text-lg font-bold">
                        {['임','계'].includes(engineResult.ilGan) ? 'Blue' : 
                         ['갑','을'].includes(engineResult.ilGan) ? 'Green' :
                         ['병','정'].includes(engineResult.ilGan) ? 'Red' :
                         ['무','기'].includes(engineResult.ilGan) ? 'Yellow' : 'White'}
                      </p>
                    </div>
                    <div className="bg-white/10 p-4 rounded-2xl backdrop-blur-sm">
                      <p className="text-[10px] text-white/50 uppercase font-bold mb-1">Time</p>
                      <p className="text-lg font-bold">14:00 ~ 16:00</p>
                    </div>
                  </div>
                  <p className="mt-4 text-xs text-white/60 leading-relaxed italic">
                    "가장 강력한 오행의 기운이 활성화되는 시간대에 심화 학습을 배치하세요."
                  </p>
                </section>
              </div>

              {/* Right Column: Narrative Reports */}
              <div className="xl:col-span-8 space-y-8">
                <section className="bg-white p-8 lg:p-10 rounded-[2rem] border border-slate-100 shadow-sm relative">
                  <div className="max-w-none prose prose-slate">
                    {/* AI Deep Analysis Section */}
                    {aiReport && (
                      <motion.div 
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="mb-12"
                      >
                        <div className="inline-flex items-center gap-2 px-3 py-1 bg-indigo-50 text-indigo-900 rounded-full border border-indigo-100 mb-6">
                          <Gem className="w-3.5 h-3.5" />
                          <span className="text-[10px] font-bold uppercase tracking-widest text-[#4F46E5]">Expert Consultation Deep Analysis</span>
                        </div>
                        <div className="markdown-body text-slate-700 leading-relaxed text-lg prose-headings:text-slate-900 prose-headings:font-bold prose-p:mb-4 prose-ul:mb-4 prose-strong:text-indigo-600 prose-li:my-1">
                          <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {aiReport}
                          </ReactMarkdown>
                        </div>
                      </motion.div>
                    )}

                    {!aiReport && isAnalyzing && (
                      <div className="py-20 flex flex-col items-center justify-center space-y-4">
                        <motion.div
                          animate={{ rotate: 360 }}
                          transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                        >
                          <Sparkles className="w-12 h-12 text-indigo-400" />
                        </motion.div>
                        <p className="text-slate-400 font-medium animate-pulse">전문가 시스템이 귀하의 기운을 심층 분석하고 있습니다...</p>
                      </div>
                    )}

                    {engineResult && (
                      <div className="pt-10 border-t border-slate-100">
                        <div className="inline-flex items-center gap-2 px-3 py-1 bg-slate-50 text-slate-900 rounded-full border border-slate-100 mb-6">
                        <span className="w-1.5 h-1.5 bg-slate-900 rounded-full"></span>
                        <span className="text-[10px] font-bold uppercase tracking-widest">분석 데이터 요약 (ID-Base)</span>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                          <p className="text-xs font-bold text-slate-400 uppercase mb-2">기본 기질</p>
                          <p className="text-lg font-bold text-slate-800">{engineResult.ilGan} ({KAN_DETAILS[engineResult.ilGan].title})</p>
                        </div>
                        <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                          <p className="text-xs font-bold text-slate-400 uppercase mb-2">핵심 학습 전략</p>
                          <p className="text-sm font-medium text-slate-600 leading-relaxed">{STRATEGY_DETAILS[KAN_DETAILS[engineResult.ilGan].ten_god]}</p>
                        </div>
                      </div>
                    </div>
                    )}
                  </div>

                  <footer className="mt-12 pt-8 border-t border-slate-100 flex justify-between items-center text-[10px] text-slate-400 font-medium uppercase tracking-widest">
                    <span>Expert Myeong-Ri Analysis Engine v3.0 (Zero-API)</span>
                    <span>Verified High-End Report</span>
                  </footer>
                </section>
              </div>
            </div>
          </motion.div>
        )}
      </main>
    </div>
  );
}
