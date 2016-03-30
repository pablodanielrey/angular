angular
  .module('mainApp')
  .controller('CompanyCtrl', CompanyCtrl);

CompanyCtrl.$inject = ['$rootScope','$scope', 'LaboralInsertion'];

function CompanyCtrl($rootScope, $scope, LaboralInsertion) {

  $scope.model = {
    companies: [],
    companySelected:null,
    bkpCompanySelected:null
  }

  $scope.view = {
    search:'',
    style:''
  }

  $scope.initialize = initialize;
  $scope.loadCompanies = loadCompanies;
  $scope.selectCompany = selectCompany;
  $scope.save = save;
  $scope.cancel = cancel;
  $scope.addContact = addContact;
  $scope.removeContact = removeContact;


  // --------------------------------------------
  // ------------- INICIALIZACION ---------------
  // --------------------------------------------

  function initialize() {
    $scope.loadCompanies();
  }

  function loadCompanies() {
    LaboralInsertion.findAllCompanies().then(function(companies) {
      $scope.model.companies = companies;
      for (var i = 0; i < companies.length; i++) {
        c = $scope.model.companies[i];
        c['beginCM'] = new Date(c['beginCM']);
        c['endCM'] = new Date(c['endCM']);
        c['img'] = '/systems/laboralInsertion/img/empresa.jpg';
      }
    }, function(err) {
      console.log(err);
    });
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
    $scope.model.bkpCompanySelected = angular.copy($scope.model.companySelected);
    if (!c.contacts) {
      c.contacts = [];
      $scope.addContact();
    }
    $scope.view.style = 'displayForm';
  }

  function cancel() {
    angular.copy($scope.model.bkpCompanySelected, $scope.model.companySelected);
    $scope.model.companySelected = null;
    $scope.view.style = "";
  }

  function save() {
    var i = $scope.model.companySelected.contacts.length;
    while (i > 0) {
      var c = $scope.model.companySelected.contacts[i-1];
      if (c.name.trim() == '' && c.telephone.trim() == '' && c.email.trim() == '') {
        $scope.removeContact(c);
      }
      i = i - 1;
    }
    LaboralInsertion.persistCompany($scope.model.companySelected).then(function(id) {
      loadCompanies();
      $scope.model.companySelected = null;
      $scope.view.style = "";
    }, function(err) {
        console.log(err);
    });
  }

  function addContact() {
    $scope.model.companySelected.contacts.push({'name':'','email':'','telephone':''});
  }

  function removeContact(c) {
    var index = $scope.model.companySelected.contacts.indexOf(c);
    if (index > -1) {
        $scope.model.companySelected.contacts.splice(index, 1);
    }
    if ($scope.model.companySelected.contacts.length <= 0) {
      addContact();
    }
  }

}
