import { Article } from './article';

export class BotMessage {
  contents: BotMessageContents[] = [];
}

export class BotMessageContents {
  text: string;
  additional: Article[] | Office | undefined; // TODO: Implement contacts
}

export class Office {
  visitAddress: VisitAddress;
  contactInfo: ContactInfo;
  postAddress: PostAddress;

  constructor(visitAddress: VisitAddress, contactInfo: ContactInfo, postAddress: PostAddress) {
    this.visitAddress = visitAddress;
    this.contactInfo = contactInfo;
    this.postAddress = postAddress;
  }
}

export class VisitAddress {
  country: string;
  street: string;
  city: string;

  constructor(country: string, street: string, city: string) {
    this.country = country;
    this.street = street;
    this.city = city;
  }
}

export class ContactInfo {
  phone: string;
  mail: string;
  fax: string;

  constructor(phone: string, mail: string, fax: string) {
    this.phone = phone;
    this.mail = mail;
    this.fax = fax;
  }
}

export class PostAddress {
  companyName: string;
  street: string;
  zip: string;
  city: string;

  constructor(companyName: string, street: string, zip: string, city: string) {
    this.companyName = companyName;
    this.street = street;
    this.zip = zip;
    this.city = city;
  }
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

    } else if (response.hasOwnProperty('office')) {
      let office = response.office;
      let visitAddress = new VisitAddress(office.visitAddress.country, office.visitAddress.street, office.visitAddress.city);
      let contactInfo = new ContactInfo(office.contactInfo.phone, office.contactInfo.mail, office.contactInfo.fax);
      let postAddress = new PostAddress(office.postAddress.companyName, office.postAddress.street, office.postAddress.zip, office.postAddress.city);

      contents.additional = new Office(visitAddress, contactInfo, postAddress);

    } else if (response.hasOwnProperty('contacts')) {
      // TODO: Implement contacts
    }
    return contents;
}
