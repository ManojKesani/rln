/**
 * S-008: Shows in/out tokens and latency under a reply
 * Imports: (props)
 * Exports: TokenBadge
 */
type Props = { input: number; output: number; latencyMs?: number; label?: string };

export function TokenBadge({ input, output, latencyMs, label }: Props) {
  return (
    <div className="text-[11px] text-mut">
      {label && <span className="mr-2">{label}</span>}
      in {input} · out {output}{latencyMs !== undefined ? ` · ${latencyMs} ms` : ""}
    </div>
  );
}