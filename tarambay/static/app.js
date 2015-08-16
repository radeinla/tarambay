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
  var Event = $resource('/api/events/:id', {}, {
    query: {
      isArray: false,
      transformResponse: [function(data, getHeaders) {
        return angular.fromJson(data);
      }, function(data, getHeaders) {
        var results = [];
        for (var idx in data.results) {
          var event = data.results[idx];
          results.push(new Event(event));
        }
        data.results = results;
        return data;
      }],
    }
  });

  Event.prototype.getCoordinates = function(){
    console.log(this);
    return [parseFloat(this.latitude), parseFloat(this.longitude)];
  };

  Event.prototype.join = function() {
    var Join = $resource('/api/events/'+this.id+'/join', {}, {
      update: {
        method: 'PUT',
      }
    });
    var join = new Join({id: this.id, join: true});
    return join.$update();
  };

  (new Event()).join();

  return Event;
})

.controller('tarambayAppController', [
  '$q', '$scope', '$mdDialog', 'mdThemeColors', '$http', '$window', 'Event',
  function($q, $scope, $mdDialog, mdThemeColors, $http, $window, Event) {
    var self = this;
    self.viewAsMap = true;
    self.currentUser = null;
    $scope.mdThemeColors = mdThemeColors;

    self.addEvent = {};

    self.categoriesPromise = $http.get('/api/categories')
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

    self.loadCategories = function() {
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

    self.fetchCurrentUser = function() {
      $http.get('api/users/profile')
        .then(function(response){
          self.currentUser = response.data
        }, function(error){
          self.currentUser = null;
        })
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
      Event.query().$promise
        .then(function(events) {
          var response = {data: {results: events.results}};
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
      // if (!self.allEvents) {
        Event.query('/api/events').$promise
        .then(function(events) {
          console.log(events);
          self.allEvents = events.results;
        }, function(error) {
          //TODO: error
        })
      // }
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
    self.fetchCurrentUser();
  }
])

.controller('SearchFormController', function($scope) {

});

function ShowEventController($scope, $mdDialog, $http, selectedEvent, categoriesDict, Event) {
  $scope.selectedEvent = selectedEvent;

  $scope.closeShowEventDialog = function() {
    $mdDialog.cancel();
  };

  $scope.joinEvent = function(event) {
    console.log('joinEvent', event);
    console.log(event);
    (new Event(event)).join().then(function() {
      console.log('joined!');
    });
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

