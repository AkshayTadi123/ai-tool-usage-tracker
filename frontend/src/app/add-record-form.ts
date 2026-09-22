import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { UsageService } from './usage.service';

@Component({
  selector: 'app-add-record-form',
  imports: [ReactiveFormsModule],
  templateUrl: './add-record-form.html',
  styleUrl: './add-record-form.css',
})
export class AddRecordForm {
  @Input() teams: string[] = [];
  /** Tells the parent a record was created, so the table can refresh. */
  @Output() created = new EventEmitter<void>();

  private readonly usage = inject(UsageService);
  private readonly fb = inject(FormBuilder);

  readonly tools = ['Claude Code', 'GitHub Copilot', 'Cursor', 'ChatGPT'];

  submitting = false;
  error: string | null = null;

  // Validators mirror the Pydantic constraints in backend/schemas.py, so the
  // user gets feedback without a round trip. The server still validates.
  readonly form = this.fb.nonNullable.group({
    user_name: ['', Validators.required],
    team: ['', Validators.required],
    tool: [this.tools[0], Validators.required],
    tokens: [1000, [Validators.required, Validators.min(1)]],
    cost: ['0.10', Validators.required],
    used_on: [new Date().toISOString().slice(0, 10), Validators.required],
  });

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.submitting = true;
    this.error = null;

    this.usage.createRecord(this.form.getRawValue()).subscribe({
      next: () => {
        this.submitting = false;
        this.form.patchValue({ user_name: '' });
        this.created.emit();
      },
      error: (err) => {
        this.submitting = false;
        this.error =
          err.status === 422
            ? 'The API rejected this record (422). Check tokens and cost.'
            : 'Could not save the record.';
      },
    });
  }
}
