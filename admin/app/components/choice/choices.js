"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
var choiceService_1 = require('../../services/choiceService');
var DinosaurComponent = (function () {
    function DinosaurComponent(choiceService) {
        this.choiceService = choiceService;
    }
    DinosaurComponent.prototype.getChoices = function () {
        var _this = this;
        this.choiceService
            .getChoices()
            .then(function (choices) { return _this.choices = choices['results']; })
            .catch(function (error) { return _this.error = error; });
    };
    DinosaurComponent.prototype.ngOnInit = function () {
        this.getChoices();
    };
    DinosaurComponent = __decorate([
        core_1.Component({
            selector: 'choices',
            template: "<ul><li *ngFor=\"let choice of choices\">{{choice.choice_text}}</li></ul>"
        }), 
        __metadata('design:paramtypes', [choiceService_1.ChoiceService])
    ], DinosaurComponent);
    return DinosaurComponent;
}());
exports.DinosaurComponent = DinosaurComponent;
//# sourceMappingURL=choices.js.map