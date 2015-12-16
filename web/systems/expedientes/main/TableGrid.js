
/**
 * Servicio de controlador de grilla con busqueda simple, avanzada, indice y paginacion
 */
app.service('TableGrid', ["$location", "$rootScope", "$http", "ServerAccess", function($location, $rootScope, $http, ServerAccess){
	
	
	this.initialize = function($scope, label){
	  
    /***** datos de la grilla *****/
    $scope.grid = {numRows: 0, data: 0};
    
    /***** datos de busqueda *****/
    $scope.search = {simple: null, advanced: [], index: []};

    /***** datos de paginacion *****/
    $scope.pagination = {pageSize: 40, page: 0, pages: 0, disabled: true};
    
    /***** datos de ordenamiento *****/
    $scope.orderBy = {field: null, type: null};
    
    /***** seleccionados *****/
    $scope.selection = [];

    this.initializeSearch($scope.search);
    this.getGridNumRows($scope, label);
	}
  
  /***** METODOS ASOCIADOS AL FORMULARIO DE BUSQUEDA ******
  /**
   * Limpiar variables de busqueda, la busqueda se inicializa en funcion de los parametros de la url
   */
  this.initializeSearch = function(search){
    var urlParams = $location.search(); //inicializar parametros de busqueda especificados en la url
    
    //***** inicializar busqueda simple *****
    if(urlParams.s) search.simple = urlParams.s;
    
    //***** inicializar busqueda indice *****
    if(urlParams.ic){
      var searchIndexCountAux = parseInt(urlParams.ic);
      var searchIndexCount = (!isNaN(searchIndexCountAux)) ? searchIndexCountAux : 0;
        
      for (var i = 0; i < searchIndexCount; i++){
        var searchIndexElement = {
          field: null, //field a buscar
          value: null, //valor de la opcion a buscar
          fieldLabel:null,  //etiqueta del field
          valueLabel:null, //etiqueta del label
          table: null //tabla asociada a la busqueda indice
        };
      
        if(urlParams[i + "if"]) searchIndexElement.field = urlParams[i + "if"];
        if(urlParams[i + "if"]) searchIndexElement.fieldLabel = urlParams[i + "if"];
        if(urlParams[i + "iv"]) searchIndexElement.value = urlParams[i + "iv"];
        if(urlParams[i + "iv"]) searchIndexElement.valueLabel = urlParams[i + "iv"];
        if(urlParams[i + "it"]) searchIndexElement.table = urlParams[i + "it"];
        if(urlParams[i + "in"]) searchIndexElement.fieldLabel = urlParams[i + "in"];
    
        search.index[i] = searchIndexElement;
        this.initializeSearchIndexValueLabel(search.index[i]);
      }
    }
    
    return search;
  };
  
  
  /**
   * Inicializar busqueda indice
   * @param {Array} urlParams Parametros de la url
   * @returns {Array} busqueda indice
   */
  this.initializeSearchIndexValueLabel = function(searchIndex){
    ServerAccess.findById(searchIndex.value, searchIndex.table)
      .then(
        function(response){ searchIndex.valueLabel = response.data["label"]; },
        function(error){ $rootScope.$broadcast("errorEvent", error); }
      );
  };

  
  /***** METODOS ASOCIADOS A LA PAGINACION *****  
  /**
   * Inicializar paginacion: En funcion de numRows se inicializan los parametros de paginacion
   * @param {type} $scope
   * @returns {undefined}
   */
  this.initializePagination = function($scope){
    var pageSize = parseInt($scope.pagination.pageSize);
    $scope.pagination.pageSize = $scope.pagination.pageSize.toString();
    $scope.pagination.page = 0;
    $scope.pagination.pages = 0;
    $scope.pagination.disabled = true;
    if ($scope.grid.numRows > 0){
      $scope.pagination.page = 1;
      $scope.pagination.pages = ($scope.grid.numRows !== 0) ? Math.ceil($scope.grid.numRows / pageSize) : 0;
    }   
  };
  
  
  /**
   * Definir pagina
   */
  this.setPage = function($scope, page){
    $scope.pagination.disabled = true;
    var p = parseInt(page);    
    $scope.pagination.page = (isNaN(p)) ? 1 :
      (p < 1) ? 1 :
        (p > $scope.pagination.pages) ? $scope.pagination.pages : p;
  };
   
   
  /**
   * Modificar tamanio de pagina
   * @param {$scope} $scope
   * @param {string} label Etiqueta de acceso
   */   
  this.changePagination = function($scope, label){
    this.initializePagination($scope);
    this.getGridData($scope, label);
  };
  
  /**
   * Consultar datos de una pagina
   * @param {type} $scope
   * @param {type} page
   * @returns {undefined}
   */  
  this.goPage = function($scope, page, label){
    this.setPage($scope, page);    
    this.getGridData($scope, label);
  };
  
  
  /***** METODOS DE FORMATO DE VARIABLES PARA ENVIAR AL SERVIDOR *****/
  /**
   * Definir parametros de busqueda para enviar al servidor
get
   * @returns {undefined}
   */
  this.defineSearchParams = function(search){  
    var searchParams = {};
  
    /***** definir busqueda simple *****/
    if (search.simple) searchParams["s"] = search.simple;
    
    /***** definir busqueda indice *****/
    if (search.index.length){
      
      searchParams["ic"] = search.index.length;
      for(var i = 0; i < search.index.length; i++){
        searchParams[i + "if"] = search.index[i].field;
        searchParams[i + "iv"] = search.index[i].value;
      }
    }
    
    return searchParams;
  };
  
  
  
  
  /**
   * Definir parametros de busqueda para enviar al servidor
   * @param {Object} pagination = Debe estar correctamente definido
   *    {
   *      page: Numero de pagina
   *      pageSize: Tamanio de pagina
   *    
   *    }
   * 
   * @returns {undefined}
   */
  this.definePaginationParams = function(pagination){    
    var paginationParams = {};
    paginationParams["p"] = parseInt(pagination.page);
    paginationParams["q"] = parseInt(pagination.pageSize);
    return paginationParams;
  };
  
  /**
   * Definir parametrod de ordenamiento
   * @param {type} orderBy
   * @returns {TableGrid_L5.defineOrderByParams.orderByParams}
   */
  this.defineOrderByParams = function(orderBy){
    var orderByParams = {};
    if(orderBy.field){ orderByParams["of"] = orderBy.field;
      orderByParams["ot"] = orderBy.type;
    }
    return orderByParams;
  };


  /**
   * Definir parametros para obtener los datos de la grilla
   * @param {type} scope
   * @param {type} access
   * @returns {undefined}
   */
  this.defineParams = function($scope){
    var params = this.defineSearchParams($scope.search);
    var paginationParams = this.definePaginationParams($scope.pagination);
    var orderByParams = this.defineOrderByParams($scope.orderBy);
    for (var param in paginationParams) { params[param] = paginationParams[param]; }
    for (var param in orderByParams) {  params[param] = orderByParams[param]; }
    return params;
  };

  
  
  /***** CONSULTA DE NUM ROWS *****/
  /**
   * get num rows
   * @param {type} scope
   * @param {type} access
   * @returns {undefined}
   */
  this.getGridNumRows = function(scope, label){    
    var searchParams = this.defineSearchParams(scope.search);    
    console.log(searchParams);
    return ServerAccess.numRows(searchParams, label)
        .then(
          function(response){
            scope.grid.numRows = parseInt(response.data);
            $rootScope.$broadcast("gridNumRowsInitialized");
          },
          function(error){
            var alert = {title:"Error", message:error.data};
            scope.addAlert(alert);
          }
        );
  };
  
  
  /**
   * Buscar datos
   */
  this.searchData = function($scope, label){
    $scope.pagination.disabled = true;
    this.getGridNumRows($scope, label);
  }


  /**
   * Consultar datos de la grilla.
   * La consulta a los datos de la grilla se realiza luego de haber consultado la cantidad de elementos
   * @param {fieldset} fieldsetId
   * @param {$scope} $scope
   * @param {String} access Identificacion de acceso
   */
  this.getGridData = function($scope, label){
    
    $scope.grid.data = []; 
    if($scope.grid.numRows < 1) return;

    var params = this.defineParams($scope);

    ServerAccess.gridData(params, label)
      .then(
        function(response){
          $scope.grid.data = response.data;   //cargar datos de la grilla
          $scope.pagination.disabled = false; //habilitar paginacion
        },
        function(error){
          var alert = {title:"Error", message:"Error al consultar datos de la grilla"};
          $scope.addAlert(alert);
        }
      );
  };
  
  /**
   * Seleccion de filas de la grilla
   * @param {type} $scope
   * @param {type} id
   */
  this.toggleSelection = function($scope, id){
    var index = $scope.selection.indexOf(id);
    if (index > -1) $scope.selection.splice(index, 1); // is currently selected
    else $scope.selection.push(id); // is newly selected
  };
  
  
  this.toggleOrderBy = function($scope, field){
    if($scope.orderBy.field == field){
      if($scope.orderBy.type == "asc") $scope.orderBy.type = "desc";
      else $scope.orderBy.type = "asc";
    } else {
      $scope.orderBy.field = field;
      $scope.orderBy.type = "asc";
    }
    this.getGridData($scope);
  };
  

}]);
