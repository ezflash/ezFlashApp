import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FlashConfirmDialogComponent } from './flash-confirm-dialog.component';

describe('FlashConfirmDialogComponent', () => {
  let component: FlashConfirmDialogComponent;
  let fixture: ComponentFixture<FlashConfirmDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FlashConfirmDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FlashConfirmDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
