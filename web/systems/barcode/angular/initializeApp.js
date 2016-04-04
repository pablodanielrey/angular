/**
 * Detalle de la configuracion
 * ui.bootstrap: Bootstrap para angular, var app = angular.module("MainApp", [..., 'ui.bootstrap'], ... //adicionalmente se debe incluir la librería html
 *    uibDatepickerConfig: Configuracion por defecto del uibDatepicker de bootstrap
 *    uibDatepickerPopupConfig: Configuracion por defecto del uibDatepicker de bootstrap
 * $locationProvider y $httpProvider: Configuración de la lectura y pasaje de parametros
 * angular-md5: Codificacion md5 (incluir si se necesita login, , var app = angular.module("MainApp", [..., 'angular-md5'], ... //adicionalmente se debe incluir la librería html
 * ngFileUpload: Directiva para subir archivos (incluir si se necesita subir archivos, var app = angular.module("MainApp", [..., 'ngFileUpload'], ... //adicionalmente se debe incluir la librería html
 */

var app = angular.module("MainApp", ['ngAnimate', 'ngRoute', 'ui.bootstrap', 'ngFileUpload'], function($httpProvider) {
 
  // Use x-www-form-urlencoded Content-Type
  $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
 
  /**
   * The workhorse; converts an object to x-www-form-urlencoded serialization.
   * @param {Object} obj
   * @return {String}
   */
  var param = function(obj) {
    var query = '', name, value, fullSubName, subName, subValue, innerObj, i;
      
    for(name in obj) {
      value = obj[name];
        
      if(value instanceof Array) {
        for(i=0; i<value.length; ++i) {
          subValue = value[i];
          fullSubName = name + '[' + i + ']';
          innerObj = {};
          innerObj[fullSubName] = subValue;
          query += param(innerObj) + '&';
        }
      }
      else if(value instanceof Object) {
        for(subName in value) {
          subValue = value[subName];
          fullSubName = name + '[' + subName + ']';
          innerObj = {};
          innerObj[fullSubName] = subValue;
          query += param(innerObj) + '&';
        }
      }
      else if(value !== undefined && value !== null)
        query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
    }
      
    return query.length ? query.substr(0, query.length - 1) : query;
  };
 
  // Override $http service's default transformRequest
  $httpProvider.defaults.transformRequest = [function(data) {
    return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
  }];

})

.config(['uibDatepickerConfig', function(uibDatepickerConfig) {
  uibDatepickerConfig.showWeeks = false;
  uibDatepickerConfig.startingDay = 1;
}])

.config(['uibDatepickerPopupConfig', function(uibDatepickerConfig) {
  uibDatepickerConfig.showButtonBar = false;
}]);
