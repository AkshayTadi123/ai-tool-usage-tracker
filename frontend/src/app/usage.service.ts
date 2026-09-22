import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { NewUsageRecord, TeamSummary, UsageRecord } from './usage.models';

const API_BASE = 'http://localhost:8000';

/**
 * Every HTTP call lives here. Components inject this and consume the
 * Observables it returns; they never touch HttpClient directly.
 */
@Injectable({ providedIn: 'root' })
export class UsageService {
  private readonly http = inject(HttpClient);

  getRecords(team: string | null, limit = 50, offset = 0): Observable<UsageRecord[]> {
    let params = new HttpParams().set('limit', limit).set('offset', offset);
    if (team) {
      params = params.set('team', team);
    }
    return this.http.get<UsageRecord[]>(`${API_BASE}/records`, { params });
  }

  getSummary(): Observable<TeamSummary[]> {
    return this.http.get<TeamSummary[]>(`${API_BASE}/summary`);
  }

  createRecord(record: NewUsageRecord): Observable<UsageRecord> {
    return this.http.post<UsageRecord>(`${API_BASE}/records`, record);
  }
}
