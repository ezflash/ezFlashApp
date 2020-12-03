import { Component, OnInit, OnDestroy, Inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { FlashProgApiService } from '../flash-prog-api.service';
import { FlashConfirmDialogComponent}  from '../flash-confirm-dialog/flash-confirm-dialog.component';
import { DeviceNamePipe } from '../../device-name.pipe';
import { Subscription } from 'rxjs';

import { NgxFileDropEntry, FileSystemFileEntry, FileSystemDirectoryEntry } from 'ngx-file-drop';

import { MatDialog,MAT_DIALOG_DATA } from '@angular/material/dialog';
import {MatSnackBar} from '@angular/material/snack-bar';


@Component({
  selector: 'app-flash-prog-device',
  templateUrl: './flash-prog-device.component.html',
  styleUrls: ['./flash-prog-device.component.scss']
})
export class FlashProgDeviceComponent implements OnInit, OnDestroy {
  subArray : Subscription[] = [];
  deviceId : string;
  deviceIsRunning: boolean = false;
  flashDevice : string = "Not probed";
  deviceType : string;
  deviceLoaded : Boolean = false;
  flashInProgress : Boolean = false;

  constructor(private flashProgApiService: FlashProgApiService,
              private route: ActivatedRoute,
              public dialog: MatDialog,
              private _snackBar: MatSnackBar) { }

  ngOnInit() {
    this.subArray.push(this.route.paramMap.subscribe(params => {
      this.deviceId = params.get('id');
      if (this.deviceId) {

        this.deviceLoaded = false;
        this.subArray.push(this.flashProgApiService.browseDevice(this.deviceId).subscribe ( (res: any) => {
          // console.log(res);
          this.deviceType = res.deviceType;
          this.deviceLoaded = true;
          this.flashDevice = res.flashType;
          this.deviceIsRunning = false;

        }));

        this.subArray.push(this.flashProgApiService.deviceStateSub().subscribe ( (res: any) => {
          // console.log(res);
          this.deviceIsRunning = res.deviceIsRunning;

        }));
      }
    }));
  }

  ngOnDestroy() {

    for ( const sub of this.subArray) {
      sub.unsubscribe();
    }
  }

  // Device management functions
  

  // file drag and drop
    public files: NgxFileDropEntry[] = [];
  
    public dropped(files: NgxFileDropEntry[]) {
      this.files = files;
      // for (const droppedFile of files) {
  
      //   // Is it a file?
      //   if (droppedFile.fileEntry.isFile) {
      //     const fileEntry = droppedFile.fileEntry as FileSystemFileEntry;
      //     console.log(fileEntry);
      //     fileEntry.file((file: File) => {
  
      //       // Here you can access the real file
      //       console.log(droppedFile.relativePath, file);
  
      //       /**
      //       // You could upload it like this:
      //       const formData = new FormData()
      //       formData.append('logo', file, relativePath)
  
      //       // Headers
      //       const headers = new HttpHeaders({
      //         'security-token': 'mytoken'
      //       })
  
      //       this.http.post('https://mybackend.com/api/upload/sanitize-and-save-logo', formData, { headers: headers, responseType: 'blob' })
      //       .subscribe(data => {
      //         // Sanitized logo returned from backend
      //       })
      //       **/
  
      //     });
      //   } else {
      //     // It was a directory (empty directories are added, otherwise only files)
      //     const fileEntry = droppedFile.fileEntry as FileSystemDirectoryEntry;
      //     console.log(droppedFile.relativePath, fileEntry);
      //   }
      // }
    }
  
    public fileOver(event){
      // console.log(event);
    }
  
    public fileLeave(event){
      // console.log(event);
    }

  // flash erase confirmation dialog
  programFlash(): void {
    
    if(this.files.length != 1) {
      console.log("myst be only one file");
    }

    if(this.files[0].fileEntry.isFile) {

      const fileEntry = this.files[0].fileEntry as FileSystemFileEntry;

      fileEntry.file((file: File) => {
        this.flashInProgress = true;
        this.subArray.push(this.flashProgApiService.programFlashDevice(this.deviceType,this.deviceId,file,fileEntry.name).subscribe ( (eraseStatus) => {
          this.flashInProgress = false;
        }));
      });
  

    } else {

      console.log("input is not a file");
    }

  }
  // flash erase confirmation dialog
  eraseFlashDialog(): void {
    const dialogRef = this.dialog.open(FlashConfirmDialogComponent, {
      width: '250px'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result === true) {
        this.flashInProgress = true;
        // console.log("erase in progress", this.flashInProgress);
        this.subArray.push( this.flashProgApiService.eraseFlashDevice(this.deviceType,this.deviceId).subscribe ( (eraseStatus) => {
          this.flashInProgress = false;
          // console.log("erase in progress", this.flashInProgress);
          this._snackBar.openFromComponent(PizzaPartyComponent, {
            duration: 2000,
          });
          
        }));
      }
    });
  }

  resetAndRun(deviceType: any,deviceId: any) {
    this.flashProgApiService.resetAndRun(deviceType,deviceId);
  }
  resetAndHalt(deviceType: any, deviceId: any) {
    this.flashProgApiService.resetAndHalt(deviceType,deviceId);
  }
}


@Component({
  selector: 'snack-bar-component-example-snack',
  templateUrl: 'snack-bar-component-example-snack.html',
  styles: [`
    .example-pizza-party {
      color: hotpink;
    }
  `],
})
export class PizzaPartyComponent {}