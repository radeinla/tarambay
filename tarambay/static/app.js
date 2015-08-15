//alert('Hello world!');

angular.module('tarambayApp', ['ngMaterial', 'mdThemeColors', 'JDatePicker', 'ngMap'])
.config(['$mdThemingProvider', function($mdThemingProvider) {
  $mdThemingProvider.theme('default').primaryPalette('purple');
}])

.controller('tarambayAppController', ['$scope', '$mdDialog', '$http', 'mdThemeColors', function($scope, $mdDialog, $http, mdThemeColors) {
  $scope.mdThemeColors = mdThemeColors;
  this.addEvent = {};
  var self = this;

  this.categoriesPromise = $http.get('/api/categories')
    .then(function(response) {
      console.log(response.data.results);
      self.categories = response.data.results;
    }, function(error) {
      //TODO: error
    });

  this.loadCategories = function() {
    return this.categoriesPromise;
  }

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

