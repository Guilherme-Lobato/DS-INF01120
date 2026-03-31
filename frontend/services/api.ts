const API_URL = 'http://localhost:8000';

export interface ApiConfig {
  texto: string;
  bpm: number;
  instrumento_inicial: number;
  oitava_inicial: number;
  volume_inicial: number;
}

export interface ApiEvento {
  evento: string;
  char: string;
  nota?: string;
  oitava?: number;
  volume?: number;
  instrumento?: number;
}

export interface ApiResponse {
  status: string;
  bpm: number;
  total_eventos: number;
  sequencia: ApiEvento[];
}

/**
 * Envia o texto e configurações ao backend e retorna a sequência musical.
 * Lança erro se o backend estiver offline ou retornar erro HTTP.
 */
export async function gerarSequencia(config: ApiConfig): Promise<ApiResponse> {
  const response = await fetch(`${API_URL}/enviar-form`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config),
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `Erro HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Checa se o backend está acessível.
 */
export async function checarBackend(): Promise<boolean> {
  try {
    const res = await fetch(`${API_URL}/docs`, { method: 'HEAD' });
    return res.ok;
  } catch {
    return false;
  }
}
