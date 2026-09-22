import { DecimalPipe } from '@angular/common';
import { Component, Input, OnChanges } from '@angular/core';
import { inject } from '@angular/core';

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

  records: UsageRecord[] = [];
  loading = false;
  error: string | null = null;

  /** Fires on the initial binding and whenever the parent changes `team`. */
  ngOnChanges(): void {
    this.load();
  }

  load(): void {
    this.loading = true;
    this.error = null;

    this.usage.getRecords(this.team).subscribe({
      next: (records) => {
        this.records = records;
        this.loading = false;
      },
      error: () => {
        this.error = 'Could not reach the API on :8000.';
        this.loading = false;
      },
    });
  }
}
