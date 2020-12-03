import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-suota-list',
  templateUrl: './suota-list.component.html',
  styleUrls: ['./suota-list.component.scss']
})
export class SuotaListComponent implements OnInit {

  firmware_ptr : number = 0;
  chunk_sent   : number = 0;
  position     : number = 0;


  constructor() { }

  ngOnInit() {
  }

  scanDevices() {




  }

  
  connect_to_peer() {

    let name = "";
    let device;

    // Update GUI to match current activity
    // document.getElementById("connect_card").style.display = "none";
    // document.getElementById("progress_card").style.display = "none";
    // document.getElementById("dropfile_card").style.display = "none";
    // var textarea = document.getElementById('log');
    // textarea.value = "";

    // Set BLE scan filters
    // let options = {
    //     filters: [
    //       {services: [SPOTAR_SERVICE]}
    //     ],
    //     optionalServices: [SPOTAR_SERVICE]
    //   }
    
    // Try to connect to a BLE device
    // try {
    //   console.log('Requesting Bluetooth Device...');

    //   device  = await navigator.bluetooth.requestDevice(options);
    //   device.addEventListener('gattserverdisconnected', this.onDisconnected);
     
    //   name = device.name;
    //   log("Connected to ["+name+"]");

    //   log('Connecting to GATT Server...');
    //   server = await device.gatt.connect();
      
    //   log('Mapping SUotA Service...');
    //   const spotar_service = await server.getPrimaryService(SPOTAR_SERVICE);

    //   log(' Getting SPOTA_SERV_STATUS Characteristic...');
    //   spotar_serv_status = await spotar_service.getCharacteristic(SPOTA_SERV_STATUS);
    
    //   log('Subscribing to SPOTA_SERV_STATUS notifications ...');
    //   await spotar_serv_status.startNotifications();
    //   spotar_serv_status.addEventListener('characteristicvaluechanged', incomingData);

    //   log(' Getting SPOTA_MEM_DEV Characteristic...');
    //   spotar_mem_dev = await spotar_service.getCharacteristic(SPOTA_MEM_DEV);
    
    //   log(' Getting SPOTA_GPIOMAP Characteristic...');
    //   spotar_gpiomap = await spotar_service.getCharacteristic(SPOTA_GPIOMAP);
    
    //   log(' Getting SPOTA_MEM_INFO Characteristic...');
    //   spotar_mem_info = await spotar_service.getCharacteristic(SPOTA_MEM_INFO);

    //   log(' Getting SPOTA_PATCH_LEN Characteristic...');
    //   spotar_patch_len = await spotar_service.getCharacteristic(SPOTA_PATCH_LEN);
    
    //   log(' Getting SPOTA_PATCH_DATA Characteristic...');
    //   spotar_patch_data = await spotar_service.getCharacteristic(SPOTA_PATCH_DATA);
    
    //   log(' Getting SPOTA_MTU Characteristic...');
    //   spotar_mtu_size = await spotar_service.getCharacteristic(SPOTA_MTU);
      
    //   let spotar_mtu_value = await spotar_mtu_size.readValue();

    //   CHUNK_SIZE = (spotar_mtu_value.getUint8(0) + 256*spotar_mtu_value.getUint8(1))/4;

    //   BLOCK_SIZE = CHUNK_SIZE * CHUNK_PER_BLOCK;
    //   log("MTU value " + CHUNK_SIZE);

    //   // Initialize SUotA
    //   await spotar_mem_dev.writeValue(new Uint8Array(FLASH_CMD)); 
    //   //await spotar_gpiomap.writeValue(new Uint8Array(GPIO_CMD));
    //   log("Write patch_len: " + BLOCK_SIZE);
    //   await spotar_patch_len.writeValue(Uint8Array.of(BLOCK_SIZE & 0xFF ,(BLOCK_SIZE/256) & 0xFF));
      
    //   log('Ready to communicate.');

    //   // Update GUI to show that we are ready to receive a file
    //   document.getElementById("dropfile_card").style.display = "inline";
      
    // } catch(error) {
    //   log('Failed: ' + error);
    //   document.getElementById("refresh_card").style.display = "inline";
    //   document.getElementById("settings_icon").style.display = "none";
    //   document.getElementById("info_icon").style.display = "none";
    // }
  }
}
