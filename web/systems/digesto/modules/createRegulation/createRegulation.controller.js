angular
    .module('mainApp')
    .controller('CreateRegulationCtrl',CreateRegulationCtrl);

CreateRegulationCtrl.$inject = ['$rootScope', '$scope', '$location', '$window', '$timeout','WebSocket', 'Session', 'Cache', 'Notifications', 'Digesto'];

function CreateRegulationCtrl($rootScope, $scope, $location, $window, $timeout, WebSocket, Session, Cache, Notifications, Digesto) {

    $scope.model = {
      issuersRegulation: [],
      issuersOrdinance: [],
      issuersResolution: [],
      issuers: [],
      normative: {},
      visibilities: [],
      status:[]
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
      if ($scope.model.normative.visibility.value == 'GROUPPRIVATE') {
        $scope.selectRegulation(7);
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
    // -------------------------------------------------------------
    // ----------------- CARGA DE DATOS INICIALES ------------------
    // -------------------------------------------------------------
    function initialize() {
      $scope.model.visibilities = [{value:'PUBLIC',name:'Pública'},{value:'PRIVATE',name:'Privada'},{value:'GROUPPRIVATE',name:'Privada de Grupos'}];
      $scope.model.status = [{value:'APPROVED',name:'Aprobado'},{value:'PENDING',name:'Pendiente'}]
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
        if ($scope.model.visibilities[i].value == v) {
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
      $scope.model.normative.type = type;
      $scope.model.normative.file_number = null;
      $scope.model.normative.normative_number = null;
      $scope.model.normative.year = null;
      $scope.model.normative.created = new Date();
      $scope.model.normative.extract = '';
      $scope.model.normative.status = status;
      $scope.model.normative.visibility = visibility;
      $scope.model.normative.relateds = [];
    }



    $scope.save = function() {
      $scope.view.regulationIndex = $scope.view.regulationIndex + 3;
      console.log($scope.model.regulationIndex);
    }




    // $scope.save = function() {
    //   normative = {};
    //   status = "";
    //   visibility = {};
    //   relateds = [];
    //   file = {};
    //   Digesto.createNormative(normative,status,visibility,relateds,file,
    //     function(response) {
    //       Notifications.message(response);
    //     },
    //     function(error) {
    //         Notifications.message(error);
    //     }
    //   );
    // }



};
