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

    $scope.visual = {
      regulationIndex: 0,
      regulationName: ['','ORDENANZA','RESOLUCIÓN','DISPOSICIÓN','ORDENANZA','RESOLUCIÓN','DISPOSICIÓN',''],
      styleNames: ['menu','screenOrdenanza','screenResolucion','screenDisposicion','screenOrdenanzaFinal','screenResolucionFinal','screenDisposicionFinal','screenPrivadaDeGrupos','screenRelacionDeNorma']
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
        $scope.visual.regulationIndex = i;
    }

    function getRegulationName() {
      var t = $scope.model.regulationName[$scope.model.regulationIndex];
      return t;
    }

    function getStyleName() {
      var t = $scope.model.styleNames[$scope.model.regulationIndex];
      return t;
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
      $scome.model.status = [{value:'APPROVED',name:'Aprobado'},{value:'PENDING',name:'Pendiente'}]
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

    function createOrdinance() {
      loadDataNormative($scope.model.issuersOrdinance,'ORDINANCE','APPROVED','PUBLIC');
      $scope.selectRegulation(1);
    }

    function createRegulation() {
      loadDataNormative($scope.model.issuersRegulation,'REGULATION','APPROVED','PUBLIC');
      $scope.selectRegulation(2);
    }

    function createResolution() {
      loadDataNormative($scope.model.issuersResolution,'RESOLUTION','PENDING','PRIVATE');
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
      $scope.model.regulationIndex = $scope.model.regulationIndex + 3;
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
