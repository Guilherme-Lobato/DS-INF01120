import * as Tone from 'tone';
import type { ApiEvento } from './api';

/**
 * Mapeia número de instrumento MIDI para tipo de oscilador do Tone.js.
 * Agrupa os 128 instrumentos MIDI em famílias de timbre.
 */
function instrumentoParaOscilador(instrumento: number): Tone.ToneOscillatorType {
  if (instrumento < 8)   return 'sine';
  if (instrumento < 16)  return 'triangle';
  if (instrumento < 24)  return 'square';
  if (instrumento < 32)  return 'sawtooth';
  if (instrumento < 40)  return 'sine';
  if (instrumento < 48)  return 'triangle';
  if (instrumento < 56)  return 'square';
  if (instrumento < 64)  return 'sawtooth';
  if (instrumento < 72)  return 'sine';
  if (instrumento < 80)  return 'triangle';
  if (instrumento < 88)  return 'square';
  if (instrumento < 96)  return 'sawtooth';
  if (instrumento < 104) return 'sine';
  if (instrumento < 112) return 'triangle';
  if (instrumento < 120) return 'square';
  return 'sawtooth';
}

export class AudioPlayer {
  private synths: Record<number, Tone.PolySynth> = {};
  private playing = false;

  private getSynth(voz_id: number): Tone.PolySynth {
    if (!this.synths[voz_id]) {
      this.synths[voz_id] = new Tone.PolySynth(Tone.Synth).toDestination();
    }
    return this.synths[voz_id];
  }

  /**
   * Toca a sequência de eventos (Polifônica) calculando os tempos absolutos.
   */
  async tocar(
    eventos: ApiEvento[],
    bpm: number,
    onIndex: (i: number) => void,
  ): Promise<void> {
    await Tone.start();
    this.playing = true;

    const transport = Tone.getTransport();
    transport.bpm.value = bpm;
    transport.cancel();
    transport.stop();

    return new Promise<void>((resolve) => {
      let activeEvents = 0;

      if (eventos.length === 0) {
        resolve();
        return;
      }

      eventos.forEach((ev, index) => {
        const beat = ev.beat_absoluto ?? index;
        const time = beat * (60 / bpm); // Em segundos absolutos

        transport.schedule((t) => {
          if (!this.playing) return;
          
          onIndex(index);

          const trackId = ev.voz_id ?? 0;
          const synth = this.getSynth(trackId);

          switch (ev.evento) {
            case 'CHANGE_BPM':
              if (ev.bpm) transport.bpm.value = ev.bpm;
              break;

            case 'TOCAR_NOTA':
              if (ev.nota && ev.oitava !== undefined) {
                if (ev.instrumento !== undefined) {
                  synth.set({ oscillator: { type: instrumentoParaOscilador(ev.instrumento) } });
                }
                if (ev.volume !== undefined) {
                  const normalized = Math.max(ev.volume, 1) / 127;
                  synth.volume.value = Tone.gainToDb(normalized);
                }
                // Duração de 1 beat
                synth.triggerAttackRelease(`${ev.nota}${ev.oitava}`, 60 / transport.bpm.value, t);
              }
              break;

            case 'CHANGE_INSTRUMENT':
              if (ev.instrumento !== undefined) {
                synth.set({ oscillator: { type: instrumentoParaOscilador(ev.instrumento) } });
              }
              break;

            case 'CHANGE_VOLUME':
              if (ev.volume !== undefined) {
                const normalized = Math.max(ev.volume, 1) / 127;
                synth.volume.value = Tone.gainToDb(normalized);
              }
              break;
          }

          activeEvents++;
          if (activeEvents >= eventos.length) {
            setTimeout(() => {
              this.parar();
              resolve();
            }, (60 / transport.bpm.value) * 1000);
          }
        }, `+${time}`);
      });

      transport.start();
    });
  }

  parar(): void {
    this.playing = false;
    const transport = Tone.getTransport();
    transport.stop();
    transport.cancel();
    Object.values(this.synths).forEach((s) => s.releaseAll());
  }

  dispose(): void {
    this.parar();
    Object.values(this.synths).forEach((s) => s.dispose());
    this.synths = {};
  }
}
