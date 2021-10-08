import { Component, OnInit, Input } from '@angular/core';
import { BotMessageContents } from '../botMessage';
import { Office } from '../office';

@Component({
  selector: 'app-office-message',
  templateUrl: './office-message.component.html',
  styleUrls: ['./office-message.component.css', '../messages/messages.component.css']
})
export class OfficeMessageComponent implements OnInit {

  @Input() botMessageContents: BotMessageContents;

  constructor() { }

  ngOnInit(): void {
  }

}
