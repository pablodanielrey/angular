

var app = angular.module('mainApp');

app.factory('Cache', function($window) {

  var cache = {};

  cache.getStorage = function() {
    return $window['localStorage'];
  }

  cache.getItem = function(key) {
    var s = this.getStorage();
    var jdata = s.getItem(key);
    if (jdata == null) {
      return null;
    }
    var data = JSON.parse(jdata);
    return data;
  };

  cache.removeItem = function(key) {
    var s = this.getStorage();
    s.removeItem(key);
  };

  cache.setItem = function(key,value) {
    var s = this.getStorage();
    s.setItem(key,JSON.stringify(value));
  };


  return cache;

});
