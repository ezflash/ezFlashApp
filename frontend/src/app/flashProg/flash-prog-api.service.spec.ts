import { TestBed } from '@angular/core/testing';

import { FlashProgApiService } from './flash-prog-api.service';

describe('FlashProgApiService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: FlashProgApiService = TestBed.get(FlashProgApiService);
    expect(service).toBeTruthy();
  });
});
