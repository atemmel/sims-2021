import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AttentionBubbleComponent } from './attention-bubble.component';

describe('AttentionBubbleComponent', () => {
  let component: AttentionBubbleComponent;
  let fixture: ComponentFixture<AttentionBubbleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AttentionBubbleComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AttentionBubbleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
