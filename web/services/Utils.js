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
    retorna el día de la semana asignado a cierta fecha.
  */
  this.getDayShortName = function(date) {
    var weekday = new Array(7);
    weekday[0]=  "Dom";
    weekday[1] = "Lun";
    weekday[2] = "Mar";
    weekday[3] = "Mie";
    weekday[4] = "Jue";
    weekday[5] = "Vie";
    weekday[6] = "Sab";
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




  /**
   * Obtener datos de la justificacion.
   * El metodo recibe como parametro el id de la justificacion y retorna los siguientes datos de la misma:
   *  id: Id
   *  name: Nombre
   *  shortName: Nombre corto
   *  icon: Icono
   *
   * Consideracion  importante, para facilitar la administracion todos estos datos deberian ser posteriormente almacenados en la base de datos
   *
   * @param {type} justificationId
   */
  this.getJustification = function(justificationId){
    switch(justificationId){
      case 'e0dfcef6-98bb-4624-ae6c-960657a9a741':
        return {id:justificationId, name:'Ausente con aviso', shortName:'AA', icon:'fa-ticket'};
      break;
      case '48773fd7-8502-4079-8ad5-963618abe725':
        return {id:justificationId, name:'Compensatorio', shortName:'C', icon:'fa-ticket'};
      break;
      case 'fa64fdbd-31b0-42ab-af83-818b3cbecf46':
        return {id:justificationId, name:'Boleta de Salida', shortName:'BS', icon:'fa-ticket'};
      break;
      case '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb':
        return {id:justificationId, name:'Art 102', shortName:'102', icon:'fa-ticket'};
      break;
      case 'b70013e3-389a-46d4-8b98-8e4ab75335d0':
        return {id:justificationId, name:'Pre-Exámen', shortName:'PE', icon:'fa-graduation-cap'};
      break;
      case '76bc064a-e8bf-4aa3-9f51-a3c4483a729a':
        return {id:justificationId, name:'Licencia Anual Ordinaria', shortName:'LAO', icon:'fa-plane'};
      break;
      case '50998530-10dd-4d68-8b4a-a4b7a87f3972':
        return {id:justificationId, name:'Resolución 638', shortName:'R', icon:'fa-file-text-o'};
      break;
      case 'f9baed8a-a803-4d7f-943e-35c436d5db46':
        return {id:justificationId, name:'Licencia Médica Corta Duración', shortName:'MCD', icon:'fa-medkit'};
      break;
      case 'a93d3af3-4079-4e93-a891-91d5d3145155':
        return {id:justificationId, name:'Licencia Médica Largo Tratamiento', shortName:'MLT', icon:'fa-medkit'};
      break;
      case 'b80c8c0e-5311-4ad1-94a7-8d294888d770':
        return {id:justificationId, name:'Licencia Médica Atención Familiar', shortName:'MAF', icon:'fa-medkit'};
      break;
      case '478a2e35-51b8-427a-986e-591a9ee449d8':
        return {id:justificationId, name:'Justificado por Médico', shortName:'JM', icon:'fa-medkit'};
      break;
      case '5ec903fb-ddaf-4b6c-a2e8-929c77d8256f':
        return {id:justificationId, name:'Feriado', shortName:'F', icon:'fa-calendar'};
      break;
      case '874099dc-42a2-4941-a2e1-17398ba046fc':
        return {id:justificationId, name:'Paro', shortName:'P', icon:'fa-calendar'};
      break;
      case 'b309ea53-217d-4d63-add5-80c47eb76820':
        return {id:justificationId, name:'Cumpleaños', shortName:'CU', icon:'fa-birthday-cake'};
      break;
      case '0cd276aa-6d6b-4752-abe5-9258dbfd6f09':
        return {id:justificationId, name:'Duelo', shortName:'D', icon:'fa-circle'};
      break;
      case 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b':
        return {id:justificationId, name:'Donación de Sangre', shortName:'DS', icon:'fa-tint'};
      break;
      case 'cb2b4583-2f44-4db0-808c-4e36ee059efe':
        return {id:justificationId, name:'Boleta en Comisión', shortName:'BC', icon:'fa-ticket'};
      break;
      case '5c548eab-b8fc-40be-bb85-ef53d594dca9':
        return {id:justificationId, name:'Día del Bibliotecario', shortName:'B', icon:'fa-calendar'};
      break;
      case '508a9b3a-e326-4b77-a103-3399cb65f82a':
        return {id:justificationId, name:'Congresos / Capacitación', shortName:'CC', icon:'fa-ticket'};
      break;
      case '70e0951f-d378-44fb-9c43-f402cbfc63c8':
        return {id:justificationId, name:'ART', shortName:'ART', icon:'fa-ticket'};
      break;
      case '3d486aa0-745a-4914-a46d-bc559853d367':
        return {id:justificationId, name:'Incumbencias Climáticas', shortName:'IC', icon:'fa-ticket'};
      break;

      case '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7':
        return {id:justificationId, name:'Entrada Tarde Justificada', shortName:'ET', icon:'fa-ticket'};
      break;

      case 'c32eb2eb-882b-4905-8e8f-c03405cee727':
        return {id:justificationId, name:'Justificado Por Autoridad', shortName:'AUT', icon:'fa-ticket'};
      break;

      case 'aa41a39e-c20e-4cc4-942c-febe95569499':
        return {id:justificationId, name:'Licencia Médica Pre-Natal. Art 106P', shortName:'PRN', icon:'fa-ticket'};
      break;

      case '68bf4c98-984d-4b71-98b0-4165c69d62ce':
        return {id:justificationId, name:'Licencia Médica Pos-Natal', shortName:'PON', icon:'fa-ticket'};
      break;

      case 'e249bfce-5af3-4d99-8509-9adc2330700b':
        return {id:justificationId, name:'Nacimiento', shortName:'NAC', icon:'fa-ticket'};
      break;

      case '5289eac5-9221-4a09-932c-9f1e3d099a47':
        return {id:justificationId, name:'Concurso', shortName:'CON', icon:'fa-ticket'};
      break;

      case 'f7464e86-8b9e-4415-b370-b44b624951ca':
        return {id:justificationId, name:'Receso de Invierno', shortName:'INV', icon:'fa-ticket'};
      break;

      case '30a249d5-f90c-4666-aec6-34c53b62a447':
        return {id:justificationId, name:'Matrimonio', shortName:'MAT', icon:'fa-ticket'};
      break;

      case '1c14a13c-2358-424f-89d3-d639a9404579':
        return {id:justificationId, name:'Licencia Sin Goce de Sueldo', shortName:'SGS', icon:'fa-ticket'};
      break;

      case 'bfaebb07-8d08-4551-b264-85eb4cab6ef1':
        return {id:justificationId, name:'Suspensión', shortName:'SUS', icon:'fa-ticket'};
      break;

      case '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9':
        return {id:justificationId, name:'Viaje', shortName:'VJE', icon:'fa-ticket'};
      break;


      default:
        return {id:justificationId, name:null, shortName:null, icon:null};
    }
  };


  /**
   * Dar formato a una solicitud de justificacion
   */
  this.formatRequestJustification = function(req) {
    var request = {
      id:null,
      justificationId:null,
      justificationName:null,
      requestorId:null,
      userId:null,
      dateSort:null,
      time:null,
      start:null,
      end:null,
      status:null
    };

    request.id = req.id;
    request.justificationName = this.getJustificationName(req.justification_id);
    request.justificationId = req.justification_id;
    request.requestorId = req.requestor_id;
    request.userId = req.user_id;
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

    if(request.justificationId=== 'cb2b4583-2f44-4db0-808c-4e36ee059efe'){
      request.start = this.formatTime(date);
    }

    return request;
  };

});
