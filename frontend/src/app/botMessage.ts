import { NgIterable } from '@angular/core';
import { Article } from './article';
import { Office, VisitAddress, ContactInfo, PostAddress } from './office';

export class BotMessage {
  contents: BotMessageContents[] = [];
}

export class BotMessageContents {
  text: string;
  additional: any;

  // TODO: below doesn't work with ArticleMessageComponent
  // and officeMessageComponent, get smarter and fix it
  //additional: Article[] | Office[] | undefined;
}

export function buildContents(response: any) {
    var contents = new BotMessageContents();
    contents.text = response.text;

    if (response.hasOwnProperty('articles')) {

      let articles: Article[] = [];

      for (let article of response.articles) {
        articles.push(new Article(article.title, article.url));
      }

      contents.additional = articles;

    } else if (response.hasOwnProperty('offices')) {
      let offices: Office[] = [];

      for (let office of response.offices) {
        let visitAddress = new VisitAddress(office.visitAddress.country, office.visitAddress.street, office.visitAddress.city);
        let contactInfo = new ContactInfo(office.contactInfo.phone, office.contactInfo.mail, office.contactInfo.fax);
        let postAddress = new PostAddress(office.postAddress.companyName, office.postAddress.street, office.postAddress.zip, office.postAddress.city);
        offices.push(new Office(visitAddress, contactInfo, postAddress));
      }
      contents.additional = offices
    }
    return contents;
}
