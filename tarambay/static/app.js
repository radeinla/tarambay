//alert('Hello world!');

angular.module('tarambayApp', ['ngMaterial'])
.controller('tarambayAppController', function($scope, $mdDialog) {
  $scope.openAddEventDialog = function(ev) {
    $mdDialog.show({
      controller: AddEventDialogController,
      templateUrl: 'addEventDialog.tmpl.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:true
    })
    .then(function(answer) {
      //
    }, function() {
      //
    });
  };
})

.controller('SearchFormController', function($scope) {

});

function AddEventDialogController($scope, $mdDialog) {
  $scope.cancel = function() {
    $mdDialog.cancel();
  };

  $scope.save = function() {
    //TODO: save
  };
}