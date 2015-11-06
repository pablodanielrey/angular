
angular
    .module('mainApp')
    .controller('MyTaskCtrl',MyTaskCtrl);

MyTaskCtrl.$inject = ['$scope', '$wamp', 'Notifications', '$location', 'Task'];

function MyTaskCtrl($scope, $wamp, Notifications,  $location, Task) {


    // -------------------------------------------------------------
    // ------------------------- VARIABLES -------------------------
    // -------------------------------------------------------------

    $scope.model = {
      task:'',
      tasks:[]
    }

    $scope.id = 2;

    // -------------------------------------------------------------
    // ------------------------- METODOS ---------------------------
    // -------------------------------------------------------------

    $scope.initialize = initialize;
    $scope.createTask = createTask;
    $scope.getTasks = getTasks;
    $scope.updateStatus = updateStatus;
    $scope.removeTask = removeTask;
    $scope.removeTaskByStatus = removeTaskByStatus;

    // -------------------------------------------------------------
    // ----------------- CARGA DE DATOS INICIALES ------------------
    // -------------------------------------------------------------

    function initialize() {
    	$scope.getTasks();
    	$wamp.subscribe('task.removeTaskEvent', removeTaskEvent);
    	$wamp.subscribe('task.changeTaskEvent', changeTaskEvent);
    	$wamp.subscribe('task.newTaskEvent', newTaskEvent);
    }

    function removeTaskEvent(args) {
      var id = args[0];
      for (var i = 0; i < $scope.model.tasks.length; i++) {
        var t = $scope.model.tasks[i];
        if (t.id == id) {
          var index = $scope.model.tasks.indexOf(t);
          if (index > -1) {
            $scope.model.tasks.splice(index, 1);
          }
          return;
        }
      }
    }

    function changeTaskEvent(args) {
      var task = args[0];
      for (var i = 0; i < $scope.model.tasks.length; i++) {
        var t = $scope.model.tasks[i];
        if (t.id == task.id) {
          t.finish = task.finish;
          return;
        }
      }
    }

    function newTaskEvent(args) {
      var task = args[0];
      $scope.model.tasks.push(task);
    }


    // -------------------------------------------------------------
    // -------------------- CARGA DE TAREAS ------------------------
    // -------------------------------------------------------------

    function getTasks() {
      Task.getTasks(
        function(data) {
          $scope.model.tasks = data;
        },
        function(error) {
          Notifications.message(error);
        }
      );
    }

    // -------------------------------------------------------------
    // ------------------------- EVENTOS ---------------------------
    // -------------------------------------------------------------
    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });


    // -------------------------------------------------------------
    // ------------------------ ACCIONES ---------------------------
    // -------------------------------------------------------------

    function createTask() {
      Task.createTask($scope.model.task,
        function(data) {
          $scope.model.task = '';
        },
        function(error) {
          $scope.model.task = '';
          Notifications.message(error);
        }
      );
    }

    function updateStatus(task) {
      Task.updateStatus(task.id,task.finish,
        function(data) {

        },
        function(error) {
          Notifications.message(error);
        }
      );
    }

    function removeTask(task) {
      Task.removeTask(task.id,
        function(data) {

        },
        function(error) {
          Notifications.message(error);
        }
      );
    }


    function removeTaskByStatus() {
      Task.removeTaskByStatus(true,
        function(data) {

        },
        function(error) {
          Notifications.message(error);
        }
      );
    }

}
