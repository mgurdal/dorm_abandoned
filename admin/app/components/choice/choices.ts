import { Component, OnInit } from '@angular/core';
import { ChoiceService } from '../../services/choiceService'

@Component({
  selector: 'choices',
  template: `<ul><li *ngFor="let choice of choices">{{choice.choice_text}}</li></ul>`
})
export class DinosaurComponent implements OnInit {
  choices: any[];
  error: any;

  constructor(private choiceService: ChoiceService) { }

  getChoices() {
    this.choiceService
        .getChoices()
        .then(choices => this.choices = choices['results'])
        .catch(error => this.error = error);
  }

  ngOnInit() {
    this.getChoices();
  }
}
