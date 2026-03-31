import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion } from 'motion/react';
import { Play, Square, Music, Volume2, Clock, Layers, Trash2, Wifi, WifiOff } from 'lucide-react';
import { gerarSequencia, checarBackend, type ApiEvento } from './services/api';
import { AudioPlayer } from './services/audio';

export default function App() {
  // ── Estado do formulário ──
  const [text, setText] = useState('');
  const [bpm, setBpm] = useState(120);
  const [initialInstrument, setInitialInstrument] = useState(0);
  const [initialOctave, setInitialOctave] = useState(4);
  const [initialVolume, setInitialVolume] = useState(64);

  // ── Estado da reprodução ──
  const [isPlaying, setIsPlaying] = useState(false);
  const [events, setEvents] = useState<ApiEvento[]>([]);
  const [currentIndex, setCurrentIndex] = useState(-1);

  // ── Estado da UI ──
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);
  const [statusMsg, setStatusMsg] = useState('');
  const [erro, setErro] = useState('');

  // ── Refs ──
  const playerRef = useRef<AudioPlayer | null>(null);

  // ── Inicializa o player de áudio ──
  useEffect(() => {
    playerRef.current = new AudioPlayer();
    return () => playerRef.current?.dispose();
  }, []);

  // ── Checa backend ao montar ──
  useEffect(() => {
    checarBackend().then(setBackendOnline);
  }, []);

  // ── Parar reprodução ──
  const handleStop = useCallback(() => {
    playerRef.current?.parar();
    setIsPlaying(false);
    setCurrentIndex(-1);
    setStatusMsg('Parado');
  }, []);

  // ── Gerar e Tocar ──
  const handlePlay = async () => {
    // Se já está tocando, para primeiro
    if (isPlaying) {
      handleStop();
      return;
    }

    if (!text.trim()) {
      setErro('Digite algum texto antes de gerar.');
      return;
    }

    setErro('');

    if (!backendOnline) {
      setErro('Backend offline. Inicie o servidor com: python -m uvicorn app:app --reload --port 8000');
      return;
    }

    try {
      // Garante que qualquer reprodução anterior parou
      playerRef.current?.parar();

      setStatusMsg('Enviando texto ao backend...');

      const data = await gerarSequencia({
        texto: text,
        bpm,
        instrumento_inicial: initialInstrument,
        oitava_inicial: initialOctave,
        volume_inicial: initialVolume,
      });

      setEvents(data.sequencia);
      setStatusMsg(`${data.total_eventos} eventos gerados`);
      setIsPlaying(true);
      setCurrentIndex(0);

      await playerRef.current?.tocar(data.sequencia, bpm, (i) => {
        setCurrentIndex(i);
      });

      // Terminou naturalmente
      setIsPlaying(false);
      setCurrentIndex(-1);
      setStatusMsg('Reprodução finalizada');
    } catch (err: any) {
      setErro(err.message || 'Erro ao comunicar com o backend');
      setStatusMsg('');
      setIsPlaying(false);
    }
  };

  const clearText = () => {
    handleStop();
    setText('');
    setEvents([]);
    setStatusMsg('');
    setErro('');
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-[#e5e5e5] font-sans selection:bg-orange-500/30">
      {/* ═══ Header ═══ */}
      <header className="border-b border-white/10 p-6 flex justify-between items-center bg-black/40 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-orange-500 rounded-full flex items-center justify-center shadow-lg shadow-orange-500/20">
            <Music className="text-black w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tighter uppercase italic">Texto para Música</h1>
            <p className="text-[10px] uppercase tracking-widest opacity-50 font-mono">UFRGS — INF01120 — Fase 1</p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs font-mono">
          {backendOnline === null ? (
            <span className="opacity-40">verificando...</span>
          ) : backendOnline ? (
            <>
              <Wifi className="w-4 h-4 text-green-400" />
              <span className="text-green-400">Backend online</span>
            </>
          ) : (
            <>
              <WifiOff className="w-4 h-4 text-red-400" />
              <span className="text-red-400">Backend offline</span>
            </>
          )}
        </div>
      </header>

      {/* ═══ Conteúdo Principal ═══ */}
      <main className="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* ── Coluna Esquerda: Entrada e Controles ── */}
        <div className="lg:col-span-8 space-y-6">
          {/* Campo de Texto */}
          <section className="relative group">
            <div className="absolute -top-3 left-4 px-2 bg-[#0a0a0a] text-[10px] uppercase tracking-widest font-mono z-10 text-orange-500">
              Entrada de Texto
            </div>
            <div className="relative">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Digite ou cole seu texto aqui (conto, poema, notícia...)"
                className="w-full h-64 bg-white/5 border border-white/10 rounded-xl p-6 font-mono text-lg focus:outline-none focus:border-orange-500/50 transition-all resize-none"
              />
              <button
                onClick={clearText}
                className="absolute bottom-4 right-4 p-2 hover:bg-red-500/20 rounded-lg transition-colors text-red-400"
                title="Limpar"
              >
                <Trash2 className="w-5 h-5" />
              </button>
            </div>
          </section>

          {/* Configurações — Requisito 4 do enunciado */}
          <section className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
            <ConfigCard icon={<Clock className="w-4 h-4" />} label="BPM" value={bpm} onChange={setBpm} min={40} max={240} />
            <ConfigCard icon={<Layers className="w-4 h-4" />} label="Instrumento" value={initialInstrument} onChange={setInitialInstrument} min={0} max={127} />
            <ConfigCard icon={<Music className="w-4 h-4" />} label="Oitava" value={initialOctave} onChange={setInitialOctave} min={1} max={8} />
            <ConfigCard icon={<Volume2 className="w-4 h-4" />} label="Volume" value={initialVolume} onChange={setInitialVolume} min={0} max={127} />
          </section>

          {/* Botão de Tocar / Parar */}
          <div className="flex flex-col gap-2">
            <button
              onClick={handlePlay}
              disabled={backendOnline === false}
              className={`flex-1 flex items-center justify-center gap-3 py-4 rounded-xl font-bold uppercase tracking-widest transition-all ${
                isPlaying
                  ? 'bg-red-500 hover:bg-red-600 text-white'
                  : backendOnline === false
                    ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
                    : 'bg-orange-500 hover:bg-orange-600 text-black'
              }`}
            >
              {isPlaying ? <Square className="w-6 h-6 fill-current" /> : <Play className="w-6 h-6 fill-current" />}
              {isPlaying ? 'Parar' : 'Gerar e Tocar'}
            </button>

            {statusMsg && <p className="text-center text-xs font-mono opacity-50">{statusMsg}</p>}
            {erro && <p className="text-center text-xs font-mono text-red-400">{erro}</p>}
          </div>
        </div>

        {/* ── Coluna Direita: Visualização da Sequência ── */}
        <div className="lg:col-span-4 space-y-6">
          <section className="bg-white/5 border border-white/10 rounded-xl p-6 h-[400px] flex flex-col">
            <div className="text-[10px] uppercase tracking-widest font-mono text-orange-500 mb-4">
              Sequência Musical
            </div>
            <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
              <div className="flex flex-wrap gap-2">
                {events.length > 0 ? (
                  events.map((ev, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{
                        scale: idx === currentIndex ? 1.2 : 1,
                        opacity: 1,
                        backgroundColor: idx === currentIndex ? '#f97316' : 'rgba(255,255,255,0.1)',
                        color: idx === currentIndex ? '#000' : '#fff',
                      }}
                      className="w-8 h-8 flex items-center justify-center rounded text-xs font-mono font-bold transition-colors"
                    >
                      {ev.char === '\\n' ? '↵' : ev.char === ' ' ? '·' : ev.char}
                    </motion.div>
                  ))
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-white/20 italic text-sm text-center">
                    Aguardando geração...
                  </div>
                )}
              </div>
            </div>
          </section>

          {/* Evento Atual */}
          {isPlaying && currentIndex >= 0 && events[currentIndex] && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-orange-500 text-black p-4 rounded-xl flex justify-between items-center"
            >
              <div className="text-xs font-bold uppercase">Evento Atual</div>
              <div className="text-2xl font-black font-mono">
                {events[currentIndex].evento === 'TOCAR_NOTA'
                  ? `${events[currentIndex].nota}${events[currentIndex].oitava}`
                  : events[currentIndex].evento === 'PAUSA'
                    ? '—'
                    : events[currentIndex].evento.replace('CHANGE_', '')}
              </div>
            </motion.div>
          )}
        </div>
      </main>

      <style>{`
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(249,115,22,0.5); }
      `}</style>
    </div>
  );
}

// ── Componentes auxiliares ──

function ConfigCard({ icon, label, value, onChange, min, max }: {
  icon: React.ReactNode;
  label: string;
  value: number;
  onChange: (v: number) => void;
  min: number;
  max: number;
}) {
  return (
    <div className="bg-white/5 border border-white/10 rounded-xl p-4 space-y-2">
      <div className="flex items-center gap-2 text-[10px] uppercase tracking-widest opacity-50 font-mono">
        {icon}
        {label}
      </div>
      <input
        type="number"
        value={value}
        onChange={(e) => onChange(Math.max(min, Math.min(max, parseInt(e.target.value) || min)))}
        className="bg-transparent text-xl font-bold font-mono w-full focus:outline-none text-orange-500"
      />
      <input
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={(e) => onChange(parseInt(e.target.value))}
        className="w-full accent-orange-500 h-1 bg-white/10 rounded-lg appearance-none cursor-pointer"
      />
    </div>
  );
}
