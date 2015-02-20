

var app = angular.module('mainApp');

app.service('Cache', function($window) {

  this.getStorage = function() {
    return $window['localStorage'];
  }

  this.getItem = function(key) {
    var s = this.getStorage();
    var jdata = s.getItem(key);
    if (jdata == null) {
      return null;
    }
    var data = JSON.parse(jdata);
    return data;
  };

  this.removeItem = function(key) {
    var s = this.getStorage();
    s.removeItem(key);
  };

  this.setItem = function(key,value) {
    var s = this.getStorage();
	var j = JSON.stringify(value);
	console.log(j);
    s.setItem(key,j);
  };

});
