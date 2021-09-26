import { Injectable } from '@angular/core';

import { Message } from './message';

@Injectable({
  providedIn: 'root'
})

export class MessageService {

  messages: Message[] = [];

  add(message: Message) {
    this.messages.push(message);
  }

  constructor() { }
}
