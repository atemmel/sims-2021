import { Component, OnInit } from '@angular/core';
import { MessageService } from '../message.service';
import { ArticleMessageComponent } from '../article-message/article-message.component';
import { Article } from '../article';
import { Office } from '../office';

@Component({
  selector: 'app-messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.css']
})
export class MessagesComponent implements OnInit {

  constructor(public messageService: MessageService) { }

  ngOnInit(): void {}

  instanceOfArticle(additional: any) {
    if (!Array.isArray(additional)) return false;
    return additional[0] instanceof Article;
  }

  instanceOfOffice(additional: any) {
    if (!Array.isArray(additional)) return false;
    return additional[0] instanceof Office;
  }
}
