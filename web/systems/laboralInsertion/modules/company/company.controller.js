angular
  .module('mainApp')
  .controller('CompanyCtrl', CompanyCtrl);

CompanyCtrl.$inject = ['$rootScope','$scope'];

function CompanyCtrl($rootScope, $scope) {

  $scope.model = {
    companies: [],
    companySelected:null
  }

  $scope.view = {
    search:'',
    style:''
  }

  $scope.initialize = initialize;
  $scope.selectCompany = selectCompany;
  $scope.save = save;
  $scope.cancel = cancel;
  $scope.addTelephone = addTelephone;
  $scope.removeTelephone = removeTelephone;
  $scope.addEmail = addEmail;
  $scope.removeEmail = removeEmail;

  // --------------------------------------------
  // ------------- INICIALIZACION ---------------
  // --------------------------------------------

  function initialize() {
    $scope.model.companies = [{'name':'AFIP','city':'La Plata','img':'/systems/laboralInsertion/img/empresa.jpg'},
                              {'name':'Cerveceria Quilmes','city':'La Plata','img':'/systems/laboralInsertion/img/empresa.jpg'},
                              {'name':'OSDE','city':'La Plata','img':'/systems/laboralInsertion/img/empresa.jpg'},
                              {'name':'Seguros Rivadavia','city':'La Plata','img':'/systems/laboralInsertion/img/empresa.jpg'},
                              {'name':'Techint','city':'Capital Federal','img':'/systems/laboralInsertion/img/empresa.jpg'},
                              {'name':'Coca Cola','city':'La Plata','img':'/systems/laboralInsertion/img/empresa.jpg'},
                              {'name':'Google','city':'Capital Federal','img':'/systems/laboralInsertion/img/empresa.jpg'},
                              {'name':'Arba','city':'La Plata','img':'/systems/laboralInsertion/img/empresa.jpg'}
                             ];
  }

  // --------------------------------------------
  // ---------------- EVENTOS -------------------
  // --------------------------------------------
  $rootScope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });


  // --------------------------------------------
  // ---------------- ACCIONES -------------------
  // --------------------------------------------

  function selectCompany(c) {
    if (c == null) {
      c = {};
    }
    $scope.model.companySelected = c;
    if (c.telephones === undefined || c.telephones.length <= 0) {
      c.telephones = [];
      addTelephone();
    }
    if (c.emails === undefined || c.emails.length <= 0) {
      c.emails = [];
      addEmail();
    }
    $scope.view.style = 'displayForm';
  }

  function cancel() {
    $scope.model.companySelected = null;
    $scope.view.style = "";
  }

  function save() {
    $scope.model.companySelected = null;
    $scope.view.style = "";
  }

  function addTelephone() {
    $scope.model.companySelected.telephones.push({'number':''});
  }

  function removeTelephone(t) {
    var index = $scope.model.companySelected.telephones.indexOf(t);
    if (index > -1) {
        $scope.model.companySelected.telephones.splice(index, 1);
    }
    if ($scope.model.companySelected.telephones.length <= 0) {
      addTelephone();
    }
  }

  function addEmail() {
    $scope.model.companySelected.emails.push({'email':''});
  }

  function removeEmail(m) {
    var index = $scope.model.companySelected.emails.indexOf(m);
    if (index > -1) {
        $scope.model.companySelected.emails.splice(index, 1);
    }
    if ($scope.model.companySelected.emails.length <= 0) {
      addEmail();
    }
  }

}
