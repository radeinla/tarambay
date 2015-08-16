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
  '$scope', '$mdDialog', 'mdThemeColors', '$http', '$timeout', 'Event',
  function($scope, $mdDialog, mdThemeColors, $http, $timeout, Event) {
    var self = this;
    self.viewAsMap = true;
    $scope.mdThemeColors = mdThemeColors;

    this.addEvent = {};

    this.categoriesPromise = $http.get('/api/categories')
      .then(function(response) {
        self.categories = response.data.results;
        self.categoriesDict = {}
        for (var i=0; i<self.categories.length; i++) {
          self.categoriesDict[self.categories[i].id] = self.categories[i].name;
        }
      }, function(error) {
        //TODO: error
      });

    $scope.$on('mapInitialized', function(event, map) {
      $scope.map = map;
      if (self.viewAsMap)
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
          self.allEvents = response.data.results;
          self.allEventsMarkers = [];
          for (var i=0; i<response.data.results.length; i++) {
            var gMapsLatLong = new google.maps.LatLng(response.data.results[i].latitude, response.data.results[i].longitude)
            self.allEventsMarkers.push(gMapsLatLong);
            var marker = new google.maps.Marker({
              position: gMapsLatLong,
              map: $scope.map,
              draggable: false,
              title: response.data.results[i].title,
              eventInfo: response.data.results[i]
            });
            marker.addListener('click', function(event) {
              //open dialog with event info
              console.log('click', this);
              $mdDialog.show({
                controller: ShowEventController,
                templateUrl: 'showEventDialog.tmpl.html',
                parent: angular.element(document.body),
                targetEvent: event,
                clickOutsideToClose:true,
                locals: {
                  selectedEvent: this.eventInfo,
                  categoriesDict: self.categoriesDict
                }
              });
            });
          };
          console.log(self.allEventsMarkers);
        }, function(error){
          //TODO: error
        })
    };

    self.listEvents = function() {
      if (!self.allEvents) {
        $http.get('/api/events')
        .then(function(response) {
          self.allEvents = response.data.results;
        }, function(error) {
          //TODO: error
        })
      }
    };

    self.showEvent = function(event, selectedEvent) {
      $mdDialog.show({
        controller: ShowEventController,
        templateUrl: 'showEventDialog.tmpl.html',
        parent: angular.element(document.body),
        targetEvent: event,
        clickOutsideToClose:true,
        locals: {
          selectedEvent: selectedEvent,
          categoriesDict: self.categoriesDict
        }
      });
    };

    self.setDefaultEventParams();
    self.loadCategories();
  }
])

.controller('SearchFormController', function($scope) {

});

function ShowEventController($scope, $mdDialog, selectedEvent, categoriesDict) {
  $scope.selectedEvent = selectedEvent;

  $scope.closeShowEventDialog = function() {
    $mdDialog.cancel();
  };

  $scope.joinEvent = function(event) {
    console.log('joinEvent', event);
    //TODO: join event
    //TODO: show toast: successful/error
    $mdDialog.hide();
  };

  $scope.getCategoryName = function(categoryLink) {
    console.log('getCategoryName', categoryLink);
    //TODO: ayusin? pampabilis lang to
    var id = categoryLink.split('/')[5];
    if (id in categoriesDict) {
      return categoriesDict[id];
    }
    else return null;
  };

  $scope.getUserDisplayName = function(userLink) {

  }
};

