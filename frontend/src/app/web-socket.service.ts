import { Injectable } from '@angular/core';
import { io } from 'socket.io-client';
import { Observable } from 'rxjs';
import { BotMessage, BotMessageContents, Office, VisitAddress, ContactInfo, PostAddress, buildContents } from './botMessage';
  import { CustomerMessage } from './customerMessage';
  import { MessageService } from './message.service'
  import { Article } from './article';

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

          let message = new BotMessage();

          for (let response of data.response) {
            message.contents.push(buildContents(response));
          }

          this.messageService.addBotMessage(message);
          subscriber.next(data);
        })
      });
    }

    // Sends data to the server, called from sendMessage() in
    // app.component.html when the user clicks on the send button
    emit(eventName: string, data: any) {
      var message = new CustomerMessage();
      message.text = data;

      this.messageService.addCustomerMessage(message);
      this.socket.emit(eventName, data);
    }
  }
