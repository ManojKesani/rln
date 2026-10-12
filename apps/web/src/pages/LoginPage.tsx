/**
 * S-007: Login form
 * Imports: hooks.useLogin
 * Exports: LoginPage
 */
import { useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useLogin } from "@/api/hooks";

export function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const login = useLogin();
  const navigate = useNavigate();
  const qc = useQueryClient();

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    login.mutate(
      { username, password },
      {
        onSuccess: async () => {
          await qc.invalidateQueries({ queryKey: ["me"] });
          navigate("/", { replace: true });
        },
      },
    );
  };

  return (
    <div className="flex h-full items-center justify-center">
      <form onSubmit={submit} className="w-72 rounded-2xl border border-line bg-p p-5">
        <h1 className="mb-1 font-mono text-lg tracking-widest text-acc">✦ TRILLIAN</h1>
        <p className="mb-4 text-xs text-mut">mostly harmless</p>
        <input className="mb-2 w-full" placeholder="username" autoComplete="username"
               value={username} onChange={(e) => setUsername(e.target.value)} />
        <input className="mb-3 w-full" type="password" placeholder="password" autoComplete="current-password"
               value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="pri w-full" type="submit" disabled={login.isPending}>Log in</button>
        {login.isError && <p className="mt-2 text-xs text-bad">{login.error.message}</p>}
      </form>
    </div>
  );
}