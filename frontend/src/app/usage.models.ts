// Mirrors the Pydantic response models in backend/schemas.py.

export interface UsageRecord {
  id: number;
  user_name: string;
  team: string;
  tool: string;
  cost: string; // DECIMAL arrives as a string so money never becomes a float
  tokens: number;
  used_on: string; // ISO date, e.g. "2026-09-21"
}

export interface TeamSummary {
  team: string;
  total_tokens: number;
  total_cost: string;
  record_count: number;
}

export interface NewUsageRecord {
  user_name: string;
  team: string;
  tool: string;
  tokens: number;
  cost: string;
  used_on: string;
}
