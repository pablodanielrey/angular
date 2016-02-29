angular
  .module('mainApp')
  .controller('SearchCtrl', SearchCtrl);

SearchCtrl.$inject = ['$rootScope','$scope','$location', '$window', 'Notifications','LaboralInsertion', 'Login', 'Utils', 'Users', '$wamp'];

function SearchCtrl($rootScope, $scope, $location, $window, Notifications, LaboralInsertion, Login, Utils, Users, $wamp) {

  $scope.model = {
    sents: {},
    inscriptions: [],
    selected: 0,
    users: [],
    data: [],
    currentScreen: '',
    companies: [],
    company: null,
    emailAddToCompany: '',
    emails: [],
    filters: []
  };


  $scope.getCurrentScreen = function() {
    return $scope.model.currentScreen;
  }

  $scope.selectFilters = function() {
    $scope.model.currentScreen = "screenFilters";
  }

  $scope.selectInscriptions = function(filters) {
    $scope.model.currentScreen = "";
    $scope.model.filters = filters;
  }

  $scope.viewSelected = function() {
    if ($scope.model.selected <= 0) {
      return;
    }
    $scope.model.currentScreen = "screenSelected";
  }


  $scope.selectCompany = function() {
    if ($scope.model.selected <= 0) {
      return;
    }
    $scope.model.currentScreen = "screenSelected screenSelectBusiness";
  }

  $scope.confirmMailToCompany = function(c) {
    $scope.model.currentScreen = "screenSelected screenSendBusiness";
    $scope.model.company = c;
  }

  $scope.addEmailToCompany = function() {
    $scope.model.company.emails.push($scope.model.emailAddToCompany);
    $scope.model.emailAddToCompany = '';
  }

  $scope.removeEmailFromCompany = function(email) {
    for (i = 0; i < $scope.model.company.emails.length; i++) {
      if ($scope.model.company.emails[i] == email) {
        $scope.model.company.emails.splice(i,1);
      }
    }
  }

  $scope.sendMailToCompany = function() {

    if ($scope.model.company.emails.length <= 0) {
      console.log('company.emails = 0');
      return;
    }

    var selectedInscriptions = [];
    for (i = 0; i < $scope.model.inscriptions.length; i++) {
      if ($scope.model.inscriptions[i].selected) {
        selectedInscriptions.push($scope.model.inscriptions[i]);
      }
    }

    if (selectedInscriptions.length <= 0) {
      console.log('selectedInscriptions == 0');
      return;
    }

    $scope.model.currentScreen = "screenSelected screenSending";
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
    $scope.model.currentScreen = "screenSelected screenSent";
    $scope.model.emails = emails;
    console.log('mail enviado ok');
  }

  /*
    Calcula la cantidad de seleccionados
  */
  $scope.getSelectedNumber = function() {
    return $scope.model.selected;
  }

  /*
    Selecciona todas las inscripciones que se puedan seleccionar de la lista de inscripciones
  */
  $scope.selectAllInscriptions = function() {
    for (var i = 0; i < $scope.model.inscriptions.length; i++) {
      $scope.selectInscription($scope.model.inscriptions[i]);
    }
  }

  /*
    Selecciono una inscripcion para ser enviado por correo a una empresa
  */
  $scope.selectInscription = function(i) {

    // chequeo que tenga email
    if ($scope.getMail(i.user_id) == 'No Definido') {
      console.log('No tiene email');
      return;
    }

    i.selected = !i.selected;
    if (i.selected) {
      $scope.model.selected = $scope.model.selected + 1;
    } else {
      $scope.model.selected = $scope.model.selected - 1;
    }
  }

  /*
    Chequea si una inscripcion esta seleccionado para ser enviado a una empresa.
  */
  $scope.isSelected = function(i) {
    if(i) return i.selected;
  }

  /*
    funciones para obtener datos de la persona identificada por el id.
  */
  $scope.getName = function(id) {
    if ($scope.model.users[id] == undefined) {
      return "No Definido";
    }
    return $scope.model.users[id].lastname + " " + $scope.model.users[id].name;
  }

  $scope.getResidence = function(id) {
    if ($scope.model.users[id] == undefined) {
      return "No Definido";
    }
    return $scope.model.users[id].residence_city;
  }

  $scope.getCity = function(id) {
    if ($scope.model.users[id] == undefined) {
      return "No Definido";
    }
    return $scope.model.users[id].city;
  }

  $scope.getDni = function(id) {
    if ($scope.model.users[id] == undefined) {
      return "No Definido";
    }
    return $scope.model.users[id].dni;
  }

  $scope.getGenre = function(id) {
    if ($scope.model.users[id] == undefined) {
      return "No Definido";
    }
    return $scope.model.users[id].genre;
  }

  $scope.getTravel = function(i) {
    if (i.travel) {
      return "Sí";
    } else {
      return "No";
    }
  }

  $scope.getMail = function(id) {
    if ($scope.model.data[id].email != null) {
      return $scope.model.data[id].email.email;
    } else {
      return "No Definido";
    }
  }

  $scope.getEnglish = function(id) {
    if ($scope.model.data[id].languages.length > 0) {
      for (a = 0; a < $scope.model.data[id].languages.length; a++) {
        if ($scope.model.data[id].languages[a].name == 'Inglés') {
          return $scope.model.data[id].languages[a].level;
        }
      }
      return "No";
    } else {
      return "No";
    }
  }

  $scope.getLanguagesOther = function(id) {
    if ($scope.model.data[id].languages.length > 0) {
      for (a = 0; a < $scope.model.data[id].languages.length; a++) {
        if ($scope.model.data[id].languages[a].name != 'Inglés') {
          return "Sí";
        }
      }
      return "No";
    } else {
      return "No";
    }
  }

  // calcula la edad a partir de la fecha de nac.
  // referencias http://stackoverflow.com/questions/4060004/calculate-age-in-javascript
  $scope._calculateAge = function(birthday) { // birthday is a date
      var ageDifMs = Date.now() - birthday.getTime();
      var ageDate = new Date(ageDifMs); // miliseconds from epoch
      return Math.abs(ageDate.getUTCFullYear() - 1970);
  }

  $scope.getAge = function(id) {
    if ($scope.model.users[id] == undefined) {
      return "No Definido";
    }
    date = new Date($scope.model.users[id].birthdate);
    if (date != null) {
      return $scope._calculateAge(date);
    } else {
      return 'nc';
    }
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
    Retorna la cantida de veces que esta registrado en los sents el id de la inscripcion
    (calculado cuando se obtienen todas las inscripciones)
  */
  $scope.getSents = function(id) {
    return $scope.model.sents[id]
  }

  /*
    Obtiene la info de los usuarios
  */
  $scope.getUsers = function(ins) {
    for (i = 0; i < ins.length; i++) {
      //console.log('Buscando usuario ' + ins[i].user_id);
      Users.findById(ins[i].user_id).then(function(user) {
        $scope.model.users[user['id']] = user;
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
        $scope.model.data[data['id']] = data;
      }, function(err) {
        console.log(err);
      });
    }
  }

  /*
    Obtiene toda la info de las companias
  */
  $scope.getCompaniesData = function() {
    LaboralInsertion.findAllCompanies().then(function(companies) {
      $scope.model.companies = companies;
      console.log(companies);
    }, function(err) {
      console.log(err);
    });
  }

  $scope.initialize = function() {
    // TODO: hay que sacar el return, lo puse para que no cargue nada
    return;
    // me registro al evento de envío de mails a las empresas.
    $wamp.subscribe('system.laboralInsertion.COMPANYSENDED', $scope.mailToCompanySent);

    LaboralInsertion.findAllInscriptions().then(function(ins) {
      $scope.model.inscriptions = ins;

      // obtegno el numero de veces que esta el id de la inscripcion en los sents
      for (var i = 0; i < ins.length; i++) {
        ins.selected = false;
        LaboralInsertion.findSentByInscriptionId(ins[i]['id']).then(function(r) {
          // registro el numero de veces que esta esa inscripcion en los sents
          console.log(r);
          $scope.model.sents[r['id']] = r['sents'].length
        }, function(err) {
          console.log(err);
        });
      }

      $scope.getUsers(ins);
      $scope.getUserData(ins);
      $scope.getCompaniesData();
      //console.log($scope.model.inscriptions);
    }, function(err) {
      console.log(err);
    });
  }

  $scope.search = function() {
    console.log($scope.model.filters);
  }

  $rootScope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

}
