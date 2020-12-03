import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { SuotaListComponent } from './suota/suota-list/suota-list.component';
import { FlashProgListComponent } from './flashProg/flash-prog-list/flash-prog-list.component';
import { PageNotFoundComponentComponent } from './page-not-found-component/page-not-found-component.component';

const routes: Routes = [
  { path: 'flashprog', component: FlashProgListComponent },
  { path: 'suota', component: SuotaListComponent },
  { path: '', redirectTo: '/flashprog', pathMatch: 'full' },
  { path: '**', component: PageNotFoundComponentComponent  }];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
