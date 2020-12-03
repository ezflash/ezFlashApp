import { Component,OnInit } from '@angular/core';

import { BackendSocketService } from './backend-socket.service';
import { UpdateConfirmDialogComponent }  from './update-confirm-dialog/update-confirm-dialog.component';
import { MatDialog,MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'SmartBond made Easy';
  version_string : string;
  update_available : boolean  = false;

  connected : boolean = false;

  constructor(private backendSocketService: BackendSocketService,
              public dialog: MatDialog) { }


  ngOnInit() {
    this.backendSocketService.query('backendVersion',{}).subscribe( (resp : any) => {
      this.version_string = resp.version;
      this.update_available = resp.update;
    });

    this.backendSocketService.getMessage('connect').subscribe( event => {
      this.connected = true;

    });
    this.backendSocketService.getMessage('disconnect').subscribe( event => {
      this.connected = false;

    });
    
  }

  triggerUpdate() {
    const dialogRef = this.dialog.open(UpdateConfirmDialogComponent, {
      width: '250px'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result === true) {
        this.backendSocketService.sendMessage('appUpdate',{});

      }
    });  
  }
}
