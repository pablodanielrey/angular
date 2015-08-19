angular
    .module('mainApp')
    .controller('CreateRegulationCtrl',CreateRegulationCtrl);

CreateRegulationCtrl.$inject = ['$rootScope', '$scope', 'Notifications', 'Digesto', 'Office','$routeParams','$location'];

function CreateRegulationCtrl($rootScope, $scope, Notifications, Digesto, Office,$routeParams,$location) {

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
      },
      typeRelateds:['Deja sin efecto','Complementa']
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
    $scope.loadFindRelatedView = loadFindRelatedView;
    $scope.back = back;

    $scope.initialize = initialize;
    $scope.initializeOrdinance = initializeOrdinance;
    $scope.initializeResolution = initializeResolution;
    $scope.initializeRegulation = initializeRegulation;
    $scope.initializeOffices = initializeOffices;

    $scope.createOrdinance = createOrdinance;
    $scope.createResolution = createResolution;
    $scope.createRegulation = createRegulation;
    $scope.loadDataOrdinance = loadDataOrdinance;
    $scope.loadDataResolution = loadDataResolution;
    $scope.loadDataRegulation = loadDataRegulation;

    $scope.removeRelated = removeRelated;
    $scope.loadRelateds = loadRelateds;
    $scope.addFile = addFile;
    $scope.removeFile = removeFile;
    $scope.cancel = cancel;
    $scope.finish = finish;

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

    function loadFindRelatedView() {
      $scope.selectRegulation(8);
      $scope.$broadcast('openRelatedsViewEvent');
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

    $scope.$on('viewSearchResultRelatedsLoad',function(event,normatives) {
      $scope.loadRelateds(normatives);
      $scope.selectRegulation(9);
    })

    $scope.$on('selectRelated',function(event,normative) {
      var r = {'related_id':normative.id,'type':$scope.model.typeRelateds[0],'normative_number_full':normative['normative_number_full']};
      $scope.model.normative.relateds.push(r);
      $scope.back();
    })
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

      $scope.model.operation = 'create';
      if ($routeParams['id']) {
        hashId = $routeParams['id'];
        id = window.atob(hashId);
        findNormativeById(id);

        if ($routeParams['operation']) {
          hashOperation = $routeParams['operation'];
          operation = window.atob(hashOperation);
          $scope.model.operation = operation;
        }
      }
    }

    function findNormativeById(id) {
      Digesto.findNormativeById(id,
          function(normative) {
            $scope.model.normative = normative;
            switch ($scope.model.normative.type) {
              case 'ORDINANCE':$scope.loadDataOrdinance(normative,normative.status.status,normative.visibility.type);break;
              case 'RESOLUTION':$scope.loadDataResolution(normative,normative.status.status,normative.visibility.type);break;
              case 'REGULATION':$scope.loadDataRegulation(normative,normative.status.status,normative.visibility.type);break;
              default:$scope.selectRegulation(0);break;
            }
          },
          function(error) {
            Notifications.message(error);
          }
      );
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

    function loadOfficesNormative(visibility) {
      if (visibility.additional_data && visibility.additional_data.length > 0) {
        Office.findOffices(visibility.additional_data,
          function(offices) {
            $scope.model.normative.offices = (offices == null)?[]:offices;
          },
          function(error) {
            Notifications.message(error);
          }
        );
      }
    }

    function createOrdinance() {
      $scope.model.normative = {};
      $scope.loadDataOrdinance(null,'APPROVED','PUBLIC');
    }

    function loadDataOrdinance(normative,status,visibility) {
      var status = findStatus(status);
      var visibility = findVisibility(visibility);
      loadOfficesNormative(normative['visibility']);
      loadDataNormative($scope.model.issuersOrdinance,'ORDINANCE',status,visibility);
      $scope.selectRegulation(1);
    }

    function createResolution() {
      $scope.model.normative = {};
      $scope.loadDataResolution(null,'PENDING','PRIVATE');
    }

    function loadDataResolution(normative,status,visibility) {
      var status = findStatus(status);
      var visibility = findVisibility(visibility);
      loadOfficesNormative(normative['visibility']);
      loadDataNormative($scope.model.issuersResolution,'RESOLUTION',status,visibility);
      $scope.selectRegulation(2);
    }

    function createRegulation() {
      $scope.model.normative = {};
      $scope.loadDataRegulation(null,'APPROVED','PUBLIC');
    }

    function loadDataRegulation(normative,status,visibility) {
      var status = findStatus(status);
      var visibility = findVisibility(visibility);
      loadOfficesNormative(normative['visibility']);
      loadDataNormative($scope.model.issuersRegulation,'REGULATION',status,visibility);
      $scope.selectRegulation(3);
    }

    function loadIssuer(issuer_id,issuers) {
        if (issuer_id != null) {
          for (var i = 0; i < issuers.length; i++) {
            if (issuer_id == issuers[i].id) {
              $scope.model.normative.issuer = issuers[i];
              $scope.model.normative.issuer_id = issuers[i].id;
              return;
            }
          }
        }

        $scope.model.normative.issuer = (issuers.length > 0)?issuers[0]:null;
        $scope.model.normative.issuer_id = (issuers.length > 0)?issuers[0].id:null;

    }

    function loadDataNormative(issuers,type,status,visibility) {
      $scope.model.issuers = issuers;

      loadIssuer($scope.model.normative.issuer_id,issuers);

      $scope.model.normative.type = type;

      if (!$scope.model.normative.file_number) {
        $scope.model.normative.file_number = null;
      } else {
        $scope.model.normative.file_number = parseInt($scope.model.normative.file_number);
      }

      if (!$scope.model.normative.normative_number_full) {
        $scope.model.normative.normative_number_full = null;
      }

      if ($scope.model.normative.created) {
        $scope.model.normative.created = new Date($scope.model.normative.created);
      } else {
        $scope.model.normative.created = new Date();
      }

      if (!$scope.model.normative.extract) {
        $scope.model.normative.extract = '';
      }

      $scope.model.normative.status = status;
      $scope.model.normative.visibility = visibility;

      if (!$scope.model.normative.offices) {
        $scope.model.normative.offices = [];
      }

      if (!$scope.model.normative.relateds) {
        $scope.model.normative.relateds = [];
      }

      $scope.model.normative.file = null;
    }



    $scope.save = function() {
      console.log($scope.model.operation);
      if ($scope.model.operation != 'create') {

        $scope.view.regulationIndex = $scope.view.regulationIndex + 3;
        return;
      }

      var normative = $scope.model.normative;
      if (normative.visibility.type == 'GROUPPRIVATE') {
        ids = []
        for (var i = 0; i < $scope.model.normative.offices.length; i++) {
          ids.push($scope.model.normative.offices[i].id);
        }
        normative.visibility.additional_data = ids;
      }

      Digesto.createNormative($scope.model.normative,
        function(response) {
          $scope.view.regulationIndex = $scope.view.regulationIndex + 3;
        },
        function(error) {
            Notifications.message(error);
        }
      );

    }


    // ----------------------------------------------------------
    // -------------------- ACCIONES ----------------------------
    // ----------------------------------------------------------

    function removeRelated(r) {
      var index = $scope.model.normative.relateds.indexOf(r);
      $scope.model.normative.relateds.splice(index,1);
    }

    function loadRelateds(normatives) {
      for (var i = 0; i < normatives.length; i++) {
        var include = false;
        for (var j = 0; j < $scope.model.normative.relateds.length; j++) {
          if (normatives[i].id == $scope.model.normative.relateds[j].related_id) {
            include = true;
          }
        }
        if (!include) {
          $scope.model.normatives.push(normatives[i]);
        }
      }
    }

    function addFile(fileName,fileContent) {
      $scope.model.normative.file = {};
      $scope.model.normative.file.name = fileName;
      $scope.model.normative.file.binary = window.btoa(fileContent);
    }

    function removeFile() {
      $scope.model.normative.file = null;
    }

    function cancel() {
      if ($scope.model.operation == 'create') {
        $location.path('/load');
      } else {
        $location.path('/search');
      }
    }

    function finish() {
      if ($scope.model.operation == 'create') {
        $location.path('/load');
      } else {
        $location.path('/search');
      }
    }
};
