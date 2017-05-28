import { Component } from '@angular/core';
import { DinosaurComponent } from './components/choice/choices'
import { ChoiceService } from './services/choiceService'

@Component({
  selector: 'my-app',
  template: `<h1>Hello {{name}}<span *ngIf="itIsJuly">, DjangoCon</span>!</h1>
              <choices></choices>`,
  directives: [DinosaurComponent],
  providers: [ChoiceService]
})

export class AppComponent {
  name:string = 'World'
  itIsJuly:boolean

  constructor() {
      var date = new Date()
      this.itIsJuly = (date.getMonth() == 6 && date.getFullYear() == 2016)
  }
}
