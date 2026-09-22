import { DecimalPipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';

import { UserTotal } from './usage.models';
import { UsageService } from './usage.service';

/**
 * Owns its own fetch, unlike SummaryPanel: nothing else in the app needs this
 * data, so there is no reason to lift it into the parent.
 */
@Component({
  selector: 'app-top-users-panel',
  imports: [DecimalPipe],
  templateUrl: './top-users-panel.html',
  styleUrl: './top-users-panel.css',
})
export class TopUsersPanel implements OnInit {
  private readonly usage = inject(UsageService);

  readonly rows = signal<UserTotal[]>([]);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.error.set(null);

    this.usage.getTopUsers().subscribe({
      next: (rows) => {
        this.rows.set(rows);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Could not load top users.');
        this.loading.set(false);
      },
    });
  }
}
