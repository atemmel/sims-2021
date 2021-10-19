import { ComponentFixture, TestBed } from '@angular/core/testing';

import { KnowitBackgroundComponent } from './knowit-background.component';

describe('KnowitBackgroundComponent', () => {
  let component: KnowitBackgroundComponent;
  let fixture: ComponentFixture<KnowitBackgroundComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ KnowitBackgroundComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(KnowitBackgroundComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
