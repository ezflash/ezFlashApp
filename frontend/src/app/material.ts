import {NgModule} from '@angular/core';

import {MatButtonModule} from '@angular/material/button';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatMenuModule} from '@angular/material/menu';
import {MatIconModule} from '@angular/material/icon';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatListModule} from '@angular/material/list';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatSelectModule} from '@angular/material/select';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatCardModule} from '@angular/material/card';
import {MatTooltipModule} from '@angular/material/tooltip';
import {MatChipsModule} from '@angular/material/chips';
import {MatDialogModule} from '@angular/material/dialog';


let importExport = [
  MatGridListModule,
  MatButtonModule, 
  MatCheckboxModule, 
  MatToolbarModule, 
  MatMenuModule, 
  MatIconModule,
  MatProgressBarModule,
  MatSnackBarModule,
  MatListModule,
  MatSidenavModule,
  MatFormFieldModule,
  MatSelectModule,
  MatCardModule,
  MatTooltipModule,
  MatChipsModule,
  MatDialogModule,
];


@NgModule({
  imports: importExport,
  exports: importExport,
})
export class MaterialModule { }