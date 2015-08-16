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
  '$q', '$scope', '$mdDialog', 'mdThemeColors', '$http', '$window', 'Event',
  function($q, $scope, $mdDialog, mdThemeColors, $http, $window, Event) {
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
      this.addEvent.params = {
        private: true,
        tags: []
      };
    }

    $scope.login = function() {
      $window.location.href = '/api-auth/login';
    };
    $scope.logout = function() {
      $window.location.href = '/api-auth/logout/?next=/';
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

    self.formatDateForApi = function(date, time) {
        return date.format("YYYY-MM-DD") + "T" + time.format("HH:mm") + "+08:00";
    };

    self.parseDateTime = function(dateStr, timeStr) {
      var parts = [moment(dateStr), moment(timeStr.toLowerCase(), ['hh:mm a','hh:mma','hha','ha','hh a', 'h a'])];
      for (var i in parts) {
        var part = parts[i];
        if (!part.isValid()) {
          return null;
        }
      }
      return parts;
    }

    self.parseErrors = function(responseErrors) {
      var errors = [];
      for (key in responseErrors) {
        errors = errors.concat(responseErrors[key]);
      }
      return errors;
    }

    self.saveEvent = function() {
      var data = angular.extend({}, self.addEvent.params);
      if (!data.startDate || !data.startTime || !data.endDate || !data.endTime) {
        self.addEvent.errors = {non_field_errors: ['Please specify start and end date and time.']};
        return;
      }
      if (data.startDate) {
        var parts = self.parseDateTime(data.startDate, data.startTime);
        if (!parts) {
          self.addEvent.errors = {non_field_errors: ['Please specify valid start date and time.']};
          return;
        }
        delete data.startDate;
        delete data.startTime;
        data.start = self.formatDateForApi(parts[0], parts[1]);
      }
      if (data.endDate) {
        var parts = self.parseDateTime(data.endDate, data.endTime);
        if (!parts) {
          self.addEvent.errors = {non_field_errors: ['Please specify valid end date and time.']};
          return;
        }
        delete data.endDate;
        delete data.endTime;
        data.end = self.formatDateForApi(parts[0], parts[1]);
      }
      var newEvent = new Event(data);
      var createEvent = newEvent.$save();
      createEvent.then(function(created) {
        console.log({created: created});
        self.hideAddEvent();
        self.updateMapPins();
      }, function(reject) {
        self.addEvent.errors = reject.data;
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

function ShowEventController($scope, $mdDialog, $http, selectedEvent, categoriesDict) {
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

  this.getCategoryName = function(categoryLink) {
    //TODO: ayusin? pampabilis lang to
    var id = categoryLink.split('/')[5];
    if (id in categoriesDict) {
      $scope.eventCategory = categoriesDict[id];
    } else {
      $http.get(categoryLink)
        .then(function(response) {
          $scope.eventCategory = response.data.name;
        }, function(error) {
          //TODO: error
        });
    }
  };

  this.getUserDisplayName = function(userLink) {
    $http.get(userLink)
      .then(function(response) {
        $scope.eventCreator = response.data.username;
      }, function(error) {
        //TODO: error
      });
  }

  this.getCategoryName(selectedEvent.category);
  this.getUserDisplayName(selectedEvent.admin);
};

