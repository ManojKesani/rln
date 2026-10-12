/**
 * S-007: Lists conversations, New chat button
 * Imports: hooks.useConversations
 * Exports: ConversationList
 */
import { useConversations } from "@/api/hooks";

type Props = { selectedId: string | null; onSelect: (id: string) => void; onNew: () => void; creating: boolean };

export function ConversationList({ selectedId, onSelect, onNew, creating }: Props) {
  const { data, isPending, isError } = useConversations();
  return (
    <div className="flex min-h-0 flex-1 flex-col gap-1">
      <button className="pri mb-2" onClick={onNew} disabled={creating}>+ New chat</button>
      <div className="min-h-0 flex-1 overflow-y-auto">
        {isPending && <div className="px-2 text-mut">Loading…</div>}
        {isError && <div className="px-2 text-bad">Could not load conversations</div>}
        {data?.map((c) => (
          <div key={c.id} onClick={() => onSelect(c.id)}
               className={`cursor-pointer rounded-md px-2 py-1.5 ${c.id === selectedId ? "bg-p2 text-fg" : "text-mut hover:bg-p2"}`}>
            <div className="truncate">{c.title ?? "New chat"}</div>
            <div className="truncate text-[11px]">{c.provider} · {c.model}</div>
          </div>
        ))}
      </div>
    </div>
  );
}