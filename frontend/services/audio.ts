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
  private synth: Tone.PolySynth;
  private playing = false;

  constructor() {
    this.synth = new Tone.PolySynth(Tone.Synth).toDestination();
  }

  /**
   * Toca a sequência de eventos recebida do backend.
   * onIndex é chamado a cada evento para atualizar a UI.
   * Retorna uma Promise que resolve quando terminar ou for parado.
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
      let index = 0;

      const schedule = (time: number) => {
        if (!this.playing || index >= eventos.length) {
          this.parar();
          resolve();
          return;
        }

        const ev = eventos[index];
        onIndex(index);

        switch (ev.evento) {
          case 'TOCAR_NOTA':
            if (ev.nota && ev.oitava !== undefined) {
              if (ev.instrumento !== undefined) {
                this.synth.set({ oscillator: { type: instrumentoParaOscilador(ev.instrumento) } });
              }
              if (ev.volume !== undefined) {
                const normalized = Math.max(ev.volume, 1) / 127;
                this.synth.volume.value = Tone.gainToDb(normalized);
              }
              this.synth.triggerAttackRelease(`${ev.nota}${ev.oitava}`, '8n', time);
            }
            break;

          case 'CHANGE_INSTRUMENT':
            if (ev.instrumento !== undefined) {
              this.synth.set({ oscillator: { type: instrumentoParaOscilador(ev.instrumento) } });
            }
            break;

          case 'CHANGE_VOLUME':
            if (ev.volume !== undefined) {
              const normalized = Math.max(ev.volume, 1) / 127;
              this.synth.volume.value = Tone.gainToDb(normalized);
            }
            break;

          // CHANGE_OCTAVE e PAUSA não produzem som
        }

        index++;
        transport.schedule(schedule, time + Tone.Time('8n').toSeconds());
      };

      transport.schedule(schedule, Tone.now());
      transport.start();
    });
  }

  parar(): void {
    this.playing = false;
    const transport = Tone.getTransport();
    transport.stop();
    transport.cancel();
    this.synth.releaseAll();
  }

  dispose(): void {
    this.parar();
    this.synth.dispose();
  }
}
