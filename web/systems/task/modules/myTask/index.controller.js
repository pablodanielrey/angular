
angular
    .module('mainApp')
    .controller('MyTaskCtrl',MyTaskCtrl);

MyTaskCtrl.$inject = ['$scope', 'Notifications', '$location'];

function MyTaskCtrl($scope, Notifications,  $location) {
  

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
    }

    
    // -------------------------------------------------------------
    // -------------------- CARGA DE TAREAS ------------------------
    // -------------------------------------------------------------    
    
    function getTasks() {
      $scope.model.tasks = [
	{text:'Terminar sistema de tareas',finish:false,id:1,created:Date.now()},
	{text:'Terminar sistema de pedidos',finish:true,id:2,created:Date.now()}
      ]
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
      $scope.id = $scope.id + 1;      
      var task = {id:$scope.id, text:$scope.model.task,finish:false,created:Date.now()};
      $scope.model.tasks.push(task);
    }
    
    function updateStatus(task) {
      
    }
    
    function removeTask() {
      
    }
      
}
