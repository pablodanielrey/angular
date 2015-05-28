var app = angular.module('mainApp');

app.controller("EnrollCtrl", ['$scope','$timeout','Notifications', 'Firmware',function($scope, $timeout, Notifications, Firmware) {


  $scope.model = {
    dni:null,
    class:'show-front',
    isTransition:'true',
    classItem1:'front',
    classItem2:'right',
    classItem3:'hidden',
    classItem4:'left',
    selectItem:1,
    fingers:0
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
    $scope.model.fingers = 0;

  }

  /* -------------------------------------------
   * ---------- TECLADO NUMERICO ---------------
   * -------------------------------------------
   */

  $scope.addNumber = function(n) {
    if (n == '0' && ($scope.model.dni == null || $scope.model.dni.length == 0)) {
        return;
    }

    $scope.model.dni = ($scope.model.dni == null) ? n : $scope.model.dni + n;
  }

  $scope.deleteNumber = function() {
    $scope.model.dni = ($scope.model.dni == null || $scope.model.dni.length == 0) ? null : $scope.model.dni.substring(0, $scope.model.dni.length-1);
  }

  /* -------------------------------------------
   * -------- FUNCIONES VISUALIZACION ----------
   * -------------------------------------------
   */

  $scope.next = function() {
    $scope.selectRight();
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
    }, 3000);
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


  /* -------------------------------------------
   * -------- Mensajes del Servidor ------------
   * -------------------------------------------
   */

   $scope.save = function() {
     Notifications.message("Se ha enrolado correctamente al usuario " + $scope.model.dni);
     $scope.model.selectItem = 1;
     $scope.initialize();
   }


   $scope.addUser = function() {
     Firmware.enroll($scope.model.dni,
       function(response) {
         $scope.next();
       },
       function(error) {
          Notifications.message(error);
       }
     );
   }


   /*
      FingerRequestedEvent {
          type: FingerRequestedEvent,
          data: {
                fingerNumber:numero_de_dedo
          }
      }

      ErrorEvent {
          type:ErrorEvent,
          data: {
            error: mensaje_de_error
          }
      }

      MsgEvent {
        type:MsgEvent,
        data: {
          msg: mensaje_a_mostrar
        }
      }

   */


   $scope.$on('FingerRequestedEvent', function(event, data) {
   }

   $scope.$on('ErrorEvent', function(event, data) {
   }

   $scope.$on('MsgEvent', function(event, data) {
   }

   /*
    finger updated event no va mas. este codigo no va mas.
   */
   $scope.$on('FingerUpdatedEvent', function(event, data) {

     if (typeof data.error === 'undefined') {
       $scope.model.fingers = $scope.model.fingers + 1;

       if ($scope.model.fingers == 3) {
          $scope.save();
       } else {
         $scope.next();
       }
     } else {
       Notification.message(data.error);
     }
   });




}]);
