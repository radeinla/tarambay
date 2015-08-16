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
  '$q', '$scope', '$mdDialog', 'mdThemeColors', '$http', 'Event',
  function($q, $scope, $mdDialog, mdThemeColors, $http, Event) {
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
      this.addEvent.params = {
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

