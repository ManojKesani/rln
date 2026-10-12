/**
 * S-008: Provider and model dropdowns
 * Imports: hooks.useModels
 * Exports: ModelPicker
 */
import { useModels } from "@/api/hooks";

type Props = {
  provider: string;
  model: string;
  onChange: (provider: string, model: string) => void;
};

export function ModelPicker({ provider, model, onChange }: Props) {
  const { data } = useModels();
  const available = data?.providers.filter((p) => p.available) ?? [];
  const models = available.find((p) => p.name === provider)?.models ?? [];
  // keep the current value selectable even if the list hasn't loaded or doesn't include it
  const options = models.some((m) => m.id === model) ? models : [{ id: model, name: model }, ...models];

  return (
    <div className="flex gap-2">
      <select value={provider}
              onChange={(e) => {
                const first = available.find((p) => p.name === e.target.value)?.models[0];
                onChange(e.target.value, first?.id ?? model);
              }}>
        {!available.some((p) => p.name === provider) && <option value={provider}>{provider}</option>}
        {available.map((p) => <option key={p.name} value={p.name}>{p.name}</option>)}
      </select>
      <select className="min-w-0 max-w-[260px]" value={model} onChange={(e) => onChange(provider, e.target.value)}>
        {options.map((m) => <option key={m.id} value={m.id}>{m.id}</option>)}
      </select>
    </div>
  );
}