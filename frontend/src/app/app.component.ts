import { Component, OnInit, AfterViewInit } from '@angular/core';
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
      this.scrollDown();
    });
  }

  // Called when the user clicks on the send button in app.component.html.
  // Sends the users input to the server
  sendMessage(input: any) {
    let text = input.value.trim();
    input.value = "";

    // Do nothing if the input field is empty when the user
    // clicks on enter or the send button
    if (text === "") {
      return;
    };

    // Send the string to the middleend
    this.webSocketService.emit('event', text);
    this.scrollDown();
  }

  scrollDown() {
    setTimeout(() => {
      let chatWindowElement = Array.from(document.getElementsByClassName("chat-window") as HTMLCollectionOf<HTMLElement>);
      chatWindowElement[0].scrollTop = chatWindowElement[0].scrollHeight;
    });
  }
}
