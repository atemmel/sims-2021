import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleMessageComponent } from './article-message.component';

describe('ArticleMessageComponent', () => {
  let component: ArticleMessageComponent;
  let fixture: ComponentFixture<ArticleMessageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ArticleMessageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ArticleMessageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
