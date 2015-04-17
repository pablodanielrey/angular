var app = angular.module('mainApp');

app.service('Utils', function() {

  this.base64ToBlob = function(data) {
    var binary = atob(data);
    var array = new Uint8Array(binary.length);
    for( var i = 0; i < binary.length; i++ ) { array[i] = binary.charCodeAt(i); };
    return new Blob([array],{type: "application/octet-stream;base64"});
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
  };
  
  
   /**
   * Dar formato date de la forma DD/MM/YYYY, completa con ceros!!!
   * @param {type} date
   * @returns {string} formato de datos
   */
	this.formatDate = function(date) {
    var dateArray = date.toLocaleDateString().split("/");

    if(parseInt(dateArray[0]) < 10 ){
      dateArray[0] = "0" + dateArray[0]; 
    } 
    
    if(parseInt(dateArray[1]) < 10 ){
      dateArray[1] = "0" + dateArray[1]; 
    } 

    return dateArray[0] + "/" + dateArray[1] + "/" + dateArray[2];
  };
  
  /**
   * Dar formato date de la forma YYYY-MM-DD, completa con ceros!!!
   * @returns {undefined}
   */
  this.formatDateExtend = function(date){
    return date.toJSON().substring(0,10);
  };
  
  this.formatTime = function(date){
    return date.toTimeString().substring(0, 5);
  };
  
  

});
