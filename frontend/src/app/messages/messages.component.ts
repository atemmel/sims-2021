import { Component, OnInit } from '@angular/core';

import { MessageService } from '../message.service';
import { Who } from '../who';

@Component({
  selector: 'app-messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.css']
})
export class MessagesComponent implements OnInit {

  // Make the enum Who available for MessageComponent
  // used in message.component.html
  public Who = Who;

  constructor(public messageService: MessageService) { }

  ngOnInit(): void {

  }
}
