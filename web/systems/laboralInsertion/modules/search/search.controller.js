angular
  .module('mainApp')
  .controller('SearchCtrl', SearchCtrl);

SearchCtrl.$inject = ['$rootScope','$scope','$location', '$window', 'Notifications','LaboralInsertion', 'Login', 'Utils', 'Users', '$wamp'];

function SearchCtrl($rootScope, $scope, $location, $window, Notifications, LaboralInsertion, Login, Utils, Users, $wamp) {

  $scope.model = {
    inscriptions: [],
    selected: 0,
    users: [],
    data: [],
    currentScreen: '',
    companies: [
      {'name':'Cervecería Quilmes',
       'url':'./img/logos/quilmes.jpg',
       'emails':[
         {'email':'pablo@econo.unlp.edu.ar'},
         {'email':'prueba@econo.unlp.edu.ar'}
       ]},
      {'name':'Seguros Rivadavia',
       'url':'./img/logos/sr.jpg',
       'emails':[
         {'email':'pablo@econo.unlp.edu.ar'},
         {'email':'prueba@econo.unlp.edu.ar'}
       ]}
    ],
    company: null,
    emails: []
  };

  $scope.getCurrentScreen = function() {
    return $scope.model.currentScreen;
  }

  $scope.selectFilters = function() {
    $scope.model.currentScreen = "screenFilters";
  }

  $scope.selectInscriptions = function() {
    $scope.model.currentScreen = "";
  }

  $scope.selectCompany = function() {
    if ($scope.model.selected <= 0) {
      return;
    }
    $scope.model.currentScreen = "screenBussines screenSelectBusiness";
  }

  $scope.confirmMailToCompany = function(c) {
    $scope.model.currentScreen = "screenBussines screenSendBusiness";
    $scope.model.company = c;
  }

  $scope.sendMailToCompany = function() {
    $scope.model.currentScreen = "screenBussines screenSending";
    //  $scope.model.company = c;

    var selectedInscriptions = [];
    for (i = 0; i < $scope.model.inscriptions.length; i++) {
      if ($scope.model.inscriptions[i].selected) {
        selectedInscriptions.push($scope.model.inscriptions[i]);
      }
    }

    LaboralInsertion.sendEmailToCompany(selectedInscriptions, $scope.model.company).then(
      function() {
        console.log('enviado');
      },
      function(err) {
        $scope.confirmMailToCompany($scope.model.company);
        console.log(err);
      }
    )
  }

  $scope.mailToCompanySent = function(emails) {
    $scope.model.currentScreen = "screenBussines screenSent";
    $scope.model.emails = emails;
    console.log('mail enviado ok');
  }

  /*
    Calcula la cantidad de seleccionados
  */
  $scope.getSelectedNumber = function() {
    $scope.model.selected = 0;
    for (i = 0; i < $scope.model.inscriptions.length; i++) {
      if ($scope.model.inscriptions[i].selected) {
        $scope.model.selected = $scope.model.selected + 1;
      }
    }
  }

  /*
    Selecciono una inscripcion para ser enviado por correo a una empresa
  */
  $scope.selectInscription = function(id) {
    for (i = 0; i < $scope.model.users.length; i++) {
      if ($scope.model.inscriptions[i].id == id) {
        $scope.model.inscriptions[i].selected = !$scope.model.inscriptions[i].selected;
        $scope.getSelectedNumber();
      }
    }
  }

  /*
    Chequea si una inscripcion esta seleccionado para ser enviado a una empresa.
  */
  $scope.isSelected = function(id) {
    for (i = 0; i < $scope.model.inscriptions.length; i++) {
      if ($scope.model.inscriptions[i].id == id) {
        if ($scope.model.inscriptions[i].selected == undefined) {
          return false;
        }
        return $scope.model.inscriptions[i].selected;
      }
    }
    return false;
  }

  /*
    funciones para obtener datos de la persona identificada por el id.
  */
  $scope.getName = function(id) {
    for (i = 0; i < $scope.model.users.length; i++) {
      if ($scope.model.users[i].id == id) {
        return $scope.model.users[i].lastname + " " + $scope.model.users[i].name;
      }
    }
    return 'No Encontrado';
  }

  $scope.getResidence = function(id) {
    for (i = 0; i < $scope.model.users.length; i++) {
      if ($scope.model.users[i].id == id) {
        return $scope.model.users[i].residence_city;
      }
    }
    return 'No Encontrado';
  }

  $scope.getCity = function(id) {
    for (i = 0; i < $scope.model.users.length; i++) {
      if ($scope.model.users[i].id == id) {
        return $scope.model.users[i].city;
      }
    }
    return 'No Encontrado';
  }

  $scope.getDni = function(id) {
    for (i = 0; i < $scope.model.users.length; i++) {
      if ($scope.model.users[i].id == id) {
        return $scope.model.users[i].dni;
      }
    }
    return 'No Encontrado';
  }

  $scope.getGenre = function(id) {
    for (i = 0; i < $scope.model.users.length; i++) {
      if ($scope.model.users[i].id == id) {
        return $scope.model.users[i].genre;
      }
    }
    return 'No Encontrado';
  }

  $scope.getTravel = function(i) {
    if (i.travel) {
      return "Sí";
    } else {
      return "No";
    }
  }

  $scope.getMail = function(id) {
    for (i = 0; i < $scope.model.data.length; i++) {
      if ($scope.model.data[i].id == id) {
        if ($scope.model.data[i].email != null) {
          return $scope.model.data[i].email.email;
        } else {
          return "No Definido";
        }
      }
    }
    return 'No Encontrado';
  }

  $scope.getEnglish = function(id) {
    for (i = 0; i < $scope.model.data.length; i++) {
      if ($scope.model.data[i].id == id) {
        if ($scope.model.data[i].languages.length > 0) {
          for (a = 0; a < $scope.model.data[i].languages.length; a++) {
            if ($scope.model.data[i].languages[a].name == 'Inglés') {
              return $scope.model.data[i].languages[a].level;
            }
          }
          return "No";
        } else {
          return "No";
        }
      }
    }
    return 'No Encontrado';
  }

  $scope.getLanguagesOther = function(id) {
    for (i = 0; i < $scope.model.data.length; i++) {
      if ($scope.model.data[i].id == id) {
        if ($scope.model.data[i].languages.length > 0) {
          for (a = 0; a < $scope.model.data[i].languages.length; a++) {
            if ($scope.model.data[i].languages[a].name != 'Inglés') {
              //return $scope.model.data[i].languages[a].name;
              return "Sí";
            }
          }
          return "No";
        } else {
          return "No";
        }
      }
    }
    return 'No Encontrado';
  }

  // calcula la edad a partir de la fecha de nac.
  // referencias http://stackoverflow.com/questions/4060004/calculate-age-in-javascript
  $scope._calculateAge = function(birthday) { // birthday is a date
      var ageDifMs = Date.now() - birthday.getTime();
      var ageDate = new Date(ageDifMs); // miliseconds from epoch
      return Math.abs(ageDate.getUTCFullYear() - 1970);
  }

  $scope.getAge = function(id) {
    for (i = 0; i < $scope.model.users.length; i++) {
      if ($scope.model.users[i].id == id) {
        date = new Date($scope.model.users[i].birthdate);
        if (date != null) {
          return $scope._calculateAge(date);
        } else {
          return 'nc';
        }
      }
    }
    return 'No Encontrado';
  }

  $scope.getDate = function(d) {
    d2 = new Date(d);

    day = d2.getDate()
    sday = '' + day;
    if (day <= 9) {
      sday = '0' + day;
    }

    month = d2.getMonth() + 1;
    smonth = '' + month;
    if (month <= 9) {
      smonth = '0' + month;
    }
    return sday + '/' + smonth + '/' + d2.getFullYear();
  }

  /*
    Obtiene la info de los usuarios
  */
  $scope.getUsers = function(ins) {
    for (i = 0; i < ins.length; i++) {
      //console.log('Buscando usuario ' + ins[i].user_id);
      Users.findById(ins[i].user_id).then(function(user) {
        $scope.model.users.push(user);
        //console.log(user);
      }, function(err) {
        console.log(err);
      });
    }
  }

  /*
    Obtiene la info que tiene ese usuario de las pasantias
  */
  $scope.getUserData = function(ins) {
    for (i = 0; i < ins.length; i++) {
      //console.log('Buscando usuario ' + ins[i].user_id);
      LaboralInsertion.findByUser(ins[i].user_id).then(function(data) {
        $scope.model.data.push(data);
        //console.log(data);
      }, function(err) {
        console.log(err);
      });
    }
  }


  $scope.initialize = function() {

    // me registro al evento de envío de mails a las empresas.
    $wamp.subscribe('system.laboralInsertion.COMPANYSENDED', $scope.mailToCompanySent);

    LaboralInsertion.findAllInscriptions().then(function(ins) {
      $scope.model.inscriptions = ins;
      $scope.getUsers(ins);
      $scope.getUserData(ins);
      //console.log($scope.model.inscriptions);
    }, function(err) {
      console.log(err);
    });
  }

  $rootScope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

}
