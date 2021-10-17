import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { MessagesComponent } from './messages/messages.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ArticleMessageComponent } from './article-message/article-message.component';
import { OfficeMessageComponent } from './office-message/office-message.component';
import { KnowitBackgroundComponent } from './knowit-background/knowit-background.component';

@NgModule({
  declarations: [
    AppComponent,
    MessagesComponent,
    ArticleMessageComponent,
    OfficeMessageComponent,
    KnowitBackgroundComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
