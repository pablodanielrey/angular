angular
    .module('mainApp')
    .controller('CreateRegulationCtrl',CreateRegulationCtrl);

CreateRegulationCtrl.$inject = ['$rootScope', '$scope', 'Notifications', 'Digesto', 'Office'];

function CreateRegulationCtrl($rootScope, $scope, Notifications, Digesto, Office) {

    $scope.model = {
      offices: [],
      issuersRegulation: [],
      issuersOrdinance: [],
      issuersResolution: [],
      issuers: [],
      normative: {},
      visibilities: [],
      status:[],
      search:{
        searchAllOffice:''
      }
    }

    $scope.view = {
      regulationIndex: 0,
      regulationName: ['','ORDENANZA','RESOLUCIÓN','DISPOSICIÓN','ORDENANZA','RESOLUCIÓN','DISPOSICIÓN',''],
      styleNames: ['menu','screenOrdenanza','screenResolucion','screenDisposicion','screenOrdenanzaFinal','screenResolucionFinal','screenDisposicionFinal','screenPrivadaDeGrupos','screenRelacionDeNorma','screenRelacionDeNormaFinal']
    };

    /*ordenanza => ordinance
    resolución => resolution
    disposicion => regulation*/
    // ----------------------------------------------------------
    // -------------- DEFINICION DE METODOS ---------------------
    // ----------------------------------------------------------

    $scope.selectRegulation = selectRegulation;
    $scope.getRegulationName = getRegulationName;
    $scope.getStyleName = getStyleName;
    $scope.changeVisibility = changeVisibility;
    $scope.viewDateStatus = viewDateStatus;
    $scope.back = back;

    $scope.initialize = initialize;
    $scope.initializeOrdinance = initializeOrdinance;
    $scope.initializeResolution = initializeResolution;
    $scope.initializeRegulation = initializeRegulation;
    $scope.initializeOffices = initializeOffices;

    $scope.createOrdinance = createOrdinance;
    $scope.createResolution = createResolution;
    $scope.createRegulation = createRegulation;

    // ----------------------------------------------------------
    // ---------------- PARTE VISUAL ----------------------------
    // ----------------------------------------------------------

    function selectRegulation(i) {
        $scope.view.regulationIndex = i;
    }

    function getRegulationName() {
      var t = $scope.view.regulationName[$scope.view.regulationIndex];
      return t;
    }

    function getStyleName() {
      var t = $scope.view.styleNames[$scope.view.regulationIndex];
      return t;
    }

    function changeVisibility() {
      if ($scope.model.normative.visibility.type == 'GROUPPRIVATE') {
        $scope.$broadcast('openPrivateGroupEvent');
      }
    }

    function viewDateStatus() {
      if (($scope.model.normative == null) || !($scope.model.normative.status)) {
        return false;
      }
      return $scope.model.normative.status.value == 'APPROVED';
    }

    function back() {
      if ($scope.model.normative == null || !$scope.model.normative.type) {
        return;
      }
      switch ($scope.model.normative.type) {
        case 'ORDINANCE':$scope.selectRegulation(1);break;
        case 'RESOLUTION':$scope.selectRegulation(2);break;
        case 'REGULATION':$scope.selectRegulation(3);break;
        default:$scope.selectRegulation(0);break;
      }
    }

    // -------------------------------------------------------------
    // ------------------------- EVENTOS ---------------------------
    // -------------------------------------------------------------
    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });

    $scope.$on('viewPrivateGroupLoad',function(event) {
      $scope.selectRegulation(7);
    });
    // -------------------------------------------------------------
    // ----------------- CARGA DE DATOS INICIALES ------------------
    // -------------------------------------------------------------
    function initialize() {
      $scope.model.visibilities = [{type:'PUBLIC',name:'Pública'},{type:'PRIVATE',name:'Privada'},{type:'GROUPPRIVATE',name:'Privada de Grupos'}];
      $scope.model.status = [{value:'APPROVED',name:'Aprobado'},{value:'PENDING',name:'Pendiente'}]
      initializeOrdinance();
      initializeResolution();
      initializeRegulation();
      initializeOffices();
    }

    function initializeOffices() {
      Office.getOffices(
          function(offices) {
            $scope.model.offices = offices;
          },
          function(error) {
            Notifications.message(error);
          }
      );
    }

    function initializeOrdinance() {
      Digesto.loadIssuers('ORDINANCE',
          function(issuers) {
            $scope.model.issuersOrdinance = issuers;
          },
          function(error) {
            $scope.model.issuersOrdinance = [];
          }
      );
    }

    function initializeResolution() {
      Digesto.loadIssuers('RESOLUTION',
          function(issuers) {
            $scope.model.issuersResolution = issuers;
          },
          function(error) {
            $scope.model.issuersResolution = [];
          }
      );
    }

    function initializeRegulation() {
      Digesto.loadIssuers('REGULATION',
          function(issuers) {
            $scope.model.issuersRegulation = issuers;
          },
          function(error) {
            $scope.model.issuersRegulation = [];
          }
      );
    }
    // -------------------------------------------------------------
    // ----------------- CREACION DE NORMATIVAS --------------------
    // -------------------------------------------------------------

    function findVisibility(v) {
      for (var i = 0; i < $scope.model.visibilities.length; i++) {
        if ($scope.model.visibilities[i].type == v) {
          return $scope.model.visibilities[i];
        }
      }
      return null;
    }

    function findStatus(s) {
      for (var i = 0; i < $scope.model.status.length; i++) {
        if ($scope.model.status[i].value == s) {
          return $scope.model.status[i];
        }
      }
      return null;
    }

    function createOrdinance() {
      var status = findStatus('APPROVED');
      var visibility = findVisibility('PUBLIC');
      loadDataNormative($scope.model.issuersOrdinance,'ORDINANCE',status,visibility);
      $scope.selectRegulation(1);
    }

    function createResolution() {
      var status = findStatus('PENDING');
      var visibility = findVisibility('PRIVATE');
      loadDataNormative($scope.model.issuersResolution,'RESOLUTION',status,visibility);
      $scope.selectRegulation(2);
    }

    function createRegulation() {
      var status = findStatus('APPROVED');
      var visibility = findVisibility('PUBLIC');
      loadDataNormative($scope.model.issuersRegulation,'REGULATION',status,visibility);
      $scope.selectRegulation(3);
    }

    function loadDataNormative(issuers,type,status,visibility) {
      $scope.model.issuers = issuers;
      $scope.model.normative = {};
      $scope.model.normative.issuer = (issuers.length > 0)?issuers[0]:null;
      $scope.model.normative.issuer_id = (issuers.length > 0)?issuers[0].id:null;
      $scope.model.normative.type = type;
      $scope.model.normative.file_number = null;
      $scope.model.normative.normative_number_full = null;
      $scope.model.normative.created = new Date();
      $scope.model.normative.extract = '';
      $scope.model.normative.status = status;
      $scope.model.normative.visibility = visibility;
      $scope.model.normative.offices = [];
      $scope.model.normative.relateds = [];
      $scope.model.normative.file = null;
    }



    $scope.save = function() {
      // falta verificar que este bien formateado el expediente
      console.log($scope.model.normative);

      Digesto.createNormative($scope.model.normative,
        function(response) {
          $scope.view.regulationIndex = $scope.view.regulationIndex + 3;
        },
        function(error) {
            Notifications.message(error);
        }
      );

    }



};
