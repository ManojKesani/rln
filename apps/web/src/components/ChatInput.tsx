/**
 * S-007: Text box and send
 * Imports: (props)
 * Exports: ChatInput
 */
import { useState } from "react";

type Props = { onSend: (text: string) => void; disabled: boolean };

export function ChatInput({ onSend, disabled }: Props) {
  const [text, setText] = useState("");
  const send = () => {
    const v = text.trim();
    if (!v || disabled) return;
    onSend(v);
    setText("");
  };
  return (
    <div className="flex gap-2">
      <input className="flex-1" placeholder="Ask something..." value={text} disabled={disabled}
             onChange={(e) => setText(e.target.value)}
             onKeyDown={(e) => { if (e.key === "Enter") send(); }} />
      <button className="pri" onClick={send} disabled={disabled}>Send</button>
    </div>
  );
}