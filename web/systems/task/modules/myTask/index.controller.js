
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
      console.log(" ----------- removeTaskEvent ----------");
      console.log(args);
      $scope.getTasks();
    }

    function changeTaskEvent(args) {
      console.log(" ----------- changeTaskEvent ----------");
      console.log(args);
      $scope.getTasks();
    }

    function newTaskEvent(args) {
      console.log(" ----------- newTaskEvent ----------");
      console.log(args);
      // $scope.model.tasks.push(args[0]);
      $scope.getTasks();
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

        },
        function(error) {
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

}
