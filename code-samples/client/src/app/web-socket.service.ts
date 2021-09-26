import { Injectable } from '@angular/core';
import { io } from 'socket.io-client';
import { Observable } from 'rxjs';
import { Message } from './message';
import { MessageService } from './message.service'

@Injectable({
  providedIn: 'root'
})

export class WebSocketService {

  socket: any;
  readonly uri: string = "ws://localhost:80";

  constructor(private messageService: MessageService) {
    this.socket = io(this.uri);
  }

  listen(eventName: string) {
    return new Observable((subscriber) => {
      this.socket.on(eventName, (data: any) => {

        var message = new Message();
        message.who = 'Bot: ';
        message.text = data.text;
        message.url = data.url;

        this.messageService.add(message);
        subscriber.next(data);
      })
    });
  }

  emit(eventName: string, data: any) {

    var message = new Message();
    message.who = 'You: ';
    message.text = data;

    this.messageService.add(message);
    this.socket.emit(eventName, data);
  }
}
