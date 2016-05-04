angular
  .module('mainApp')
  .controller('RequestCtrl', RequestCtrl);

RequestCtrl.inject = ['$scope', 'Login', 'Assistance', 'Users', '$location', '$timeout']

function RequestCtrl($scope, Login, Assistance, Users, $location, $timeout) {

  $scope.initialize = initialize;
  $scope.initializeFilters = initializeFilters;
  $scope.formatJustification = formatJustification;
  $scope.search = search;
  $scope.getJustTitle = getJustTitle;
  $scope.getJustName = getJustName;
  $scope.orderName = orderName;
  $scope.orderStatus = orderStatus;
  $scope.orderUserName = orderUserName;
  $scope.loadUsers = loadUsers;
  $scope.getName = getName;
  $scope.selectCompensatory = selectCompensatory;
  $scope.back = back;
  $scope.changeStatus = changeStatus;
  $scope.cancelJustification = cancelJustification;
  $scope.rejectJustification = rejectJustification;
  $scope.approveJustification = approveJustification;

  $scope.model = {
    userId: null,
    start: null,
    end: null,
    optionJustifications: null,
    justifications: [],
    users: {}
  }

  // PENDING, APPROVED, REJECTED, CANCELED
  $scope.status = {
    cancelado : 'CANCELED',
    pendiente: 'PENDING',
    aprobado: 'APPROVED',
    rechazado: 'REJECTED'
  }

  $scope.view = {
    optionsJustifications: [
      {style: 'solicitudesPersonales', description: 'MIS SOLICITUDES', value: false},
      // {style: 'solicitudesGrupo', description: 'MI GRUPO', value: true}
      {style: 'solicitudesPersonales', description: 'MI GRUPO', value: true}
    ],
    searching: false,
    reverseName: false,
    reverseUserName: false,
    reverseStatus: false,
    style: '',
    style_options: ['', 'seleccionSolicitud'],
    style2: '',
    style2_options: ['','solicitudSeleccionada']
  }

  const dayMillis = 24 * 60 * 60 * 1000;
  const limitDay = 6;

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.model.userId = '';
    Login.getSessionData()
      .then(function(s) {
          $scope.model.userId = s.user_id;
          $scope.initialize();
      }, function(err) {
        console.log("error");
      });
  });

  $scope.$on('finishCreationJEvent', function(event) {
    $timeout(function() {
      $scope.view.style = $scope.view.style_options[0];
      $scope.view.style2 = $scope.view.style2_options[0];
    }, 1500);
  })


  $scope.$watch(function() {return $scope.model.optionJustifications;}, function(o,n) {
    val = $scope.model.optionJustifications;
    $scope.view.style3 = (val != null && val.hasOwnProperty('style') && val.style != undefined) ? val.style : '';
    $scope.search();
  });

  $scope.$watch(function() {return $scope.model.start;}, function(o,n) {
    if (n == null) {
      $scope.model.start = o;
    }
    if ($scope.model.start == null && $scope.model.end == null) {
        $scope.initializeFilters();
    }

    $scope.model.start = ($scope.model.start == null) ? new Date($scope.model.end.getTime() - (limitDay * dayMillis))  : $scope.model.start;
    $scope.model.end = ($scope.model.end <= $scope.model.start) ? $scope.model.start : $scope.model.end;

  });

  $scope.$watch(function() {return $scope.model.end;}, function(o,n) {
    if (n == null) {
      $scope.model.end = o;
    }
    if ($scope.model.start == null && $scope.model.end == null) {
        $scope.initializeFilters();
    }

    $scope.model.end = ($scope.model.end == null) ? new Date($scope.model.start.getTime() + (limitDay * dayMillis))  : $scope.model.end;
    $scope.model.start = ($scope.model.start >= $scope.model.end) ? new Date($scope.model.end.getTime() - (limitDay * dayMillis))  : $scope.model.start;
  });

  function initialize() {
    $scope.model.optionJustifications = $scope.view.optionsJustifications[0];
    $scope.view.searching = false;
    $scope.model.justifications = [];
    $scope.initializeFilters();
    $scope.search();
  }

  function initializeFilters() {
    var now = new Date()
    // getDay obtiene el dia de la semana: 0->Domingo, 1->Lunes, ... , 6->Sábado
    var day = (now.getDay() - 1 < 0) ? limitDay : now.getDay() - 1;

    var start = new Date(now.getTime() - (day * dayMillis));

    end = new Date(start.getTime() + (limitDay * dayMillis));

    $scope.model.start = start;
    $scope.model.end = end;
  }

  function loadUsers(ids) {
    $scope.model.users = {};
    if (ids.length <= 0) {
      return;
    }
    Users.findById(ids).then(function(users) {
      for (var i = 0; i < users.length; i++) {
        user = users[i];
        $scope.model.users[user['id']] = user;
      }
    }, function(error) {
      console.log('Error al buscar el usuario')
    });
  }

  function changeStatus(just, status) {
    Assistance.changeStatus(just, status).then(function(data) {
      $scope.search();
    }, function(error) {
      console.log('error');
    });
  }

  function cancelJustification(j) {
    $scope.changeStatus(j.just, $scope.status.cancelado);
  }

  function approveJustification(j) {
    $scope.changeStatus(j.just, $scope.status.aprobado);
  }

  function rejectJustification(j) {
    $scope.changeStatus(j.just, $scope.status.rechazado);
  }

  function getName(id) {
    if ($scope.model.users[id] == undefined) {
      return "No Definido";
    }
    return $scope.model.users[id].lastname + " " + $scope.model.users[id].name;
  }

  function search() {
    if ($scope.model.start == null || $scope.model.end == null) {
      return
    }
    $scope.view.searching = true;
    $scope.view.style3 = 'cargandoSolicitudes';
    Assistance.getJustifications($scope.model.userId, $scope.model.start, $scope.model.end, $scope.model.optionJustifications.value).then(function(data) {
      $scope.view.searching = false;
      $scope.view.style3 = $scope.model.optionJustifications.style;
      justifications = [];
      userIds = Object.keys(data);
      $scope.loadUsers(userIds);
      for (userId in data) {
        var just = data[userId];
        for (var i = 0; i < just.length; i++) {
          justifications.push($scope.formatJustification(just[i]));
        }
      }
      console.log(justifications);
      $scope.model.justifications = justifications;
      $scope.orderName();
    }, function(error) {
      $scope.view.searching = false;
      $scope.view.style3 = $scope.model.optionJustifications.style;
      console.log('Error al buscar las justificaciones');
    });
  }


  function formatJustification(just) {
    var j = {};
    j.userId = just.userId;
    j.name = just.identifier;
    j.type = just.type;
    j.start = (just.hasOwnProperty('start') && just.start != undefined) ? new Date(just.start) : undefined;

    if (just.hasOwnProperty('date') && just.date != undefined) {
      dateStr = just.date.substr(0,10).replace('-','/').replace('-','/');
      j.date = new Date(dateStr);
    } else {
      j.date = undefined;
    }
    j.end = (just.hasOwnProperty('end') && just.end != undefined) ? new Date(just.end) : undefined;
    j.status = just.status.status;
    j.classType = just.classType;
    j.just = just;
    return j;
  }

  function getJustTitle(just) {
    v = (just.hasOwnProperty('type') && just.type != undefined) ? just.type : just.name;
    return v
  }

  function getJustName(just) {
    return (just.hasOwnProperty('type') && just.type != undefined) ? just.name : '';
  }

  function compareName(a, b) {
    aName = (a.hasOwnProperty('type') && a.type != undefined) ? a.type + ' ' + a.name : a.name;
    bName = (b.hasOwnProperty('type') && b.type != undefined) ? b.type + ' ' + b.name : b.name;
    return (aName < bName) ? -1 : (aName > bName ? 1 : 0);
  }

  function compareUserName(a, b) {
    aName = $scope.getName(a.userId);
    bName = $scope.getName(b.userId);
    return aName < bName ? -1 : (aName > bName ? 1 : 0)
  }

  function compareDate(a, b) {
    aDate = (a.hasOwnProperty('date') && a.date != undefined) ? a.date : a.start;
    bDate = (b.hasOwnProperty('date') && b.date != undefined) ? b.date : b.start;
    return aDate - bDate;
  }

  function orderName() {
    if ($scope.view.reverseName) {
      $scope.model.justifications.sort(function(a, b) {
        value = compareName(a, b);
        if (value == 0) {
          value = compareUserName(a, b);
        }
        if (value == 0) {
          value = compareDate(b, a);
        }
        return value;
      });
    } else {
      $scope.model.justifications.sort(function(a, b) {
        value = compareName(b, a);
        if (value == 0) {
          value = compareUserName(a, b);
        }
        if (value == 0) {
          value = compareDate(b, a);
        }
        return value;
      });
    }
    $scope.view.reverseName = !$scope.view.reverseName;
  }

  function orderStatus() {
    if ($scope.view.reverseStatus) {
      $scope.model.justifications.sort(function(a, b) {
        value = a.status - b.status;
        if (value == 0) {
          value = compareUserName(a, b);
        }
        if (value == 0) {
          value = compareDate(b, a);
        }
        return value;
      });
    } else {
      $scope.model.justifications.sort(function(a, b) {
        value = b.status - a.status
        if (value == 0) {
          value = compareUserName(a, b);
        }
        if (value == 0) {
          value = compareDate(b, a);
        }
        return value;
      });
    }
    $scope.view.reverseStatus = !$scope.view.reverseStatus;
  }

  function orderUserName() {
    if ($scope.view.reverseUserName) {
      $scope.model.justifications.sort(function(a, b) {
        value = compareUserName(a, b);
        if (value == 0) {
          value = compareDate(b, a);
        }
        return value;
      });
    } else {
      $scope.model.justifications.sort(function(a, b) {
        value = compareUserName(b, a);
        if (value == 0) {
          value = compareDate(b, a);
        }
        return value;
      });
    }
    $scope.view.reverseUserName = !$scope.view.reverseUserName;
  }


  function selectCompensatory() {
    $scope.view.style2 = $scope.view.style2_options[1];
    $scope.$broadcast('selectCompensatoryEvent', $scope.model.userId);
  }

  $scope.$on('closeRequestEvent', function(e) {
    $scope.view.style = $scope.view.style_options[0];
    $scope.view.style2 = $scope.view.style2_options[0];
  })

  function back() {
    $scope.view.style = $scope.view.style_options[0];
    $scope.view.style2 = $scope.view.style2_options[0];
  }


}
