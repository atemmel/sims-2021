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
  placeholderText = "";
  showAttentionBubbleTimeout: any;
  closeAttentionBubbleTimeout: any;

  constructor(private webSocketService: WebSocketService) {}

  ngOnInit() {
    this.webSocketService.listen('event').subscribe((data) => {
      this.scrollDown();
    });
    this.placeholderText = this.createPlaceholderText();
  }

  ngAfterViewInit() {
    let attentionBubble = Array.from(document.getElementsByClassName("attention-bubble") as HTMLCollectionOf<HTMLElement>);

    this.showAttentionBubbleTimeout = setTimeout(() => {
      attentionBubble[0].style.display = "block";
      this.closeAttentionBubbleTimeout = setTimeout(()=> {
        attentionBubble[0].style.display = "none";
      }, 5000);
    }, 3000);
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

  createPlaceholderText() {
    let prospects = ["IoT", "Apps", "UX", "AI"];
    return "Try asking for solutions using " + prospects[Math.floor(Math.random() * prospects.length)];
  }

  showChatbotWindow() {
    let chatWindowElement = Array.from(document.getElementsByClassName("container") as HTMLCollectionOf<HTMLElement>);
    let chatButtonElement = Array.from(document.getElementsByClassName("chatbot-button") as HTMLCollectionOf<HTMLElement>);
    let attentionBubble = Array.from(document.getElementsByClassName("attention-bubble") as HTMLCollectionOf<HTMLElement>);

	//chatWindowElement[0].style.display = "block";
	chatWindowElement[0].style.height = "auto";
	chatWindowElement[0].style.maxHeight = "600px";
	chatWindowElement[0].style.width = "400px";
    chatButtonElement[0].style.display = "none";
    attentionBubble[0].style.display = "none";

    clearTimeout(this.showAttentionBubbleTimeout);
    clearTimeout(this.closeAttentionBubbleTimeout);
  }

  closeChatbotWindow() {
    let chatWindowElement = Array.from(document.getElementsByClassName("container") as HTMLCollectionOf<HTMLElement>);
    let chatButtonElement = Array.from(document.getElementsByClassName("chatbot-button") as HTMLCollectionOf<HTMLElement>);

	//chatWindowElement[0].style.display = "none";
	chatWindowElement[0].style.height = "0";
	chatWindowElement[0].style.width = "0";
	chatWindowElement[0].style.maxHeight = "0";
    chatButtonElement[0].style.display = "block";
  }
}
