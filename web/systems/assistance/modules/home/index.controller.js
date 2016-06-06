angular
  .module('mainApp')
  .controller('HomeCtrl', HomeCtrl);

HomeCtrl.inject = ['$rootScope', '$scope', 'Users', 'Login', 'Positions', 'Assistance']

function HomeCtrl($rootScope, $scope, Users, Login, Positions, Assistance) {

  $scope.initialize = initialize;
  $scope.loadUser = loadUser;
  $scope.getUserPhoto = getUserPhoto;
  $scope.loadPosition = loadPosition;
  $scope.loadAssistanceData = loadAssistanceData;

  $scope.model = {
    user: null,
    userId: '',
    date : null,
    assistanceData: {
      'workedAssistanceData': []
    }
  }

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.model.userId = '';
    Login.getSessionData()
      .then(function(s) {
          $scope.model.userId = s.user_id;
          $scope.initialize();
      }, function(err) {
        console.log(err);
      });
  });

  $scope.$watch(function() {return $scope.model.date;}, function(o,n) {
    $scope.loadAssistanceData();
  });

  function initialize() {
    $scope.model.date = new Date();
    $scope.loadUser();
    $scope.loadPosition();
  }

  function loadPosition() {
    Positions.getPosition([$scope.model.userId]).then(function(positions) {
      $scope.model.position = (positions.length > 0) ? positions[0] : null;
    }, function(error) {
      console.log('Error al buscar el cargo')
    });
  }

  function loadUser() {
    Users.findById([$scope.model.userId]).then(function(users) {
      $scope.model.user = (users.length > 0) ? users[0] : null;
    }, function(error) {
      console.log('Error al buscar el usuario')
    });
  }

  function getUserPhoto() {
    if ($scope.model.user == null || $scope.model.user.photo == null || $scope.model.user.photo == '') {
      return "../login/modules/img/imgUser.jpg";
    } else {
      return "/c/files.py?i=" + $scope.model.user.photo;
    }
  }

  function loadAssistanceData() {
    if ($scope.model.date == null || $scope.model.userId == null) {
      return
    }
    $scope.model.date.setHours(0);
    $scope.model.date.setMinutes(0);
    $scope.model.date.setSeconds(0);
    Assistance.getAssistanceData([$scope.model.userId], $scope.model.date, $scope.model.date).then(function(data) {
      $scope.model.assistanceData = {};
      if (data.length <= 0) {
        return;
      }
      sWp = data[0];
      $scope.model.assistanceData.workedAssistanceData = sWp.workedAssistanceData;
      $scope.model.assistanceData.scheduleActual = {};
      $scope.model.assistanceData.logsActual = {};
      $scope.model.assistanceData.office = (sWp.offices == undefined || sWp.offices == null || sWp.offices.length <= 0) ? 'No tiene' : sWp.offices[0].name
      for (var i = 0; i < sWp.workedAssistanceData.length; i++) {
          selectDateStr = $scope.model.date.toISOString().substring(0, 10);
          dateStr = sWp.workedAssistanceData[i].date;
          if (selectDateStr == dateStr) {
            wActual = sWp.workedAssistanceData[i];

            sStart = (wActual.scheduleStart == null || wActual.scheduleStart == '') ? null : new Date(wActual.scheduleStart);
            sEnd = (wActual.scheduleEnd == null || wActual.scheduleEnd == '') ? null : new Date(wActual.scheduleEnd);
            $scope.model.assistanceData.scheduleActual = {'start' : sStart, 'end': sEnd};

            console.log(wActual.scheduleStart);

            lStart = (wActual.logStart == null || wActual.logStart == '') ? null : new Date(wActual.logStart);
            lEnd = (wActual.logEnd == null || wActual.logEnd == '') ? null : new Date(wActual.logEnd);
            $scope.model.assistanceData.logActual = {'start' : lStart, 'end': lEnd};
          }
      }
      console.log($scope.model.assistanceData);
    }, function(error) {
      console.log("Error al obtener los datos de asistencia");
    })
  }


}
