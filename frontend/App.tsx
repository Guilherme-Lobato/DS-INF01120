import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion } from 'motion/react';
import { Play, Square, Music, Volume2, Clock, Layers, Trash2, Upload, Download, FileAudio } from 'lucide-react';
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
  const [midiBase64, setMidiBase64] = useState<string | null>(null);

  // ── Estado da UI ──
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);
  const [statusMsg, setStatusMsg] = useState('');
  const [erro, setErro] = useState('');

  // ── Refs ──
  const playerRef = useRef<AudioPlayer | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle do arquivo aberto via File System Access API (quando suportada),
  // usado para "Salvar" sobrescrevendo o arquivo original.
  const fileHandleRef = useRef<FileSystemFileHandle | null>(null);
  const [hasFileHandle, setHasFileHandle] = useState(false);
  const supportsFS = typeof (window as any).showSaveFilePicker === 'function';

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
      setMidiBase64(data.midi_base64 || null);
      setStatusMsg(`${data.total_eventos} eventos gerados`);
      setIsPlaying(true);
      setCurrentIndex(0);

      await playerRef.current?.tocar(data.sequencia, bpm, (i) => {
        setCurrentIndex(i);
      });

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
    setMidiBase64(null);
    setStatusMsg('');
    setErro('');
  };

  // ── Manipulação de Arquivos ──

  // Importar: usa showOpenFilePicker quando disponível para guardar o handle
  // (permitindo sobrescrever depois). Sem suporte, cai no <input type="file">.
  const handleImport = async () => {
    if (supportsFS) {
      try {
        const [handle] = await (window as any).showOpenFilePicker({
          types: [{ description: 'Texto', accept: { 'text/plain': ['.txt'] } }],
        });
        const file = await handle.getFile();
        setText(await file.text());
        fileHandleRef.current = handle;
        setHasFileHandle(true);
        setStatusMsg(`Arquivo "${file.name}" importado`);
      } catch {
        // Usuário cancelou o seletor — nada a fazer.
      }
    } else {
      fileInputRef.current?.click();
    }
  };

  // Fallback de importação para navegadores sem File System Access API.
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      setText(event.target?.result as string);
      // O <input type="file"> não fornece handle de escrita; sem sobrescrita.
      fileHandleRef.current = null;
      setHasFileHandle(false);
    };
    reader.readAsText(file);
  };

  // Escreve o texto atual em um handle de arquivo.
  const escreverHandle = async (handle: FileSystemFileHandle) => {
    const writable = await (handle as any).createWritable();
    await writable.write(text);
    await writable.close();
  };

  // Salvar: sobrescreve o arquivo original (quando há handle). Caso contrário,
  // delega para "Salvar como".
  const handleSave = async () => {
    if (fileHandleRef.current) {
      try {
        await escreverHandle(fileHandleRef.current);
        setStatusMsg('Arquivo salvo (original sobrescrito)');
      } catch (err: any) {
        setErro('Falha ao salvar: ' + (err?.message || 'erro desconhecido'));
      }
    } else {
      handleSaveAs();
    }
  };

  // Salvar como: escolhe novo arquivo (FS API) ou baixa (.txt) como fallback.
  const handleSaveAs = async () => {
    if (supportsFS) {
      try {
        const handle = await (window as any).showSaveFilePicker({
          suggestedName: 'composicao.txt',
          types: [{ description: 'Texto', accept: { 'text/plain': ['.txt'] } }],
        });
        await escreverHandle(handle);
        fileHandleRef.current = handle;
        setHasFileHandle(true);
        setStatusMsg('Arquivo salvo');
      } catch {
        // Usuário cancelou o seletor.
      }
    } else {
      // Fallback: download tradicional.
      const blob = new Blob([text], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'composicao.txt';
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  const handleDownloadMidi = () => {
    if (!midiBase64) return;
    const byteCharacters = atob(midiBase64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'audio/midi' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'fuga_bach.mid';
    a.click();
    URL.revokeObjectURL(url);
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
          </div>
        </div>
      </header>

      {/* ═══ Conteúdo Principal ═══ */}
      <main className="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* ── Coluna Esquerda: Entrada e Controles ── */}
        <div className="lg:col-span-8 space-y-6">
          {/* Ações de Arquivo */}
          <div className="flex gap-4">
            <input type="file" accept=".txt" ref={fileInputRef} onChange={handleFileUpload} className="hidden" />
            <button onClick={handleImport} className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 rounded border border-white/10 transition-colors text-sm font-mono uppercase">
              <Upload className="w-4 h-4" /> Importar TXT
            </button>
            <button onClick={handleSave} disabled={!text.trim() || !hasFileHandle} title={hasFileHandle ? 'Sobrescreve o arquivo importado' : 'Importe um arquivo para sobrescrever'} className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 disabled:opacity-50 disabled:cursor-not-allowed rounded border border-white/10 transition-colors text-sm font-mono uppercase">
              <Download className="w-4 h-4" /> Salvar
            </button>
            <button onClick={handleSaveAs} disabled={!text.trim()} title={supportsFS ? 'Salvar em um novo arquivo' : 'Baixar como .txt'} className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 disabled:opacity-50 disabled:cursor-not-allowed rounded border border-white/10 transition-colors text-sm font-mono uppercase">
              <Download className="w-4 h-4" /> Salvar como
            </button>
            <button onClick={handleDownloadMidi} disabled={!midiBase64} className="flex items-center gap-2 px-4 py-2 bg-orange-500/20 hover:bg-orange-500/40 text-orange-400 disabled:opacity-50 disabled:cursor-not-allowed rounded border border-orange-500/30 transition-colors text-sm font-mono uppercase ml-auto">
              <FileAudio className="w-4 h-4" /> Baixar MIDI
            </button>
          </div>

          {/* Campo de Texto */}
          <section className="relative group">
            <div className="absolute -top-3 left-4 px-2 bg-[#0a0a0a] text-[10px] uppercase tracking-widest font-mono z-10 text-orange-500">
              Entrada de Texto
            </div>
            <div className="relative">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Digite ou cole seu texto aqui (ex: [0] C D E F \n [4] G A B C)"
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

          {/* Configurações Globais */}
          <section className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
            {/* min=10 alinhado ao piso do backend (ContextoGlobal.desacelerar).
                O enunciado não define teto; adotamos 300 como teto de UI
                (suposição documentada em docs/Registros/CorrecaoCampoBpm.md). */}
            <ConfigCard icon={<Clock className="w-4 h-4" />} label="BPM" value={bpm} onChange={setBpm} min={10} max={300} showSlider />
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

          {/* Regras de Mapeamento */}
          <details className="bg-white/5 border border-white/10 rounded-xl p-4 group">
            <summary className="text-[10px] uppercase tracking-widest font-mono text-orange-500 cursor-pointer flex justify-between items-center outline-none">
              Regras de Mapeamento (Clique para expandir)
              <span className="group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-mono text-white/70">
              <div>
                <h4 className="font-bold text-white mb-2">Estrutura (Fuga de Bach)</h4>
                <ul className="space-y-1 list-disc list-inside">
                  <li>Cada linha do texto é uma voz independente (Voz 0, 1, 2...).</li>
                  <li><span className="text-orange-400">[n]</span>: No início da linha, atrasa n beats (ex: [4]).</li>
                </ul>
                <h4 className="font-bold text-white mt-3 mb-2">Notas e Pausas</h4>
                <ul className="space-y-1 list-disc list-inside">
                  <li><span className="text-orange-400">A a G</span>: Notas (Lá a Sol).</li>
                  <li><span className="text-orange-400">H</span>: Nota Si Bemol.</li>
                  <li><span className="text-orange-400">a a h minúsculas</span>: Pausa.</li>
                  <li><span className="text-orange-400">Consoantes (outras)</span>: Repete última nota ou pausa.</li>
                </ul>
              </div>
              <div>
                <h4 className="font-bold text-white mb-2">Controles e Instrumentos</h4>
                <ul className="space-y-1 list-disc list-inside">
                  <li><span className="text-orange-400">Espaço</span>: Dobra o volume da voz atual.</li>
                  <li><span className="text-orange-400">? ou .</span>: Aumenta a oitava da voz.</li>
                  <li><span className="text-orange-400">V</span>: Diminui a oitava da voz.</li>
                  <li><span className="text-orange-400">&gt; / &lt;</span>: Aumenta / Diminui o BPM global.</li>
                  <li><span className="text-orange-400">!</span>: Instrumento Harmônica (GM 22).</li>
                  <li><span className="text-orange-400">Dígito Par</span>: Soma ao instrumento atual.</li>
                  <li><span className="text-orange-400">Dígito Ímpar ou ;</span>: Tubular Bells (GM 15).</li>
                  <li><span className="text-orange-400">,</span>: Church Organ (GM 20).</li>
                </ul>
              </div>
            </div>
          </details>
        </div>

        {/* ── Coluna Direita: Visualização da Sequência ── */}
        <div className="lg:col-span-4 space-y-6">
          <section className="bg-white/5 border border-white/10 rounded-xl p-6 h-[400px] flex flex-col">
            <div className="text-[10px] uppercase tracking-widest font-mono text-orange-500 mb-4">
              Sequência Musical (Vozes Mescladas)
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
                      className="px-2 h-8 flex items-center justify-center rounded text-xs font-mono font-bold transition-colors"
                      title={`Voz: ${ev.voz_id} | Beat: ${ev.beat_absoluto}`}
                    >
                      {ev.char === '\\n' ? '↵' : ev.char === ' ' ? '·' : ev.char}
                      {ev.voz_id !== undefined && <span className="ml-1 opacity-50 text-[8px]">v{ev.voz_id}</span>}
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
              <div className="text-xs font-bold uppercase">Voz {events[currentIndex].voz_id}</div>
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

function ConfigCard({ icon, label, value, onChange, min, max, showSlider }: {
  icon: React.ReactNode;
  label: string;
  value: number;
  onChange: (v: number) => void;
  min: number;
  max: number;
  showSlider?: boolean;
}) {
  return (
    <div className="bg-white/5 border border-white/10 rounded-xl p-4 space-y-2">
      <div className="flex items-center justify-between gap-2 text-[10px] uppercase tracking-widest opacity-50 font-mono">
        <div className="flex items-center gap-2">
            {icon}
            {label}
        </div>
        <span className="text-xl font-bold font-mono text-orange-500">{value}</span>
      </div>
      {showSlider && (
        <input
          type="range"
          min={min}
          max={max}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full accent-orange-500"
        />
      )}
    </div>
  );
}
