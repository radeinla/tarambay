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
        self.categories = response.data.results;
      }, function(error) {
        //TODO: error
      });

    $scope.$on('mapInitialized', function(event, map) {
      $scope.map = map;
      self.updateMapPins();
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

    self.updateMapPins = function() {
      $http.get('/api/events')
        .then(function(response) {
          console.log(response.data.results)
          self.allEvents = [];
          for (var i=0; i<response.data.results.length; i++) {
            self.allEvents.push(new google.maps.LatLng(response.data.results[i].latitude, response.data.results[i].longitude));
            var marker = new google.maps.Marker({
              position: self.allEvents[i],
              map: $scope.map,
              draggable: false,
              title: response.data.results[i].title
            });
            marker.addListener('click', function() {
              //TODO: open dialog with event info
            });
          };
          console.log(self.allEvents);
        }, function(error){
          //TODO: error
        })
    }
  }
])

.controller('SearchFormController', function($scope) {

});

