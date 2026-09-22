import { DecimalPipe } from '@angular/common';
import { Component, Input } from '@angular/core';

import { TeamSummary } from './usage.models';

/** Presentational: the parent owns the data, this just renders it. */
@Component({
  selector: 'app-summary-panel',
  imports: [DecimalPipe],
  templateUrl: './summary-panel.html',
  styleUrl: './summary-panel.css',
})
export class SummaryPanel {
  @Input() rows: TeamSummary[] = [];
  @Input() loading = false;
  @Input() error: string | null = null;
}
