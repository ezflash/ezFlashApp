import { Injectable } from '@angular/core';
import { Socket, SocketIoConfig } from 'ngx-socket-io';
import { map, filter, switchMap } from 'rxjs/operators';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root',
})
export class BackendSocketService {

  socket: Socket;

  constructor() {

    let url  = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port ;

    const socketIoConfig: SocketIoConfig = { url };
    this.socket = new Socket(socketIoConfig);
    this.socket.connect();
  
  }


  query(query: string ,msg: Object) : Observable<Object> {
    this.socket.emit(query, msg);
    return(this.socket.fromEvent(query));
  }

  sendMessage(topic: string,msg: Object) {
    this.socket.emit(topic, msg);
  }
  
  // getMessage() {
  //   return this.socket.fromEvent("message").map(data => data.msg);
  // }
  
  getMessage(msg: string) {
    return this.socket
        .fromEvent(msg);
}
}
