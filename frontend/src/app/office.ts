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
