import { Component, OnInit } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'app-update-confirm-dialog',
  templateUrl: './update-confirm-dialog.component.html',
  styleUrls: ['./update-confirm-dialog.component.scss']
})
export class UpdateConfirmDialogComponent {

  constructor(public dialogRef: MatDialogRef<UpdateConfirmDialogComponent>) { 

  }

}
