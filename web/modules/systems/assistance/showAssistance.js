
var app = angular.module('mainApp');
app.controller('ShowAssistanceCtrl', ["$scope", "$timeout", "$window", "Notifications" , "Session", "Assistance", "Users", "Utils","$filter", function($scope, $timeout, $window, Notifications, Session, Assistance, Users, Utils,$filter) {






// Variables


  $scope.model = {

    base64:'',

    download:false,
    //datos de assistance correspondientes a los usuarios
    assistances: [],
      /*ejemplo: {user: null, //nombre de usuario
  	  start: null, //fecha y hora de inicio
	    end: null, //fecha y hora de finalizacion
	    logs: [], //logs
      justification: null,
	    workedTime: null,} //tiempo trabajado*/

	  start: new Date(), //fecha inicial de busqueda
    end: new Date(), //fecha final de busqueda

    groups: [],
    groupSelected:{},

    users: [], //usuarios consultados
    usersFilters:[], //usuarios fitlrados
    usersIdSelected: [], //ids de usuarios seleccionados
    searchUser: null, // string con el usuario buscado

  };

  $scope.disabled = false; //flag para deshabilitar busqueda


// ------------ ORDENACION ///////////////////
$scope.orderBy = $filter('orderBy');

$scope.order = function(predicate, reverse) {
  $scope.model.assistances = $scope.orderBy($scope.model.assistances, predicate, reverse);
};


// ----------- INICIALIZACION --------------------

  $scope.initialize = function() {
    $scope.loadSession();
    $scope.loadUsers();
    $scope.clearUsersSelected();
    $scope.model.download = false;

  }

  $scope.clearUsersSelected = function() {
    $scope.model.usersIdSelected = [];
  }

  $timeout(function() {
    $scope.initialize();
  },0);


  /**
   * Cargar y chequear session
   */
  $scope.loadSession = function(){
    if (!Session.isLogged()){
      Notifications.message("Error: Sesion no definida");
      $window.location.href = "/#/logout";
    } else {
      var session = Session.getCurrentSession();
      $scope.model.session_user_id = session.user_id;
    }
  };


  /**
    * Cargar usuarios
   */
  $scope.loadUsers = function() {
    $scope.model.users = [];
    $scope.model.usersFilters = [];

    Assistance.getUsersInOfficesByRole('autoriza',
      function(usersId) {
        if (usersId == null || usersId.length == 0) {
          usersId = [$scope.model.session_user_id];
        }

        $scope.loadGroups(usersId);
        $scope.defineUsers(usersId);
      },
      function(error){
        Notifications.message(error);
      }
    );
  };

  /**
   * Definir usuarios
   * @param usersId id de los usuarios a definir
   */
  $scope.defineUsers = function(usersId){
    for(var i = 0; i < usersId.length; i++){
      var id = usersId[i];
      Users.findUser(id,
        function(user){
          if(user != null) {
            $scope.model.users.push(user);
            $scope.model.usersFilters.push(user);
          }
        },
        function(error){
          Notifications.message(error);
        }
      );
    }
  };

  /**
    * Cargar todos los grupos
  */
  $scope.loadGroups = function(usersId) {
    $scope.model.groupSelected = {};
    $scope.model.groups = [];

    var userId = $scope.model.session_user_id;
    var tree = true;
    var role = 'autoriza';

    Assistance.getOfficesByUserRole(userId,role,tree,
      function(groups) {
        $scope.model.groups = groups;
      },
      function(error) {
        Notifications.message(error);
      }
    );
  }


  $scope.include = function(users,uid) {
    for (var $i = 0; $i < users.length; $i++) {
      if (users[$i].id == uid) {
        return true;
      }
    }
    return false;
  }

  $scope.filterUsers = function() {
    $scope.model.usersFilters = $scope.model.users.slice();
    if ($scope.model.groupSelected == null) {
      return;
    }

    offices = [$scope.model.groupSelected.id];
    $scope.model.usersFilters = [];

    Assistance.getOfficesUsers(offices,
      function(users) {
        for (var $i = 0; $i < users.length; $i++) {
          var uid = users[$i];
          for (var $k = 0; $k < $scope.model.users.length; $k++) {
            var user = $scope.model.users[$k];
            if (uid == user.id && !$scope.include($scope.model.usersFilters,uid)) {
              $scope.model.usersFilters.push(user);
            }
          }
        }
      },
      function(error) {
        Notification.message(error);
      }
    );

  }

// ------------------------------------------------------------------------------------------------------------




  $scope.initializeSearchUsers = function(searchDates){

    var users = [];
    if (searchDates.length < 1) {
      return users;
    }

    if($scope.model.usersIdSelected.length == 0){
       users = $scope.model.usersFilters;
    } else {
       for(var i = 0; i < $scope.model.usersIdSelected.length; i++){
        var id = $scope.model.usersIdSelected[i];
        for(var j = 0; j < $scope.model.users.length; j++){
          var idAux = $scope.model.users[j].id;
          if(id == idAux){
            users.push($scope.model.users[j]);
            break;
          }
        }
      }
    }

    return users;
  };

  $scope.initializeSearchDates = function(){
    var dates = [];

    if($scope.model.start != null){
      if($scope.model.end != null){
        dates = Utils.getDates($scope.model.start, $scope.model.end);
      } else {
        dates.push($scope.model.start);
      }

    } else if($scope.model.end != null) {
      dates.push($scope.model.end);

    } else {
      dates.push(new Date());
    }

    return dates;

  };

  $scope.checkDates = function(){
    if($scope.model.start == null){
      $scope.model.start = new Date();
    }

    if(($scope.model.end === null) || ($scope.model.start > $scope.model.end)){
      $scope.model.end =  new Date($scope.model.start);
    }

    $scope.model.start.setHours(0,0,0,0);
    $scope.model.end.setHours(23,59,59,999);
  };

  $scope.getUsersIds = function(users) {
    var ids = [];
    for (var i = 0; i < users.length; i++) {
      ids.push(users[i].id);
    }
    return ids;
  }

  $scope.formatJustification = function(justification) {
    justification.startDate = Utils.formatDate(new Date(justification.begin));
    justification.startTime = Utils.formatTime(new Date(justification.begin));
    justification.endDate = Utils.formatDate(new Date(justification.end));
    justification.endTime = Utils.formatTime(new Date(justification.end));
  };


  /**
   * Asignar "justifications" a los "assistances" previamente consultados
   */
  $scope.setJustifications = function(justifications) {

    // tiene las justificaciones que no machean con ninguna asistencia
    var auxJustifications = justifications.slice();

    for (var $i = 0; $i < justifications.length; $i++) {
      var j = justifications[$i];
      j.date = Utils.formatDate(new Date(j.begin));
      for (var $k = 0; $k < $scope.model.assistances.length; $k++) {
        var a = $scope.model.assistances[$k]
        //verifico que la fecha de la justificacion sea igual a la de la asistencia y que tenga el mismo usuario
        if (j != null && a.date == j.date && j.user_id == a.userId) {
          var index = auxJustifications.indexOf(j);
          auxJustifications.splice(index,1);
          a.justification = j;
          $scope.formatJustification(a.justification);
        }
      }
    }

    //creo una asistencia por cada justificacion que quedo pendiente, es decir que no corresponde a ninguna marcacion
    for (var $i = 0; $i < auxJustifications.length; $i++) {
      var j = auxJustifications[$i];
      var newAssistance = {};
      newAssistance.userId = j.user_id;
      newAssistance.start = new Date(j.begin);
      newAssistance = $scope.formatAssistance(newAssistance);
      newAssistance.start = null; //redefino en null la hora de inicio

      newAssistance.justification = j;
      $scope.formatJustification(j);
      $scope.model.assistances.push(newAssistance);
    }

    $scope.disabled = false;


    $scope.order('dateSort',false);//ordenamiento por defecto
    $scope.model.download = true;
  }






  /**
  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
  * CODIGO PORONGA A ARREGLAR. LO METO AHORA PORQUE ESTOY CANSADO Y PARA SOLUCIONAR EL TEMA DE LAS JUSTIFICAIONES
  */

  $scope.model.justificationNames = {
    'e0dfcef6-98bb-4624-ae6c-960657a9a741':'Ausente con aviso',
    '48773fd7-8502-4079-8ad5-963618abe725':'Compensatorio',
    'fa64fdbd-31b0-42ab-af83-818b3cbecf46':'Boleta de Salida',
    '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb':'Art 102',
    'b70013e3-389a-46d4-8b98-8e4ab75335d0':'Pre-Exámen',
    '76bc064a-e8bf-4aa3-9f51-a3c4483a729a':'Licencia Anual Ordinaria',
    '50998530-10dd-4d68-8b4a-a4b7a87f3972':'Resolución',
    'f9baed8a-a803-4d7f-943e-35c436d5db46':'Licencia Médica Corta Duración',
    'a93d3af3-4079-4e93-a891-91d5d3145155':'Licencia Médica Largo Tratamiento',
    'b80c8c0e-5311-4ad1-94a7-8d294888d770':'Licencia Médica Atención Familiar',
    '478a2e35-51b8-427a-986e-591a9ee449d8':'Justificado por Médico',
    '5ec903fb-ddaf-4b6c-a2e8-929c77d8256f':'Feriado',
    '874099dc-42a2-4941-a2e1-17398ba046fc':'Paro',
    'b309ea53-217d-4d63-add5-80c47eb76820':'Cumpleaños',
    '0cd276aa-6d6b-4752-abe5-9258dbfd6f09':'Duelo',
    'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b':'Donación de Sangre'
  };


  $scope.getJustificationName = function(id) {
    return $scope.model.justificationNames[id];
  }

  /*
    //////////////////////////////////////////////
    hasta aca es el codigo poronga que agregueee
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////
  */









  /**
   * En funcion de los datos del formulario se consultaran las justificaciones
   * @returns {undefined}
   */
  $scope.getJustifications = function() {
    var status = "APPROVED"; //se establece un valor de null para obtener todas las justificaciones
    var start = $scope.model.start; //fecha de inicio de la busqueda
    var end = $scope.model.end; //fecha de fin de la busqueda
    var usersId = $scope.usersIds; //id de usuarios a buscar
    Assistance.getJustificationRequestsByDate(status, $scope.usersIds, $scope.model.start, $scope.model.end,

      function ok(requests) {
        $scope.setJustifications(requests);
      },

      //en caso de error se vuelve a habilitar la busqueda
      function error() {
        $scope.disabled = false;
      }
    );
  };


  /**
   * Metodo principal de busqueda de datos
   */
  $scope.searchAssistance = function(){
    if(!$scope.disabled) {
      $scope.checkDates();
      $scope.disabled = true; //deshabilitar nuevas busquedas hasta no completar la actual

      $scope.model.assistances = [];
      $scope.searchDates = $scope.initializeSearchDates();

      if($scope.searchDates.length){
        var searchUsers = $scope.initializeSearchUsers($scope.searchDates); //si no existen usuarios seleccionados, se definen todos los usuarios

        $scope.usersIds = $scope.getUsersIds(searchUsers);
        Assistance.getAssistanceStatusByUsers($scope.usersIds, $scope.searchDates,
            function ok(response) {
              var assistances = response.assistances;
              $scope.model.base64 = response.base64;
              for (var i = 0; i < assistances.length; i++) {
                var assistance = assistances[i];
                var newAssistance = $scope.formatAssistance(assistance);

                if(assistance.userId != null){
                  $scope.model.assistances.push(newAssistance);
                }

              }

              $scope.getJustifications();

            },
            function error(){
              // decremento el contador
              $scope.disabled = false;
              Notifications.message(error);
              throw new Error(error);
            }
          );
      }
    }
  };



  $scope.formatAssistance = function(assistance) {
    var newAssistance = {};

    newAssistance.displayLogs = false;
    newAssistance.displayJustification = false;

    var date = new Date(assistance.date);
    newAssistance.date = Utils.formatDate(date);

    for(var i = 0; i < $scope.model.users.length; i++){
      var user = $scope.model.users[i];
      if(user.id == assistance.userId) {
        newAssistance.userId = assistance.userId;
        newAssistance.user = user.name + " " + user.lastname;
        break;
      }
    }

    newAssistance.dateSort = date;
    if(assistance.start != null){
      var start = new Date(assistance.start);
      newAssistance.dateSort = start;
      newAssistance.start = Utils.formatTime(start);
    };

    if(assistance.end != null){
      var end = new Date(assistance.end);
      newAssistance.end = Utils.formatTime(end);
    };

    newAssistance.logs = [];

    if (assistance.logs != null) {
      for(var i = 0; i < assistance.logs.length; i++){
        var date = new Date(assistance.logs[i]);
        var log = {};
        log.date = Utils.formatDate(date);
        log.time = Utils.formatTime(date);
        newAssistance.logs.push(log);
      }
    }

    if (assistance.workedMinutes != null) {
      newAssistance.workedTime = Utils.getTimeFromMinutes(assistance.workedMinutes);
    }

    if (assistance.status != null) {
      newAssistance.status = assistance.status;
    }

    return newAssistance;
  };


  /**
    * Seleccionar usuario
   */
  $scope.selectUser = function(user){
    var index = $scope.model.usersIdSelected.indexOf(user.id);
    if(index > -1){
      $scope.model.usersIdSelected.splice(index, 1);
    } else {
      $scope.model.usersIdSelected.push(user.id);
    }
  };

  $scope.isSelectedUser = function(user){
    var index = $scope.model.usersIdSelected.indexOf(user.id);
    if(index > -1){
      return true;
    } else {
      return false;
    }
  };

  $scope.showLogs = function(v,assistance) {
    assistance.displayLogs = v;
    assistance.displayJustification = false;
  };

  $scope.showJustifications = function(assistance) {
    assistance.displayLogs = false;
    assistance.displayJustification = !assistance.displayJustification;
  };

  $scope.isDisabled = function() {
    return ($scope.disabled) ;
  };


// ---------- EXPORTAR DATOS --------

  $scope.download = function() {
    console.log($scope.model.base64);
    if ($scope.model.base64 == null || $scope.model.base64 == '') {
      return;
    }
    var blob = Utils.base64ToBlob($scope.model.base64);
    window.saveAs(blob,'controlDeHorario.ods');
  }


}]);
