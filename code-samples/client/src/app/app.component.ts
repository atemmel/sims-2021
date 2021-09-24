import { Component, OnInit } from '@angular/core';
import { NgModule } from '@angular/core';
import { WebSocketService } from './web-socket.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {
  title = 'chatbot';

  constructor(private webSocketService: WebSocketService) {}

  ngOnInit() {
    this.webSocketService.listen('my event').subscribe((data) => {
      console.log(data)
    });
  }

  sendMessage(data: string) {
    console.log("Sending message: ", data)
    this.webSocketService.emit('event', data);
  }
}
