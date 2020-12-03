import { Component } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'app-flash-confirm-dialog',
  templateUrl: './flash-confirm-dialog.component.html',
  styleUrls: ['./flash-confirm-dialog.component.scss']
})
export class FlashConfirmDialogComponent {

  constructor(public dialogRef: MatDialogRef<FlashConfirmDialogComponent>) { }


}



