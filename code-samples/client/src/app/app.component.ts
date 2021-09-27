import { Component, OnInit } from '@angular/core';
import { NgModule } from '@angular/core';
import { WebSocketService } from './web-socket.service';
import { MessagesComponent } from './messages/messages.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {
  title = 'chatbot';

  constructor(private webSocketService: WebSocketService) {}

  ngOnInit() {
    this.webSocketService.listen('event').subscribe((data) => {
      console.log(data)
    });
  }

  // Called when the user clicks on the send button in app.component.html.
  // Sends the users input to the server
  sendMessage(data: string) {
    this.webSocketService.emit('event', data);
  }
}
