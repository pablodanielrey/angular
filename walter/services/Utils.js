var app = angular.module('mainApp');

app.service('Utils', function() {

  this.getId = function() {
    var id =  (Math.floor((Math.random() * 1000000000) + 1)).toString();
    return id;
  };

});
