import { useEffect, useRef } from "react";
import { TokenBadge } from "./TokenBadge";

export type Msg = { role: string; content: string };
export type Pending = { convId: string; user: string; text: string; error?: string };
export type Badge = { input: number; output: number; latencyMs?: number; label?: string };

type Props = {
  messages: Msg[];
  pending: Pending | null;
  liveBadge: Badge | null;
  badges: Badge[];          // one per saved assistant message, in order
};

function Bubble({ role, children }: { role: string; children: React.ReactNode }) {
  const user = role === "user";
  return (
    <div className={`max-w-[80%] whitespace-pre-wrap rounded-xl border px-3 py-2 ${
      user ? "self-end border-acc bg-acc text-[#1b1300]" : "border-line bg-p"}`}>
      {children}
    </div>
  );
}

export function MessageList({ messages, pending, liveBadge, badges }: Props) {
  const end = useRef<HTMLDivElement>(null);
  useEffect(() => { end.current?.scrollIntoView({ block: "end" }); }, [messages, pending, liveBadge]);

  let assistantIdx = -1;
  return (
    <div className="flex min-h-0 flex-1 flex-col gap-2.5 overflow-y-auto pb-2">
      {messages.filter((m) => m.role !== "system").map((m, i) => {
        if (m.role !== "assistant") return <Bubble key={i} role={m.role}>{m.content}</Bubble>;
        assistantIdx += 1;
        const b = badges[assistantIdx];
        return (
          <div key={i} className="flex flex-col gap-1">
            <Bubble role="assistant">{m.content}</Bubble>
            {b && <TokenBadge {...b} />}
          </div>
        );
      })}
      {pending && (
        <>
          <Bubble role="user">{pending.user}</Bubble>
          <Bubble role="assistant">
            {pending.text || (pending.error ? "" : "…")}
            {pending.error && <div className="mt-1 text-xs text-bad">error: {pending.error}</div>}
          </Bubble>
          {liveBadge && <TokenBadge {...liveBadge} />}
        </>
      )}
      <div ref={end} />
    </div>
  );
}