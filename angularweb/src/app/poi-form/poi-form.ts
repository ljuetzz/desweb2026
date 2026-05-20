import { Component } from '@angular/core';
import { ReactiveFormsModule, FormControl, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../api';
import { ServerAnswer } from '../models/server-answer';
import { Poi } from '../models/poi';

@Component({
  selector: 'app-poi-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './poi-form.html',
  styleUrl: './poi-form.css'
})
export class PoiForm {

  message = '';
  answer = '';

  id = new FormControl(1, Validators.required);
  name = new FormControl('', Validators.required);
  description = new FormControl('', Validators.required);
  category = new FormControl('', Validators.required);
  visitedAt = new FormControl('', Validators.required);
  rating = new FormControl(0, Validators.required);
  geom = new FormControl('', Validators.required);

  controlsGroup = new FormGroup({
    id: this.id,
    name: this.name,
    description: this.description,
    category: this.category,
    visitedAt: this.visitedAt,
    rating: this.rating,
    geom: this.geom
  });

  constructor(private api: ApiService) {}

  getPoiFromForm() {
    let poi = new Poi();
    poi.name = this.name.value || '';
    poi.description = this.description.value || '';
    poi.category = this.category.value || '';
    poi.visitedAt = this.visitedAt.value || '';
    poi.rating = Number(this.rating.value);
    poi.geom = this.geom.value || '';
    return poi;
  }

  putPoiInForm(poi: any) {
    this.id.setValue(poi.id);
    this.name.setValue(poi.name);
    this.description.setValue(poi.description);
    this.category.setValue(poi.category);
    this.visitedAt.setValue(poi.visitedAt);
    this.rating.setValue(poi.rating);
    this.geom.setValue(poi.geom);
  }

  fillExample() {
    this.name.setValue('UPV Point');
    this.description.setValue('POI inserted from Angular reactive form');
    this.category.setValue('landmark');
    this.visitedAt.setValue('2026-05-07T10:00:00Z');
    this.rating.setValue(5);
    this.geom.setValue('POINT(726050 4372050)');
  }

  clean() {
    this.id.setValue(1);
    this.name.setValue('');
    this.description.setValue('');
    this.category.setValue('');
    this.visitedAt.setValue('');
    this.rating.setValue(0);
    this.geom.setValue('');
    this.message = 'POI form cleaned';
    this.answer = '';
  }

  manageAnswer(res: any) {
    let serverAnswer = res as ServerAnswer;
    this.answer = JSON.stringify(serverAnswer, null, 2);

    if (serverAnswer.ok) {
      this.message = serverAnswer.message;
      if (serverAnswer.data.length > 0 && serverAnswer.data[0].id) {
        this.id.setValue(serverAnswer.data[0].id);
        this.message = serverAnswer.message + ' with id ' + serverAnswer.data[0].id;
      }
    } else {
      this.message = 'Error: ' + serverAnswer.message;
    }
  }

  insert() {
    if (this.controlsGroup.invalid) {
      this.message = 'Error: some form controls are not valid';
      return;
    }

    this.api.insert('poi', this.getPoiFromForm()).subscribe((res: any) => {
      this.manageAnswer(res);
    });
  }

  selectAll() {
    this.api.selectAll('poi').subscribe((res: any) => {
      this.manageAnswer(res);
    });
  }

  selectOne() {
    let idValue = Number(this.id.value);

    this.api.selectOne('poi', idValue).subscribe((res: any) => {
      this.manageAnswer(res);
      if (res.ok && res.data.length > 0) {
        this.putPoiInForm(res.data[0]);
      }
    });
  }

  update() {
    if (this.controlsGroup.invalid) {
      this.message = 'Error: some form controls are not valid';
      return;
    }

    let idValue = Number(this.id.value);

    this.api.update('poi', idValue, this.getPoiFromForm()).subscribe((res: any) => {
      this.manageAnswer(res);
    });
  }

  delete() {
    let idValue = Number(this.id.value);

    this.api.delete('poi', idValue).subscribe((res: any) => {
      this.manageAnswer(res);
      if (res.ok) {
        this.clean();
        this.message = 'POI deleted with id ' + idValue;
      }
    });
  }
}