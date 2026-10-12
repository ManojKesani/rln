/**
 * S-007: Redirects to /login if useMe fails
 * Imports: hooks.useMe
 * Exports: RequireAuth
 */
import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useMe } from "@/api/hooks";

export function RequireAuth({ children }: { children: ReactNode }) {
  const me = useMe();
  if (me.isPending) return <div className="p-6 text-mut">Loading…</div>;
  if (me.isError) return <Navigate to="/login" replace />;
  return <>{children}</>;
}