import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FlashProgDeviceComponent } from './flash-prog-device.component';

describe('FlashProgDeviceComponent', () => {
  let component: FlashProgDeviceComponent;
  let fixture: ComponentFixture<FlashProgDeviceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FlashProgDeviceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FlashProgDeviceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
