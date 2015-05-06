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
    retorna el día de la semana asignado a cierta fecha.
  */
  this.getDayString = function(date) {
    var weekday = new Array(7);
    weekday[0]=  "Domingo";
    weekday[1] = "Lunes";
    weekday[2] = "Martes";
    weekday[3] = "Miércoles";
    weekday[4] = "Jueves";
    weekday[5] = "Viernes";
    weekday[6] = "Sábado";
    return weekday[date.getDay()];
  }


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
  this.formatDateExtend = function(date) {
    var dateArray = date.toLocaleDateString().split("/");

    if(parseInt(dateArray[0]) < 10 ){
      dateArray[0] = "0" + dateArray[0];
    }

    if(parseInt(dateArray[1]) < 10 ){
      dateArray[1] = "0" + dateArray[1];
    }

    var dateStr = dateArray[2] + "-" + dateArray[1] + "-" + dateArray[0];
    return dateStr;
  };

  this.formatTime = function(date){
    return date.toTimeString().substring(0, 5);
  };

  this.getTimeFromMinutes = function(minutes){
    var hours = Math.floor(minutes / 60).toString();
    if(hours.length === 1) hours = "0" + hours;
    var minutes = Math.round((minutes % 60)).toString();
    if(minutes.length === 1) minutes = "0" + minutes;
    return hours + ":" + minutes;
  };

  this.getDates = function(startDate, endDate){
    var s = new Date(startDate);
    var dates = new Array();
    while (s <= endDate) {
        dates.push(new Date(s));
        s.setDate(s.getDate() + 1);
    }
    return dates;
  };

  this.getDifferenceTimeFromDates = function(date1, date2){
    var diffMin = ((Math.abs(date2 - date1) / 1000) / 60); //minutos entre date 1 y date 2
    return this.getTimeFromMinutes(diffMin);
  };

  /**
   * Definir un timestamp extrayendo el date de un parametro y el time de otro
   * @param {Date} date Parametro desde el cual se obtendra el date
   * @param {type} time Parametro desde el cual se obtendra el time
   * @returns {string} timestamp, ejemplo '2000-01-01 10:00:00'
   */
  this.getTimestampFromDateAndTime = function(date, time){
    var timestamp = new Date(date);
    timestamp.setHours(time.getHours());
    timestamp.setMinutes(time.getMinutes());
    return timestamp;
  };


});
