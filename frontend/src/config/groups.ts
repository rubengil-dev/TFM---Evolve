/** Groups shown in the result, always the same: blood test groups and habit groups. */

export type GroupId =
  | 'minerals' | 'sugar' | 'heart' | 'red_cells' | 'defences' | 'liver' | 'kidney' | 'weight'
  | 'smoking' | 'exercise' | 'sitting' | 'sleep'

export type Group = { id: GroupId; label: string }

// Model variables behind each group are decided in the backend
export const BLOOD_GROUPS: Group[] = [
  { id: 'minerals',  label: 'Vitaminas y minerales' },
  { id: 'sugar',     label: 'Azúcar' },
  { id: 'heart',     label: 'Corazón' },
  { id: 'red_cells', label: 'Glóbulos rojos' },
  { id: 'defences',  label: 'Defensas' },
  { id: 'liver',     label: 'Hígado' },
  { id: 'kidney',    label: 'Riñón' },
  { id: 'weight',    label: 'Peso' },
]

export const HABIT_GROUPS: Group[] = [
  { id: 'smoking',  label: 'Tabaco' },
  { id: 'exercise', label: 'Ejercicio' },
  { id: 'sitting',  label: 'Horas sentado' },
  { id: 'sleep',    label: 'Sueño' },
]
