/**
 * S-007: Reads a streaming POST and calls handlers per event
 * Imports: fetch, ReadableStream
 * Exports: streamChat(id, content, handlers)
 */
export type StreamUsage = { input: number; output: number; latency_ms: number };

export type StreamHandlers = {
  onToken: (delta: string) => void;
  onUsage: (u: StreamUsage) => void;
  onDone: () => void;
  onError: (message: string) => void;
};

export async function streamChat(id: string, content: string, h: StreamHandlers,
  override?: { provider: string; model: string },
): Promise<void> {
  let finished = false;

  const dispatch = (block: string) => {
    let event = "message";
    let data = "";
    for (const line of block.split("\n")) {
      if (line.startsWith("event:")) event = line.slice(6).trim();
      else if (line.startsWith("data:")) data += line.slice(5).trim();
    }
    let payload: any = {};
    try { payload = data ? JSON.parse(data) : {}; } catch { /* ignore */ }
    if (event === "token") h.onToken(payload.delta ?? "");
    else if (event === "usage") h.onUsage(payload);
    else if (event === "done") { finished = true; h.onDone(); }
    else if (event === "error") { finished = true; h.onError(payload.message ?? "error"); }
  };

  let res: Response;
  try {
    res = await fetch(`/api/conversations/${id}/stream`, {
      method: "POST",
      credentials: "include",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ content, provider: override?.provider, model: override?.model }),
        });
  } catch {
    h.onError("NetworkError");
    return;
  }
  if (!res.ok || !res.body) {
    h.onError(`HTTP ${res.status}`);
    return;
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buf = "";
  try {
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      let i: number;
      while ((i = buf.indexOf("\n\n")) >= 0) {
        dispatch(buf.slice(0, i));
        buf = buf.slice(i + 2);
      }
    }
  } catch {
    if (!finished) { finished = true; h.onError("StreamInterrupted"); }
  }
  if (!finished) h.onError("stream ended without done");
}