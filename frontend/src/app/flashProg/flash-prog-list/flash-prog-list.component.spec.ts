import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FlashProgListComponent } from './flash-prog-list.component';

describe('FlashProgListComponent', () => {
  let component: FlashProgListComponent;
  let fixture: ComponentFixture<FlashProgListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FlashProgListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FlashProgListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
