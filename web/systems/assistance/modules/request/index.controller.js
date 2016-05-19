angular
  .module('mainApp')
  .controller('RequestCtrl', RequestCtrl);

RequestCtrl.inject = ['$scope', 'Login', 'Assistance', 'Users', 'Office', '$location', '$timeout']

function RequestCtrl($scope, Login, Assistance, Users, Office, $location, $timeout) {

  $scope.initialize = initialize;
  $scope.initializeFilters = initializeFilters;
  $scope.loadOffices = loadOffices;
  $scope.formatJustification = formatJustification;
  $scope.search = search;
  $scope.getJustTitle = getJustTitle;
  $scope.getJustName = getJustName;
  $scope.getSelectedOrderStatus = getSelectedOrderStatus;
  $scope.getSelectedOrderName = getSelectedOrderName;
  $scope.getSelectedOrderType = getSelectedOrderType;
  $scope.order = order;
  $scope.sortName = sortName;
  $scope.orderName = orderName;
  $scope.orderStatus = orderStatus;
  $scope.sortStatus = sortStatus;
  $scope.sortUserName = sortUserName;
  $scope.orderUserName = orderUserName;
  $scope.loadUsers = loadUsers;
  $scope.getName = getName;
  $scope.selectCompensatory = selectCompensatory;
  $scope.selectInformedAbsence = selectInformedAbsence;
  $scope.selectOTWithReturn = selectOTWithReturn;
  $scope.selectOTWithoutReturn = selectOTWithoutReturn;
  $scope.selectUniversityPreExam = selectUniversityPreExam;
  $scope.selectA102 = selectA102;
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
    optionsJustifications: [],
    optionGroupJustifications: {style: 'solicitudesGrupo', description: 'MI GRUPO', value: true},
    optionMyJustifications: {style: 'solicitudesPersonales', description: 'MIS SOLICITUDES', value: false},
    searching: false,
    reverseName: false,
    reverseUserName: false,
    reverseStatus: false,
    order: '',
    order_type: 'type',
    order_name: 'name',
    order_status: 'status',
    style: '',
    style_options: ['', 'seleccionSolicitud'],
    style2: '',
    style2_options: ['','solicitudSeleccionada'],
    displayRequest: '',
    displayRequestOptions: ['', 'compensatory', 'informedAbsence', 'oTWithReturn', 'oTWithoutReturn', 'universityPreExam', 'a102']
  }


  const dayMillis = 24 * 60 * 60 * 1000;
  const limitDay = 7;

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
      $scope.search();
    }, 1500);
  })


  $scope.$watch(function() {return $scope.model.optionJustifications;}, function(o,n) {
    val = $scope.model.optionJustifications;
    $scope.view.style3 = (val != null && val.hasOwnProperty('style') && val.style != undefined) ? val.style : '';
    if (val != null) {
      $scope.search();
    }
  });

  $scope.$watch(function() {return $scope.model.start;}, function(o,n) {
    if (n == null) {
      $scope.model.start = o;
    }
    if ($scope.model.start == null && $scope.model.end == null) {
        $scope.initializeFilters();
    }

    $scope.model.start = ($scope.model.start == null) ? new Date($scope.model.end) : $scope.model.start;
    $scope.model.end = ($scope.model.end < $scope.model.start) ? new Date($scope.model.start) : $scope.model.end;

  });

  $scope.$watch(function() {return $scope.model.end;}, function(o,n) {
    if (n == null) {
      $scope.model.end = o;
    }
    if ($scope.model.start == null && $scope.model.end == null) {
        $scope.initializeFilters();
    }

    $scope.model.end = ($scope.model.end == null) ? new Date($scope.model.start)  : $scope.model.end;
    $scope.model.start = ($scope.model.start > $scope.model.end) ? new Date($scope.model.end)  : $scope.model.start;
  });

  function initialize() {
    $scope.view.searching = false;
    $scope.model.justifications = [];
    $scope.initializeFilters();
    $scope.loadOffices();
  }

  function initializeFilters() {
    var now = new Date()
    var start = new Date(now.getTime() - (limitDay * dayMillis));

    end = new Date(now.getTime() + (limitDay * dayMillis));

    $scope.model.start = start;
    $scope.model.end = end;

    $scope.view.order = $scope.view.order_status;
  }

  function loadOffices() {
    $scope.view.optionsJustifications = [];
    $scope.view.optionsJustifications.push($scope.view.optionMyJustifications);
    $scope.model.optionJustifications = $scope.view.optionsJustifications[0];

    Office.getOfficesByUserRole($scope.model.userId, true, 'autoriza').then(function(ids) {
      if (ids.length > 0) {
        $scope.view.optionsJustifications.push($scope.view.optionGroupJustifications);
      }
    }, function(error) {
      console.log(error);
    });
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
      $scope.model.justifications = justifications;
      $scope.order();

    }, function(error) {
      $scope.view.searching = false;
      $scope.view.style3 = $scope.model.optionJustifications.style;
      console.log('Error al buscar las justificaciones');
    });
  }

  function order() {
    switch ($scope.view.order) {
      case ($scope.view.order_type): $scope.orderName(); break;
      case ($scope.view.order_name): $scope.orderUserName(); break;
      case ($scope.view.order_status): $scope.orderStatus(); break;
    }
  }

  function getSelectedOrderStatus() {
    return $scope.view.order == $scope.view.order_status;
  }

  function getSelectedOrderName() {
    return $scope.view.order == $scope.view.order_name;
  }

  function getSelectedOrderType() {
    return $scope.view.order == $scope.view.order_type;
  }

  function formatJustification(just) {
    var j = {};
    j.userId = just.userId;
    j.name = just.identifier;
    j.typeName = just.typeName;
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
    v = (just.hasOwnProperty('typeName') && just.typeName != undefined) ? just.typeName : just.name;
    return v
  }

  function getJustName(just) {
    return (just.hasOwnProperty('typeName') && just.typeName != undefined) ? just.name : '';
  }

  function compareName(a, b) {
    aName = (a.hasOwnProperty('typeName') && a.typeName != undefined) ? a.typeName + ' ' + a.name : a.name;
    bName = (b.hasOwnProperty('typeName') && b.typeName != undefined) ? b.typeName + ' ' + b.name : b.name;
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

  function sortName() {
    $scope.view.reverseName = !$scope.view.reverseName;
    $scope.orderName();
  }

  function orderName() {
    $scope.view.reverseName = ($scope.view.order != $scope.view.order_type) ? false : $scope.view.reverseName;
    $scope.view.order = $scope.view.order_type;
    if (!$scope.view.reverseName) {
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
  }

  function sortStatus() {
    $scope.view.reverseStatus = !$scope.view.reverseStatus;
    $scope.orderStatus();
  }

  function orderStatus() {
    $scope.view.reverseStatus = ($scope.view.order != $scope.view.order_status) ? false : $scope.view.reverseStatus;
    $scope.view.order = $scope.view.order_status;
    if (!$scope.view.reverseStatus) {
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
  }

  function sortUserName() {
    $scope.view.reverseUserName = !$scope.view.reverseUserName;
    $scope.orderUserName();
  }

  function orderUserName() {
    $scope.view.reverseUserName = ($scope.view.order != $scope.view.order_name) ? false : $scope.view.reverseUserName;
    $scope.view.order = $scope.view.order_name;
    if (!$scope.view.reverseUserName) {
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
  }


  function selectCompensatory() {
    $scope.view.style2 = $scope.view.style2_options[1];
    $scope.view.displayRequest = $scope.view.displayRequestOptions[1];
    $scope.$broadcast('selectCompensatoryEvent', $scope.model.userId);
  }

  function selectInformedAbsence() {
    $scope.view.style2 = $scope.view.style2_options[1];
    $scope.view.displayRequest = $scope.view.displayRequestOptions[2];
    $scope.$broadcast('selectInformedAbsenceEvent', $scope.model.userId);
  }

  function selectOTWithReturn() {
    $scope.view.style2 = $scope.view.style2_options[1];
    $scope.view.displayRequest = $scope.view.displayRequestOptions[3];
    $scope.$broadcast('selectOTWithReturnEvent', $scope.model.userId);
  }

  function selectOTWithoutReturn() {
    $scope.view.style2 = $scope.view.style2_options[1];
    $scope.view.displayRequest = $scope.view.displayRequestOptions[4];
    $scope.$broadcast('selectOTWithoutReturnEvent', $scope.model.userId);
  }

  function selectUniversityPreExam() {
    $scope.view.style2 = $scope.view.style2_options[1];
    $scope.view.displayRequest = $scope.view.displayRequestOptions[5];
    $scope.$broadcast('selectUniversityPreExamEvent', $scope.model.userId);
  }

  function selectA102() {
    $scope.view.style2 = $scope.view.style2_options[1];
    $scope.view.displayRequest = $scope.view.displayRequestOptions[6];
    $scope.$broadcast('selectA102Event', $scope.model.userId);
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
