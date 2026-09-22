import { DecimalPipe } from '@angular/common';
import { Component, Input, OnChanges, computed, inject, signal } from '@angular/core';

import { UsageRecord } from './usage.models';
import { UsageService } from './usage.service';

const PAGE_SIZE = 20;

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

  readonly pageSize = PAGE_SIZE;

  // Signals, not plain fields: this app is zoneless, so Angular only re-renders
  // when a signal it read during rendering is written to.
  readonly records = signal<UsageRecord[]>([]);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);
  readonly offset = signal(0);

  readonly page = computed(() => this.offset() / PAGE_SIZE + 1);
  readonly hasPrev = computed(() => this.offset() > 0);
  /** No total count from the API, so a full page means "there may be more". */
  readonly hasNext = computed(() => this.records().length === PAGE_SIZE);

  /** Fires on the initial binding and whenever the parent changes `team`. */
  ngOnChanges(): void {
    this.offset.set(0); // a new filter means starting from page 1
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.error.set(null);

    this.usage.getRecords(this.team, PAGE_SIZE, this.offset()).subscribe({
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

  nextPage(): void {
    this.offset.update((value) => value + PAGE_SIZE);
    this.load();
  }

  prevPage(): void {
    this.offset.update((value) => Math.max(0, value - PAGE_SIZE));
    this.load();
  }
}
