var app = angular.module('mainApp');

app.service('Utils', function() {

  this.getId = function() {
    var id =  (Math.floor((Math.random() * 1000000000) + 1)).toString();
    return id;
  };


  this.filter = function(f,a) {
    var r = [];
    for (var i = 0; i < a.length; i++) {
      if (f(a[i]) == true) {
        r.push(a[i])
      }
    }
    return r;
  }

});
