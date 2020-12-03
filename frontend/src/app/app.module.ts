import { BrowserModule } from '@angular/platform-browser';
import { Injectable, NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './material';
import { PageNotFoundComponentComponent } from './page-not-found-component/page-not-found-component.component';
import { FlashProgListComponent } from './flashProg/flash-prog-list/flash-prog-list.component';
import { SuotaListComponent } from './suota/suota-list/suota-list.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FlashProgDeviceComponent,PizzaPartyComponent } from './flashProg/flash-prog-device/flash-prog-device.component';
import { FlashConfirmDialogComponent } from './flashProg/flash-confirm-dialog/flash-confirm-dialog.component';
import { DeviceNamePipe } from './device-name.pipe';

import { NgxFileDropModule } from 'ngx-file-drop';
import { UpdateConfirmDialogComponent } from './update-confirm-dialog/update-confirm-dialog.component';

 
@NgModule({
  declarations: [
    AppComponent,
    PageNotFoundComponentComponent,
    FlashProgListComponent,
    SuotaListComponent,
    FlashProgDeviceComponent,
    DeviceNamePipe,
    FlashConfirmDialogComponent,
    PizzaPartyComponent,
    UpdateConfirmDialogComponent
  ],
  imports: [
    FlexLayoutModule ,
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    NgxFileDropModule,
  ],
  providers: [],
  entryComponents: [
    FlashConfirmDialogComponent,
    UpdateConfirmDialogComponent,
    PizzaPartyComponent
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
