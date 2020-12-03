import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SuotaListComponent } from './suota-list.component';

describe('SuotaListComponent', () => {
  let component: SuotaListComponent;
  let fixture: ComponentFixture<SuotaListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SuotaListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SuotaListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
