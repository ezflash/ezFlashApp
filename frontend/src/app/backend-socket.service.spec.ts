import { TestBed } from '@angular/core/testing';

import { BackendSocketService } from './backend-socket.service';

describe('BackendSocketService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: BackendSocketService = TestBed.get(BackendSocketService);
    expect(service).toBeTruthy();
  });
});
