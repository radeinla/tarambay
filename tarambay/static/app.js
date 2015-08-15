//alert('Hello world!');

angular.module('tarambayApp', ['ngMaterial', 'ngMap'])
.controller('tarambayAppController', function($scope, $mdDialog) {
  $scope.openAddEventDialog = function(ev) {
    $mdDialog.show({
      controller: AddEventDialogController,
      templateUrl: 'addEventDialog.tmpl.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:true,
      resolve: {
        //TODO: get categories
      }
    })
    .then(function() {
      console.log('dialog hide');
    }, function() {
      console.log('dialog cancel');
    });
  };
})

.controller('SearchFormController', function($scope) {

});

function AddEventDialogController($scope, $mdDialog) {
  $scope.params = {
    private: true,
  };
  $scope.tags = [];

  $scope.cancel = function() {
    $mdDialog.cancel();
  };

  $scope.saveEvent = function() {
    //TODO: save
    console.log('saveEvent');
    console.log($scope.params);
    $mdDialog.hide();
  };
}