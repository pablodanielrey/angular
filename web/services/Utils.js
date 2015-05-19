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
  
  this.getTimeFromSeconds = function(seconds) {
      var hours   = Math.floor(seconds / 3600);
      var minutes = Math.floor((seconds - (hours * 3600)) / 60);
      var secondsAux = seconds - (hours * 3600) - (minutes * 60);

      if (hours   < 10) {hours   = "0"+hours;}
      if (minutes < 10) {minutes = "0"+minutes;}
      if (secondsAux < 10) {secondsAux = "0"+secondsAux;}
      var time    = hours+':'+minutes;
      return time;
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



  //***** FORMATO DE JUSTIFICACIONES *****
  this.getJustificationName = function(justificationId){
    var j = this.getJustification(justificationId);
    return j.name;
  };

  this.getJustificationShortName = function(justificationId){
     var j = this.getJustification(justificationId);
     return j.shortName;
  };

  this.getJustificationIcon = function(justificationId){
    var j = this.getJustification(justificationId);
    return j.icon;
  };
  
  this.getJustificationRequestMode = function(justificationId){
    var j = this.getJustification(justificationId);
    return j.requestMode;
  };
  
  this.getJustificationStockMode = function(justificationId){
    var j = this.getJustification(justificationId);
    return j.stockMode;
  };
  
  
  /**
   * Obtener datos de la justificacion.
   * El metodo recibe como parametro el id de la justificacion y retorna los siguientes datos de la misma:
   *  id: Id
   *  name: Nombre
   *  shortName: Nombre corto
   *  icon: Icono
   *  requestMode: modo de solicitud, puede tomar los valores
   *    date: Se solicita una fecha
   *    dates: Se solicita un rango de fechas
   *    date,times: Se solicita una fecha y un rango de horarios
   *  stockMode: Modo del stock, puede tomar los valores
   *    total: Se considera solo el stock total
   *    none: No se considera stock
   *    total,year: Se considera stock total y anual
   *    
   * Consideracion  importante, para facilitar la administracion todos estos datos deberian ser posteriormente almacenados en la base de datos
   * 
   * @param {type} justificationId
   */
  this.getJustification = function(justificationId){
    switch(justificationId){
      case 'e0dfcef6-98bb-4624-ae6c-960657a9a741':
        return {id:justificationId, name:'Ausente con aviso', shortName:'AA', icon:'fa-ticket', requestMode:'date', stockMode:'year'};
      break;
      case '48773fd7-8502-4079-8ad5-963618abe725':
        return {id:justificationId, name:'Compensatorio', shortName:'C', icon:'fa-ticket', requestMode:'dates', stockMode:'total'};
      break;
      case 'fa64fdbd-31b0-42ab-af83-818b3cbecf46':
        return {id:justificationId, name:'Boleta de Salida', shortName:'BS', icon:'fa-ticket', requestMode:'times', stockMode:'yearTime'};
      break;
      case '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb':
        return {id:justificationId, name:'Art 102', shortName:'102', icon:'fa-ticket', requestMode:'date', stockMode:'year'};
      break;
      case 'b70013e3-389a-46d4-8b98-8e4ab75335d0':
        return {id:justificationId, name:'Pre-Exámen', shortName:'PE', icon:'fa-graduation-cap', requestMode:'dates', stockMode:'year'};
      break;
      case '76bc064a-e8bf-4aa3-9f51-a3c4483a729a':
        return {id:justificationId, name:'Licencia Anual Ordinaria', shortName:'LAO', icon:'fa-plane', requestMode:'dates', stockMode:'total'};
      break;
      case '50998530-10dd-4d68-8b4a-a4b7a87f3972':
        return {id:justificationId, name:'Resolución 638', shortName:'R', icon:'fa-file-text-o', requestMode:'dates', stockMode:'total'};
      break;
      case 'f9baed8a-a803-4d7f-943e-35c436d5db46':
        return {id:justificationId, name:'Licencia Médica Corta Duración', shortName:'MCD', icon:'fa-medkit', requestMode:'dates', stockMode:'none'};
      break;
      case 'a93d3af3-4079-4e93-a891-91d5d3145155':
        return {id:justificationId, name:'Licencia Médica Largo Tratamiento', shortName:'MLT', icon:'fa-medkit', requestMode:'dates', stockMode:'none'};
      break;
      case 'b80c8c0e-5311-4ad1-94a7-8d294888d770':
        return {id:justificationId, name:'Licencia Médica Atención Familiar', shortName:'MAF', icon:'fa-medkit', requestMode:'dates', stockMode:'none'};
      break;
      case '478a2e35-51b8-427a-986e-591a9ee449d8':
        return {id:justificationId, name:'Justificado por Médico', shortName:'JM', icon:'fa-medkit', requestMode:'dates', stockMode:'none'};
      break;
      case '5ec903fb-ddaf-4b6c-a2e8-929c77d8256f':
        return {id:justificationId, name:'Feriado', shortName:'F', icon:'fa-calendar', requestMode:'dates', stockMode:'none'};
      break;
      case '874099dc-42a2-4941-a2e1-17398ba046fc':
        return {id:justificationId, name:'Paro', shortName:'P', icon:'fa-calendar', requestMode:'dates', stockMode:'none'};
      break;
      case 'b309ea53-217d-4d63-add5-80c47eb76820':
        return {id:justificationId, name:'Cumpleaños', shortName:'CU', icon:'fa-birthday-cake', requestMode:'date', stockMode:'total'};
      break;
      case '0cd276aa-6d6b-4752-abe5-9258dbfd6f09':
        return {id:justificationId, name:'Duelo', shortName:'D', icon:'fa-circle', requestMode:'dates', stockMode:'none'};
      break;
      case 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b':
        return {id:justificationId, name:'Donación de Sangre', shortName:'DS', icon:'fa-tint', requestMode:'date', stockMode:'none'};
      break;
      default:
        return {id:justificationId, name:null, shortName:null, icon:null, requestMode:null, stockMode:null};
    }
  };
  
  
  /**
   * Dar formato a una solicitud de justificacion
   */
  this.formatRequestJustification = function(req) {
    var request = {
      id:null,
      justificationName:null,
      date:null,
      time:null,
      start:null,
      end:null,
      status:null
    };
    
    request.id = req.id;
    request.justificationName = this.getJustificationName(req.justification_id);
    request.status = req.status;
    
    if(req.begin !== null){
      var date = new Date(req.begin);
      request.date = this.formatDate(date);
    }
    
    if(req.end !== null){
      var date2 = new Date(req.end);
    }
    
    if(date && date2){
      request.time = this.getDifferenceTimeFromDates(date, date2);
      request.start = this.formatTime(date);
      request.end = this.formatTime(date2);
    }
    
    return request;
  };


  /**
   * Dar formato a una solicitud de justificacion
   */
  this.formatRequestJustification = function(req) {
    var request = {
      id:null,
      justificationName:null,
      date:null,
      dateSort:null,
      time:null,
      start:null,
      end:null,
      status:null
    };
    
    request.id = req.id;
    request.justificationName = this.getJustificationName(req.justification_id);
    request.status = req.status;
    
    if(req.begin !== null){
      var date = new Date(req.begin);
      request.date = this.formatDate(date);
      request.dateSort = date;
    }
    
    if(req.end !== null){
      var date2 = new Date(req.end);
    }
    
    if(date && date2){
      request.time = this.getDifferenceTimeFromDates(date, date2);
      request.start = this.formatTime(date);
      request.end = this.formatTime(date2);
    }
    
    return request;
  };

});

