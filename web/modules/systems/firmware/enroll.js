var app = angular.module('mainApp');

app.controller("EnrollCtrl", function($scope, $rootScope, $timeout, Session, Notifications) {


  $scope.model = {
    dni:null,
    class:'show-front',
    isTransition:'true',
    classItem1:'front',
    classItem2:'right',
    classItem3:'hidden',
    classItem4:'left',
    selectItem:1
  }

  $scope.initialize = function() {
    $scope.model.dni = null;
    $scope.model.class = 'show-front';
    $scope.model.isTransition = 'true';
    $scope.model.classItem1 = 'front';
    $scope.model.classItem2 = 'right';
    $scope.model.classItem3 = 'hidden';
    $scope.model.classItem4 = 'left';
    $scope.model.selectItem = 1;

  }

  $scope.next = function() {
    $scope.selectRight();
  }

  $scope.save = function() {
    Notifications.message("Se ha enrolado correctamente al usuario " + $scope.model.dni);
    $scope.model.selectItem = 1;
    $scope.initialize();
  }


  $scope.changeItem = function(item1,item2,item3,item4) {
    $scope.item1 = item1;
    $scope.item2 = item2;
    $scope.item3 = item3;
    $scope.item4 = item4;
    $timeout(function() {
        $scope.model.classItem1 = $scope.item1;
        $scope.model.classItem2 = $scope.item2;
        $scope.model.classItem3 = $scope.item3;
        $scope.model.classItem4 = $scope.item4;
        $scope.model.isTransition = 'false';
        $scope.model.class = 'show-front';
    }, 1000);
  }

  $scope.selectLeft = function() {
  $scope.model.isTransition = 'true';
    $scope.model.class = 'show-left';

    var item = $scope.model.selectItem;
    if (item == 1) {
      $scope.model.selectItem = 4;
    } else {
      $scope.model.selectItem = $scope.model.selectItem - 1;
    }

    switch ($scope.model.selectItem) {
      case 1: $scope.changeItem('front','right','hidden','left'); break;
      case 2: $scope.changeItem('left','front','right','hidden'); break;
      case 3: $scope.changeItem('hidden','left','front','right'); break;
      case 4: $scope.changeItem('right','hidden','left','front'); break;
    }

  }

  $scope.selectRight = function() {

    var item = $scope.model.selectItem;
    if (item == 4) {
      $scope.save();
      return;
    } else {
      $scope.model.selectItem = $scope.model.selectItem + 1;
    }

    // esto es temporal, simula la escucha de eventos
    if ($scope.model.selectItem > 1) {
      $timeout(function() { $scope.next();}, 3500);
    }

    //

    $scope.model.isTransition = 'true';
    $scope.model.class = 'show-right';

    switch ($scope.model.selectItem) {
      case 1: $scope.changeItem('front','right','hidden','left'); break;
      case 2: $scope.changeItem('left','front','right','hidden'); break;
      case 3: $scope.changeItem('hidden','left','front','right'); break;
      case 4: $scope.changeItem('right','hidden','left','front'); break;
    }
  }


});
