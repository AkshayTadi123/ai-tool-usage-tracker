import { DecimalPipe } from '@angular/common';
import { Component, Input, OnChanges, inject, signal } from '@angular/core';

import { UsageRecord } from './usage.models';
import { UsageService } from './usage.service';

@Component({
  selector: 'app-records-table',
  imports: [DecimalPipe],
  templateUrl: './records-table.html',
  styleUrl: './records-table.css',
})
export class RecordsTable implements OnChanges {
  /** null means "all teams". */
  @Input() team: string | null = null;

  private readonly usage = inject(UsageService);

  // Signals, not plain fields: this app is zoneless, so Angular only re-renders
  // when a signal it read during rendering is written to.
  readonly records = signal<UsageRecord[]>([]);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);

  /** Fires on the initial binding and whenever the parent changes `team`. */
  ngOnChanges(): void {
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.error.set(null);

    this.usage.getRecords(this.team).subscribe({
      next: (records) => {
        this.records.set(records);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Could not reach the API on :8000.');
        this.loading.set(false);
      },
    });
  }
}
