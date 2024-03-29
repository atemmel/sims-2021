import { Injectable } from '@angular/core';
import { io } from 'socket.io-client';
import { Observable } from 'rxjs';
import { BotMessage, BotMessageContents, buildContents } from './botMessage';
import { CustomerMessage } from './customerMessage';
import { MessageService } from './message.service'
import { Office } from './office';
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

		  // A farmers solution, this is
		  if(message.contents[message.contents.length - 1].text
			 === "Hi, I can help you find articles, office information and more. \n") {
			message.contents.push({
				"text": "For example: \"Show me articles related to healthcare\"",
				"additional": null,
				"italic": true,
			});
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
