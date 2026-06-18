# Convenção de Instrumentos General MIDI (GM)

O enunciado é internamente contraditório quanto à numeração dos instrumentos
General MIDI — em particular sobre o instrumento base de cada voz e sobre o
Fagote (citado ora como GM 70, ora como GM 71, conforme a indexação adotada
começar em 0 ou em 1). Para evitar ambiguidade, registramos aqui a convenção
que o grupo adota e que está refletida no código.

## Convenção adotada

Adotamos **programas GM indexados de 0 a 127** (indexação base-0, padrão da
especificação MIDI para o byte de Program Change). Sob essa convenção, o número
do programa usado no código corresponde diretamente ao valor enviado no MIDI.

> Observação sobre o Fagote: na indexação base-0 o Fagote (Bassoon) é o
> **programa 70**. A referência a "GM 71" no enunciado corresponde à mesma
> sonoridade descrita em indexação base-1 (1–128). Usamos **70** (base-0).

## Instrumento base por voz (conforme implementado)

Definido em `backend/models/voz.py` (`inicializar_atributos_base`), ciclando a
cada 4 vozes (`id_voz % 4`):

| Voz | Programa GM | Instrumento   |
|-----|-------------|---------------|
| 0   | 6           | Cravo (Harpsichord) |
| 1   | 20          | Órgão (Church Organ) |
| 2   | 0           | Piano (Acoustic Grand) |
| 3   | 70          | Fagote (Bassoon) |

Vozes adicionais repetem o ciclo (Voz 4 → programa 6, Voz 5 → 20, etc.).

Esta nota é apenas documental — não houve alteração de código.
