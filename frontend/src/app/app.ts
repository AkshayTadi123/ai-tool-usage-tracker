import { Component, OnInit, ViewChild, inject } from '@angular/core';

import { AddRecordForm } from './add-record-form';
import { RecordsTable } from './records-table';
import { UsageService } from './usage.service';

@Component({
  selector: 'app-root',
  imports: [AddRecordForm, RecordsTable],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  private readonly usage = inject(UsageService);

  /** Gives us a handle on the child so we can refresh it after a create. */
  @ViewChild(RecordsTable) private table?: RecordsTable;

  teams: string[] = [];
  selectedTeam: string | null = null;

  ngOnInit(): void {
    // /summary already returns one row per team, so it doubles as the team list.
    this.usage.getSummary().subscribe({
      next: (rows) => (this.teams = rows.map((row) => row.team)),
      error: () => (this.teams = []),
    });
  }

  onTeamChange(value: string): void {
    this.selectedTeam = value || null;
  }

  onCreated(): void {
    this.table?.load();
  }
}
