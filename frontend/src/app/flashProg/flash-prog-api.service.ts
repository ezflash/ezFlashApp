import { Injectable } from '@angular/core';
import { Observable ,  of } from 'rxjs';

import { BackendSocketService } from '../backend-socket.service';


@Injectable({
  providedIn: 'root'
})
export class FlashProgApiService {

  constructor(private backendSocketService: BackendSocketService) { }


  deviceStateSub() : Observable<Object> {
    return(this.backendSocketService.getMessage('deviceStatus'));
  }

  resetAndRun(deviceType: string,deviceId: number) {
    console.log("Reset & Run");
    this.backendSocketService.sendMessage('resetAndRun',
      { 'deviceType' : deviceType,
        'deviceId'   : deviceId
    
    });
  }

  resetAndHalt(deviceType: string,deviceId: number) {
    this.backendSocketService.sendMessage('resetAndHalt',
      { 'deviceType' : deviceType,
        'deviceId'   : deviceId
    
    });
  }

  listDevices() : Observable<Object> {
    return(this.backendSocketService.query('getDeviceList',{ "cmd" : "getDeviceList" }));
  }

  browseDevice( deviceId : string) : Observable<Object> {
    return(this.backendSocketService.query('browseDevice',{ 
      "cmd"      : "browseDevice", 
      "deviceId" : deviceId
    }));
  }

  eraseFlashDevice(deviceType: string, deviceId : string) : Observable<Object> {
    return(this.backendSocketService.query('eraseFlashDevice',{ 
      "cmd"       : "eraseFlashDevice", 
      "deviceType": deviceType, 
      "deviceId"  : deviceId
    }));
  }

  programFlashDevice(deviceType: string, deviceId : string,file: any,fileName: string) : Observable<Object> {
    return(this.backendSocketService.query('programFlashDevice',{ 
      "cmd"       : "programFlashDevice", 
      "deviceType": deviceType, 
      "deviceId"  : deviceId,
      "fileName"  : fileName,
      "file"      : file 
    }));
  }

}
