//alert('Hello world!');

angular.module('tarambayApp', ['ngMaterial', 'mdThemeColors', 'JDatePicker', 'ngMap', 'ngResource'])
.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])
.config(['$mdThemingProvider', function($mdThemingProvider) {
  $mdThemingProvider.theme('default').primaryPalette('purple');
}])
.config(['$resourceProvider', function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}])
.factory('Event', function($resource) {
  return $resource('/api/events/:id', {}, {
    query: {
      isArray: false
    }
  });
})
.controller('tarambayAppController', [
  '$scope', '$mdDialog', 'mdThemeColors', '$http', 'Event',
  function($scope, $mdDialog, mdThemeColors, $http, Event) {
    var self = this;
    $scope.mdThemeColors = mdThemeColors;

    this.addEvent = {};

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

    self.setDefaultEventParams = function () {
      self.addEvent.params = {
        private: true,
        tags: []
      };
    }

    self.setDefaultEventParams();

    self.toggleAddEvent = function() {
      if (self.addEventVisible) {
        self.cancelAddEvent();
      } else {
        self.addEventVisible = true;
      }
    };

    self.hideAddEvent = function() {
      this.addEventVisible = false;
      this.setDefaultEventParams();
    };

    self.saveEvent = function() {
      //TODO: save
      console.log('saveEvent');
      console.log($scope.params);
      var newEvent = new Event(self.addEvent.params);
      var createEvent = newEvent.$save();
      createEvent.then(function(created) {
        console.log({created: created});
        self.hideAddEvent();
      }, function() {
        console.log('failed!');
      });
    };

    self.cancelAddEvent = function() {
      console.log('cancelAddEvent');
      this.hideAddEvent();
    };
  }
])

.controller('SearchFormController', function($scope) {

});

