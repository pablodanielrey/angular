var app = angular.module('mainApp');

app.service('Utils', function() {

  this.base64ToBlob = function(data) {
    var binary = atob(data.cv);
    var array = new Uint8Array(binary.length);
    for( var i = 0; i < binary.length; i++ ) { array[i] = binary.charCodeAt(i); };
    return new Blob([array],{type: "octet/stream;base64"});
  }

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
