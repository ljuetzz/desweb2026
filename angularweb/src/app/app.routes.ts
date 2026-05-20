import { Routes } from '@angular/router';
import { BuildingForm } from './building-form/building-form';
import { StreetForm } from './street-form/street-form';
import { PoiForm } from './poi-form/poi-form';

export const routes: Routes = [
  { path: '', redirectTo: 'building', pathMatch: 'full' },
  { path: 'building', component: BuildingForm },
  { path: 'street', component: StreetForm },
  { path: 'poi', component: PoiForm }
];