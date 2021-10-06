import { Injectable } from '@angular/core';
import { io } from 'socket.io-client';
import { Observable } from 'rxjs';
import { Message } from './message';
import { Who } from './who';
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

  // Called when messages are received from the bot, gives the user a response
  listen(eventName: string) {
    return new Observable((subscriber) => {
      this.socket.on(eventName, (data: any) => {

        var message = new Message();
        message.who = Who.Bot;
        message.text = data.response.text;
        message.articles = data.response.articles;

        this.messageService.add(message);
        subscriber.next(data);
      })
    });
  }

  // Sends data to the server, called from sendMessage() in
  // app.component.html when the user clicks on the send button
  emit(eventName: string, data: any) {

    var message = new Message();
    message.who = Who.Customer;
    message.text = data;

    this.messageService.add(message);
    this.socket.emit(eventName, data);
  }
}
