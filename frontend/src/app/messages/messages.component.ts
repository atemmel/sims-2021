import { Component, OnInit } from '@angular/core';
import { MessageService } from '../message.service';
import { Article } from '../article';
import { Office } from '../botMessage';
@Component({
  selector: 'app-messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.css']
})
export class MessagesComponent implements OnInit {

  // Make the enum Who available for MessageComponent
  // used in message.component.html

  constructor(public messageService: MessageService) { }

  ngOnInit(): void {

  }

  instanceOfArticle(additional: any) {
    if (!Array.isArray(additional)) return false;
    console.log(additional[0] instanceof Article);
    return additional[0] instanceof Article;
  }

  instanceOfOffice(additional: any) {
    if (!Array.isArray(additional)) return false;
    console.log(additional[0] instanceof Office);
    return additional[0] instanceof Office;
  }

  instanceOfContacts(additional: any) {
    // TODO: Implement contacts
  }
}
