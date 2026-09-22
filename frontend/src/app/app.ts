import { Component, OnInit, ViewChild, computed, inject, signal } from '@angular/core';

import { AddRecordForm } from './add-record-form';
import { RecordsTable } from './records-table';
import { SummaryPanel } from './summary-panel';
import { TeamSummary } from './usage.models';
import { UsageService } from './usage.service';

@Component({
  selector: 'app-root',
  imports: [AddRecordForm, RecordsTable, SummaryPanel],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  private readonly usage = inject(UsageService);

  /** Gives us a handle on the child so we can refresh it after a create. */
  @ViewChild(RecordsTable) private table?: RecordsTable;

  readonly summary = signal<TeamSummary[]>([]);
  readonly summaryLoading = signal(false);
  readonly summaryError = signal<string | null>(null);
  readonly selectedTeam = signal<string | null>(null);

  /** Derived, not stored: /summary has one row per team, so it is the team list. */
  readonly teams = computed(() => this.summary().map((row) => row.team));

  ngOnInit(): void {
    this.loadSummary();
  }

  loadSummary(): void {
    this.summaryLoading.set(true);
    this.summaryError.set(null);

    this.usage.getSummary().subscribe({
      next: (rows) => {
        this.summary.set(rows);
        this.summaryLoading.set(false);
      },
      error: () => {
        this.summaryError.set('Could not load the summary.');
        this.summaryLoading.set(false);
      },
    });
  }

  onTeamChange(value: string): void {
    this.selectedTeam.set(value || null);
  }

  onCreated(): void {
    // A new record changes both the list and the totals.
    this.table?.load();
    this.loadSummary();
  }
}
