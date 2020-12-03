import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute,Router } from '@angular/router';


import { FlashProgApiService } from '../flash-prog-api.service';
import { Subscription } from 'rxjs';

import { FlashProgDeviceComponent } from '../flash-prog-device/flash-prog-device.component';

@Component({
  selector: 'app-flash-prog-list',
  templateUrl: './flash-prog-list.component.html',
  styleUrls: ['./flash-prog-list.component.scss']
})
export class FlashProgListComponent implements OnInit, OnDestroy {

  private deviceListSub : Subscription;

  devicesId : any;

  constructor(private flashProgApiService: FlashProgApiService,
    private route: ActivatedRoute,
    private router: Router) { }

  ngOnInit() {

    this.deviceListSub = this.flashProgApiService.listDevices().subscribe( (response: any) => {
      this.devicesId = response.resp ;

      // clear the route when the current id is not in the list
      if(this.route.snapshot.params.id) {
        for( const info of this.devicesId){
          if(info.deviceId == this.route.snapshot.params.id) {
            return;
          }
          console.log(info)
        }
        this.router.navigate(["flashprog"]);
      }
    });

  }

  ngOnDestroy() {
    this.deviceListSub.unsubscribe();
  }

  showDeviceInfo(device) {
    console.log(device);
    
  }

}
