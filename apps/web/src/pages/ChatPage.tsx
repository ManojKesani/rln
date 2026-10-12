import { useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { useConversations, useCreateConversation, useMessages, useUsage } from "@/api/hooks";
import { ChatInput } from "@/components/ChatInput";
import { ConversationList } from "@/components/ConversationList";
import { MessageList, type Badge, type Pending } from "@/components/MessageList";
import { ModelPicker } from "@/components/ModelPicker";
import { streamChat } from "@/lib/sse";

export function ChatPage() {
  const [params, setParams] = useSearchParams();
  const convId = params.get("c");
  const qc = useQueryClient();
  const conversations = useConversations();
  const messages = useMessages(convId);
  const usage = useUsage(convId);
  const create = useCreateConversation();

  const [provider, setProvider] = useState("fake");
  const [model, setModel] = useState("fake-echo");
  const [pending, setPending] = useState<Pending | null>(null);
  const [liveBadge, setLiveBadge] = useState<Badge | null>(null);
  const [busy, setBusy] = useState(false);

  const current = conversations.data?.find((c) => c.id === convId);

  // when you open a conversation, the picker shows its remembered model
  useEffect(() => {
    if (current) { setProvider(current.provider); setModel(current.model); }
    // only re-sync when the selected conversation changes
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [convId, current?.id]);

  const select = (id: string) => { setLiveBadge(null); setParams({ c: id }); };

  const newChat = () =>
    create.mutate({ provider, model, title: null }, { onSuccess: (r) => select(r.id) });

  const send = async (content: string) => {
    if (!convId || busy) return;
    const id = convId;
    let failed = false;
    setBusy(true);
    setLiveBadge(null);
    setPending({ convId: id, user: content, text: "" });
    await streamChat(
      id,
      content,
      {
        onToken: (d) => setPending((p) => (p ? { ...p, text: p.text + d } : p)),
        onUsage: (u) => setLiveBadge({ input: u.input, output: u.output, latencyMs: u.latency_ms, label: `${provider} · ${model}` }),
        onDone: () => {},
        onError: (m) => { failed = true; setPending((p) => (p ? { ...p, error: m } : p)); },
      },
      { provider, model },
    );
    await qc.invalidateQueries({ queryKey: ["conversations"] });
    if (!failed) {
      await qc.invalidateQueries({ queryKey: ["messages", id] });
      await qc.invalidateQueries({ queryKey: ["usage", id] });
      setPending(null);
      setLiveBadge(null);
    }
    setBusy(false);
  };

  const shownPending = pending && pending.convId === convId ? pending : null;
  const badges: Badge[] = (usage.data?.calls ?? []).map((c) => ({
    input: c.input, output: c.output, latencyMs: c.latency_ms, label: `${c.provider} · ${c.model}`,
  }));
  const total = usage.data ? usage.data.input + usage.data.output : 0;

  return (
    <div className="flex h-full">
      <nav className="flex w-[220px] shrink-0 flex-col gap-2 border-r border-line bg-p p-3">
        <h1 className="font-mono text-[17px] font-bold tracking-widest text-acc">
          ✦ Trillian<div className="text-[11px] font-normal tracking-normal text-mut">mostly harmless</div>
        </h1>
        <ConversationList selectedId={convId} onSelect={select} onNew={newChat} creating={create.isPending} />
        <button onClick={() => {
          const r = document.documentElement;
          r.dataset.theme = r.dataset.theme === "light" ? "dark" : "light";
        }}>🌓 Theme</button>
      </nav>

      <main className="flex min-w-0 flex-1 flex-col p-4">
        <div className="mb-2 flex flex-wrap items-center gap-3">
          <ModelPicker provider={provider} model={model} onChange={(p, m) => { setProvider(p); setModel(m); }} />
          {convId && <span className="text-xs text-mut">total: {total} tokens (in {usage.data?.input ?? 0} · out {usage.data?.output ?? 0})</span>}
        </div>
        {!convId ? (
          <div className="m-auto text-mut">Pick a conversation, or choose a model and start a new chat.</div>
        ) : (
          <>
            {messages.isError && <div className="text-bad">Could not load messages</div>}
            <MessageList messages={messages.data ?? []} pending={shownPending} liveBadge={liveBadge} badges={badges} />
            <ChatInput onSend={send} disabled={busy} />
          </>
        )}
      </main>
    </div>
  );
}