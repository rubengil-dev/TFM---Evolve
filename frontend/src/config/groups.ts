/** Groups shown in the result, always the same: blood test groups and habit groups. */

export type GroupId =
  | 'minerals' | 'sugar' | 'red_cells' | 'defences' | 'liver' | 'kidney' | 'weight' | 'other'
  | 'smoking' | 'exercise' | 'sitting' | 'sleep'

export type Group = { id: GroupId; label: string }

// Model variables behind each group are decided in the backend (app.py)
export const BLOOD_GROUPS: Group[] = [
  { id: 'minerals',  label: 'Vitaminas y minerales' },
  { id: 'sugar',     label: 'Azúcar' },
  { id: 'red_cells', label: 'Glóbulos rojos' },
  { id: 'defences',  label: 'Defensas' },
  { id: 'liver',     label: 'Hígado' },
  { id: 'kidney',    label: 'Riñón' },
  { id: 'weight',    label: 'Peso' },
  { id: 'other',     label: 'Otros' },
]

export const HABIT_GROUPS: Group[] = [
  { id: 'smoking',  label: 'Tabaco' },
  { id: 'exercise', label: 'Ejercicio' },
  { id: 'sitting',  label: 'Horas sentado' },
  { id: 'sleep',    label: 'Sueño' },
]
