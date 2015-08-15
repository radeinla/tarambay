//alert('Hello world!');

angular.module('tarambayApp', ['ngMaterial', 'mdThemeColors', 'JDatePicker'])
.config(['$mdThemingProvider', function($mdThemingProvider) {
  $mdThemingProvider.theme('default').primaryPalette('purple');
}])
.controller('tarambayAppController', ['$scope', '$mdDialog', 'mdThemeColors', function($scope, $mdDialog, mdThemeColors) {
  $scope.mdThemeColors = mdThemeColors;
  this.addEvent = {};

  this.setDefaultEventParams = function () {
    this.addEvent.params = {
      private: true,
      tags: []
    };
  }

  this.setDefaultEventParams();

  this.toggleAddEvent = function() {
    if (this.addEventVisible) {
      this.cancelAddEvent();
    } else {
      this.addEventVisible = true;
    }
  };

  this.hideAddEvent = function() {
    this.addEventVisible = false;
    this.setDefaultEventParams();
  };

  this.saveEvent = function() {
    //TODO: save
    console.log('saveEvent');
    console.log($scope.params);
    this.hideAddEvent();
  };

  this.cancelAddEvent = function() {
    console.log('cancelAddEvent');
    this.hideAddEvent();
  };
}])

.controller('SearchFormController', function($scope) {

});

