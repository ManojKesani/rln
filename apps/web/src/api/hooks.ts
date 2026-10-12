/**
 * S-007: TanStack Query hooks
 * Imports: @tanstack/react-query, client
 * Exports: useLogin, useMe, useConversations, useMessages, useCreateConversation
 */
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "./client";
import type { components } from "./schema";

type S = components["schemas"];

export const useLogin = () =>
  useMutation({
    mutationFn: (b: S["LoginRequest"]) => api.post<{ ok: boolean }>("/api/auth/login", b),
  });

export const useMe = () =>
  useQuery({ queryKey: ["me"], queryFn: () => api.get<S["MeResponse"]>("/api/auth/me"), retry: false });

export const useConversations = () =>
  useQuery({ queryKey: ["conversations"], queryFn: () => api.get<S["ConversationOut"][]>("/api/conversations") });

export const useMessages = (id: string | null) =>
  useQuery({
    queryKey: ["messages", id],
    queryFn: () => api.get<S["MessageOut"][]>(`/api/conversations/${id}/messages`),
    enabled: !!id,
  });

export const useModels = () =>
  useQuery({ queryKey: ["models"], queryFn: () => api.get<S["ModelsResponse"]>("/api/models"), staleTime: 600_000 });

export const useCreateConversation = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (b: S["ConversationCreate"]) => api.post<S["ConversationCreated"]>("/api/conversations", b),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["conversations"] }),
  });
};

export const useUsage = (id: string | null) =>
  useQuery({
    queryKey: ["usage", id],
    queryFn: () => api.get<S["ConversationUsage"]>(`/api/conversations/${id}/usage`),
    enabled: !!id,
  });