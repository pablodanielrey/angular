var app = angular.module('mainApp');

app.factory('Utils', function() {

  var factory = {};

  factory.getId = function() {
    var id =  (Math.floor((Math.random() * 1000000000) + 1)).toString();
    return id;
  };

  return factory;

});
