import { Injectable } from '@angular/core';

import { BotMessage } from './botMessage';
import { CustomerMessage } from './customerMessage';

@Injectable({
  providedIn: 'root'
})

export class MessageService {

  messages: any[] = [];

  addBotMessage(message: BotMessage) {
    this.messages.push(message);
  }

  addCustomerMessage(message: CustomerMessage) {
    this.messages.push(message);
  }

  constructor() { }
}
