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
  sendMessage(input: any) {

    // Remove whitespace before and after the input string
    let text = input.value.trim();

    // Do nothing if the input field is empty when the user
    // clicks on enter or the send button
    if (text === "") {
      text = "";
      return;
    };

    // Send the string to the middleend
    this.webSocketService.emit('event', text);

    // Clear the input field
    input.value = "";
  }
}
