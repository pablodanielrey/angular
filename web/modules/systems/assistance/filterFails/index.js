
app.controller('FilterFailsCtrl', ["$scope", "$timeout", "$window", "Assistance", "Module", "Notifications", "Users",  "Utils", function($scope, $timeout, $window, Assistance, Module, Notifications, Users, Utils) {

  /**
   * Variables del modelo
   */
  $scope.model = {
    sessionUserId: null, //id de sesion de usuario

    //seleccion de usuario
    displayUsersList: false,  //flag para controlar si se debe mostrar la lista de usuarios
    selectedUser: null,  //usuario seleccionado
    searchUser: null,  //usuario buscado
    users: [],        //usuarios consultados para seleccionar
    usersSelectionDisable: true, //flag para indicar que se debe deshabilitar la seleccion
    
    //seleccion de oficina
    displayOfficesList: false,  //flag para controlar si se debe mostrar la lista de usuarios
    selectedOffice: null,  //usuario seleccionado
    searchOffice: null,  //usuario buscado
    offices: [],        //usuarios consultados para seleccionar
    officesSelectionDisable: true, //flag para indicar que se debe deshabilitar la seleccion
    
    begin:new Date(),
    end:new Date(),
    type:null,
    count:null,
    periodicity:null
  };

  /******************
   * INICIALIZACION *
   ******************/
  $timeout(function() {
    Module.authorize('ADMIN-ASSISTANCE,USER-ASSISTANCE',
      function(response){
        if (response !== 'granted') {
          Notifications.message("Acceso no autorizado");
          $window.location.href = "/#/logout";
        }
        $scope.model.sessionUserId = Module.getSessionUserId();
        $scope.loadUsers();
        $scope.loadOffices();
      },
      function(error){
        Notifications.message(error);
        $window.location.href = "/#/logout";
      }
    );
  }, 0);



  /******************************************************
   * METODOS CORRESPONDIENTES A LA SELECCION DE USUARIO *
   ******************************************************/
  /**
   * Cargar usuarios de la lista
   */
  $scope.loadUsers = function(){
    Assistance.getUsersInOfficesByRole('autoriza',
      function(users) {
        $scope.model.users = [];

        for (var i = 0; i < users.length; i++) {
          Users.findUser(users[i],
            function(user) {
              $scope.model.users.push(user);
            },
            function(error) {
              Notifications.message(error);
            });
        }
        
        $scope.model.usersSelectionDisable = false;
      },
      function(error){
        Notifications.message(error);
      }
    );
  };
  
  /**
   * Debe ser mostrada la lista de usuarios?
   */
  $scope.isUsersListDisplayed = function() {
    return $scope.model.displayUsersList;
  };
  
  /**
   * Mostrar lista de usuarios
   */
  $scope.displayUsersList = function(){
    $scope.model.selectedUser = null;
    $scope.model.searchUser = null;
    $scope.model.displayUsersList = true;
    $scope.model.usersSelectionDisable = false;
  };
  
  /**
   * Esta seleccionado un usuario?
   * @returns {Boolean}
   */
  $scope.isUserSelected = function(){
    return ($scope.model.selectedUser !== null);
  };


  /**
   * Seleccionar usuario
   * @param {usuario} user Usuario seleccionado
   */
  $scope.selectUser = function(user){
    $scope.model.displayUsersList = false;
    $scope.model.selectedUser = user;
    $scope.model.searchUser = $scope.model.selectedUser.name + " " + $scope.model.selectedUser.lastname;
    $scope.model.selectedOffice = null;
    $scope.model.searchOffice = null;

  };
  
  
  
  
  /******************************************************
   * METODOS CORRESPONDIENTES A LA SELECCION DE OFICINA *
   ******************************************************/
  /**
   * Cargar oficinas
   */
  $scope.loadOffices = function(){
    Assistance.getOfficesByUserRole($scope.model.sessionUserId, 'autoriza', true,
      function(offices) {
        $scope.model.offices = offices;
        $scope.model.officesSelectionDisable = false;
      },
      function(error){
        Notifications.message(error);
      }
    );
  };
  
  /**
   * Debe ser mostrada la lista de oficinas?
   */
  $scope.isOfficesListDisplayed = function() {
    return $scope.model.displayOfficesList;
  };
  
  /**
   * Mostrar lista de oficinas
   */
  $scope.displayOfficesList = function(){
    $scope.model.selectedOffice = null;
    $scope.model.searchOffice = null;
    $scope.model.displayOfficesList = true;
    $scope.model.officesSelectionDisable = false;
  };
  
  /**
   * Esta seleccionada una oficina?
   * @returns {Boolean}
   */
  $scope.isOfficeSelected = function(){
    return ($scope.model.selectedOffice !== null);
  };


  /**
   * Seleccionar oficina
   * @param {office} office Oficina seleccionada
   */
  $scope.selectOffice = function(office){
    $scope.model.displayOfficesList = false;
    $scope.model.selectedOffice = office;
    $scope.model.searchOffice = $scope.model.selectedOffice.name;
    $scope.model.selectedUser = null;
    $scope.model.searchUser = null;
  };
  
  
  
  $scope.formatDates = function() {
    if(!$scope.model.begin) $scope.model.begin = new Date();
    $scope.model.begin.setHours(0);
    $scope.model.begin.setMinutes(0);
    $scope.model.begin.setSeconds(0);
    if((!$scope.model.end) || ($scope.model.end < $scope.model.begin)) $scope.model.end = new Date($scope.model.begin);
    $scope.model.end.setHours(23);
    $scope.model.end.setMinutes(59);
    $scope.model.end.setSeconds(59);
  };
  
  
  
  $scope.checkSubmit = function(){
    return false;
  };
  
  
  
  
  
  $scope.search = function() {
    $scope.model.searching = true;
    $scope.model.assistanceFails = [];
    $scope.formatDates();
    
    var filter = {
      userId: ($scope.model.selectedUser !== null) ? $scope.model.selectedUser.id : null,
      officeId: ($scope.model.selectedOffice !== null) ? $scope.model.selectedOffice.id : null,
      begin: $scope.model.begin,
      end: $scope.model.end,
      type: $scope.model.type,
      count: $scope.model.count,
      periodicity: $scope.model.periodicity
    };
    
    Assistance.getFailsByFilter(filter,
      function(response) {
        $scope.model.base64 = response.base64;

        for (var i = 0; i < response.response.length; i++) {

          var r = response.response[i];

          r.justification = {name:''};
          if ((r.fail.justifications != undefined) && (r.fail.justifications != null) && (r.fail.justifications.length > 0)) {
            var just = Utils.getJustification(r.fail.justifications[0].justification_id);
            just.begin = r.fail.justifications[0].begin;
            r.justification = just;
          }

          var date = new Date(r.fail.date);
          r.fail.dateFormat = Utils.formatDate(date);
          r.fail.dateExtend = Utils.formatDateExtend(date);
          r.fail.dayOfWeek = {};
          r.fail.dayOfWeek.name = Utils.getDayString(date);
          r.fail.dayOfWeek.number = date.getDay();

          if (r.fail.startSchedule || r.fail.endSchedule) {
            r.fail.dateSchedule = (r.fail.startSchedule) ? r.fail.startSchedule : r.fail.endSchedule;
            r.fail.dateSchedule = Utils.formatTime(new Date(r.fail.dateSchedule));
          }

          if (r.fail.start || r.fail.end) {
            r.fail.wh = (r.fail.start) ?  new Date(r.fail.start) : new Date(r.fail.end);
            r.fail.wh =  Utils.formatTime(r.fail.wh);
          }

          if (r.fail.seconds) {
            var hoursDiff = Math.floor((r.fail.seconds / 60) / 60);
            var minutesDiff = Math.floor((r.fail.seconds / 60) % 60);
            r.fail.diff = ('0' + hoursDiff).substr(-2) + ":" + ('0' + minutesDiff).substr(-2);
          }

          if (r.fail.whSeconds) {
            var hours = Math.floor((r.fail.whSeconds / 60) / 60);
            var minutes = Math.floor((r.fail.whSeconds / 60) % 60);
            r.fail.whs = ('0' + hours).substr(-2) + ":" + ('0' + minutes).substr(-2);
          } else {
            r.fail.whs = '00:00';
          }

          $scope.model.assistanceFails.push(r);
        }
        $scope.order(['fail.dateExtend','user.lastname','user.name'],false);//ordenamiento por defecto
        $scope.model.searching = false;
      },
      function(error) {
        $scope.model.searching = false;
        Notifications.message(error);
      }

    );
  };
  
  
  

}]);
