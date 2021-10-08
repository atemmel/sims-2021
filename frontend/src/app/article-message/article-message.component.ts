import { Component, OnInit, Input } from '@angular/core';
import { BotMessageContents } from '../botMessage';
import { Article } from '../article';

@Component({
  selector: 'app-article-message',
  templateUrl: './article-message.component.html',
  styleUrls: ['./article-message.component.css', '../messages/messages.component.css']
})
export class ArticleMessageComponent implements OnInit {

  @Input() botMessageContents: BotMessageContents;

  constructor() { }

  ngOnInit(): void {
  }

}
