
//***** Metodos de uso general para dar formato *****
app.service("Format", Format);

function Format(){}


//***** Formatear una fecha *****
Format.prototype.defecto =  function(fieldName, data, defecto){
  return (fieldName in data) ? data[fieldName] : defecto;
}


//***** Formatear un entero *****
Format.prototype.integer = function(fieldName, data, defecto){
  return (fieldName in data && !isNaN(parseInt(data[fieldName]))) ? parseInt(data[fieldName]) : defecto;
};


//***** Formatear una fecha *****
Format.prototype.date =  function(fieldName, data, defecto){
  var aux = (fieldName in data) ? data[fieldName] : null;

  if(aux){
    var date = new Date(aux); //se define un date con el dato de la base de datos... la base de datos esta en utc, el date se define con la fecha en utc pero la hora en formato local, por ende habra que sumar 3 horas.
    return new Date(date.getTime() + 180*60000); //sumamos 3 horas correspondientes a la hora local
  }
   
  return defecto;
 
};













//***** Cantidad de anios entre dos fechas *****
Format.prototype.yearsFromDates = function(date1, date2) {
  date2 = (date2 == undefined) ? Date.now() : date2;
  var ageDifMs = date2 - date1.getTime();
  var ageDate = new Date(ageDifMs); // miliseconds from epoch
  return Math.abs(ageDate.getUTCFullYear() - 1970);
};


/**
 * Format typeahead
 * @param {type} fieldName
 * @param {type} alias
 * @param {type} $fields
 * @param {type} config
 * @param {type} data
 * @returns {undefined}
 */
Format.prototype.typeahead = function(fieldName, label, $fields, data, defecto, params){
  $fields[fieldName] = (fieldName in params && params[fieldName]) ? params[fieldName] : defecto;
  if (fieldName in data && data[fieldName]) $fields[fieldName] = data[fieldName];
  $fields[fieldName + "_search"] = null; //string con la busqueda
  $fields[fieldName + "_selected"] = null; //objeto con los datos de la seleccion

  if($fields[fieldName]){
    this.EntityAccess.rowById($fields[fieldName], label)
    .then(
      function(response){ if ("id" in response.data) $fields[fieldName + "_selected"] = response.data; }
    );
  }
};


/**
 * Formatear una fecha recibida del servidor
 * @param {Fields} fields Todos los fields
 * @param {String} fieldName Nombre del field
 * @param {Array} data Datos de los fields recibidos del servidor
 */
Format.prototype.formatTime =  function(fieldName, fields, data, defecto){
  defecto = (defecto) ? defecto : null;

  fields[fieldName] = (fieldName in data) ? data[fieldName] : null;  
  fields[fieldName + "_time"] = null;
  if(fields[fieldName]){
    var date = new Date();
    var time = fields[fieldName].split(":");
    date.setHours(time[0]);
    date.setMinutes(time[1]);
    date.setSeconds(0);
    fields[fieldName+"_time"] = date;
  } else {
    if(defecto == "CURRENT_TIME"){
      var date = new Date();
      date.setSeconds(0);
      fields[fieldName+"_time"] = date;
      
    }
  }
};


//***** Reformatear una hora *****
Format.prototype.reformatTime = function(fieldName, $fields, isNotNull){
  $fields[fieldName] = null;
  if($fields[fieldName + "_time"] === undefined) return "Ingrese una hora válida";
  if($fields[fieldName + "_time"] == null) {
    $fields[fieldName] = "null";
    return (isNotNull) ? "No puede estar vacío" : null;
  }
  
  var timeAux = new Date($fields[fieldName + "_time"].getTime() - 180*60000);
  $fields[fieldName] = timeAux.toISOString().substring(11, 19);
  return null;
}









//***** Formatear una fecha recibida a partir de un string *****
/**
 * @param format String con el formato de fecha
 *   "yyyymmdd"
 *   "dd/mm/yyyy" Defecto
 */
Format.prototype.dateString =  function(fieldName, $fields, data, format){
  $fields[fieldName] = (fieldName in data) ? data[fieldName] : null;
  $fields[fieldName + "_date"] = null;
  if($fields[fieldName]){
    var dateAux = new Date($fields[fieldName]); //se define un date con el dato de la base de datos... la base de datos esta en utc, el date se define con la fecha en utc pero la hora en formato local, por ende habra que sumar 3 horas.
    var date = new Date(dateAux.getTime() + 180*60000); //sumamos 3 horas correspondientes a la hora local
    
    switch(format){
      case "yyyymmdd":
        $fields[fieldName + "_date"] = date.toISODateString();
      break;
      
      case "F":
         $fields[fieldName + "_date"] = date.getMonthName();
      break;
      
      default:
        $fields[fieldName + "_date"] = date.toLocaleDateStringZero();
    }
  }
};

  
/**
 * Formatear una fecha recibida del servidor
 * @param {Fields} fields Todos los fields
 * @param {String} fieldName Nombre del field
 * @param {Array} data Datos de los fields recibidos del servidor
 */
Format.prototype.formatTimestamp =  function(fieldName, fields, data){
  fields[fieldName] = (fieldName in data) ? data[fieldName] : null;
  fields[fieldName + "_date"] = null;
  fields[fieldName + "_time"] = null;
  if(fields[fieldName]){
    var date = new Date(fields[fieldName]); //se define un date con el dato de la base de datos... la base de datos esta en utc, el date se define con la fecha en utc pero la hora en formato local, por ende habra que sumar 3 horas.
    fields[fieldName+"_date"] = new Date(date.getTime() + 180*60000); //sumamos 3 horas correspondientes a la hora local
    fields[fieldName+"_time"] = new Date(date.getTime()); //sumamos 3 horas correspondientes a la hora local
  }
};
  
  
//***** formatear textarea: crea un substring de 100 caracteres *****
Format.prototype.formatTextarea = function(fieldName, fields, data){
  var text = (fieldName in data) ? data[fieldName] : null;
  fields[fieldName] = (text) ? text : null;
  if(text){
    if(text.length > 100) fields[fieldName + "_summary"] = text.substring(0,100) + "...";
    else fields[fieldName + "_summary"] = text;
  } else {
    fields[fieldName + "_summary"] = null;
  } 
};
  



  
Format.prototype.getAdvancedSearchOptionsBoolean = function(){
  return [ 
    {label: "activado", hasValue:false},
    {label: "desactivado", hasValue:false}
  ];
};
  
Format.prototype.getAdvancedSearchOptionsDefault = function(){
  return [ 
    {label: "igual", hasValue:true},
    {label: "desde", hasValue:true},
    {label: "hasta", hasValue:true},
    {label: "distinto", hasValue:true},
    {label: "vacío", hasValue:false},
    {label: "no vacío", hasValue:false}
  ];
};
  



//****** obtener etiqueta de datos ******
//@param field Nombre del field
//@param value Valor del field
//@param label Etiqueta
Format.prototype.fieldLabel = function(fieldName, label, fields, data){
  fields[fieldName] = (data[fieldName]) ? data[fieldName] : null;
  if(!fields[fieldName]) return;
  var item = this.LocalStorage.getItem(label+fields[fieldName]);
  
  if(item){
    fields[fieldName + "_label"] = item["label"];
    return;
  }
  
  var self = this;
  this.EntityAccess.rowById(fields[fieldName], label).then(
    function(response){
      
      if(response.data){
        self.LocalStorage.setItem(label+fields[fieldName], response.data);
        fields[fieldName + "_label"] = response.data["label"];
      }
    },
    function(error){ console.log(error); }
  );
};
  
  

/**
 * Dar formato a opcion
 * @param {String} fieldName Nombre del field
 * @param {Array} fields Conjunto de fields
 * @param {Array} data Lista de datos (se envia toda la lista para comprobar existencia)
 * @param {Array} options Lista de opciones (se envia toda la lista para comprobar existencia)
 */
Format.prototype.formatSelectArrayGrid = function(fieldName, fields, data, options){
  fields[fieldName] = (fieldName in data) ? data[fieldName] : null; //se inicializa con el valor del fieldName por si no existe la opcion correspondiente
  if(!(fieldName in options)) return; //se chequea la existencia de las opciones

  for(var i = 0; i < options[fieldName].length; i++) {
    if(data[fieldName] == options[fieldName][i].id) {
      fields[fieldName] = options[fieldName][i].label;
      break;
    }
  }  
};






//***** Definir opcion seleccionada a partir de un conjunto de opciones *****
//Define 3 elementos fieldName, fieldName_selected y fieldName_label
Format.prototype.optionSelected = function(fieldName, $fields, data, options){
  $fields[fieldName] = (fieldName in data) ? data[fieldName] : null; //inicializar con el valor del fieldName por si no existe la opcion correspondiente
  if(!(fieldName in options)) return; //verificar existencia de opciones
  $fields[fieldName + "_selected"] = null; //inicializar valor selected
  for(var i = 0; i < options[fieldName].length; i++) {
    if(data[fieldName] == options[fieldName][i].id) {
      $fields[fieldName + "_selected"] = options[fieldName][i];
      $fields[fieldName + "_label"] = options[fieldName][i]["label"];

      break;
    }
  }  
};
    





  
Format.prototype.formatWeekday = function(fieldName, $fields, data){
  $fields[fieldName] = (fieldName in data) ? data[fieldName] : null;
  $fields[fieldName + "_selected"] = $fields[fieldName];
  if (fieldName in data) {
    var weekdays = Array("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo");
    var weekday = weekdays[parseInt(data[fieldName])];
    if(weekday) $fields[fieldName + "_string"] = weekday;
  }
  

};
  
  



  


/**
 * Obtener opciones autocompletar
 * @param {type} fieldsetId Identificador del fieldset
 * @param {type} search Busqueda
 * @param {type} tableName Nombre de la tabla
 */
Format.prototype.getTypeaheadOptions = function(search, fieldName, $fields, tableName){
  $fields[fieldName+"_search"] = search; //se debe actualizar el valor para que el controlador se de cuenta e que se esta buscando un nuevo valor (creo que al ingresar un nuevo valor se accede al metodo selectTypeahead donde se verifican ciertas condiciones que incluyen a "search" y permiten decidir si se encuentra definido o no el typeahead

  if(search.length < 4) return "";

  return this.EntityAccess.typeaheadSearch(search, tableName)
    .then(
      function(response){ return response.data; },
      function(error){ return error; }
    );
};

  
/**
 * Seleccionar typeahead
 * @param $fields Fields para modificar valores en base a la busqueda y seleccion del typeahead
 * @return boolean true Si se selecciono algun valor de typeahead, false en caso contrario
 */
Format.prototype.selectTypeahead = function(fieldName, $fields){
  if(($fields[fieldName + "_selected"]) && (typeof $fields[fieldName + "_selected"] === "object")){
    $fields[fieldName] = $fields[fieldName + "_selected"]["id"];
    return true;
  } 

  //si esta definido el fieldName y no esta definido el fieldName + "_search" signfica que el dato fue inicializado directamente de la base de datos
  else if(($fields[fieldName]) && (!$fields[fieldName + "_search"])){
    return true;
  }

  $fields[fieldName] = null;
  return false;
};
  
  
  










//***** Inicializar checkbox *****
Format.prototype.initCheckbox = function(fieldName, $fields, data, defaultValue){
  var aux = (fieldName in data) ? data[fieldName] : defaultValue;
  $fields[fieldName] = ((aux == "1") || (aux == "t")) ? true : false;
};

/**
 * Inicializar archivo
 * @param {String} fieldName Nombre del field
 * @param {Array} fields Fields del fieldset
 * @param {Array} data Datos del servidor
 * @returns {undefined}
 */
Format.prototype.initFile = function(fieldName, alias, $fields, data){
  $fields[fieldName] = (fieldName in data) ? data[fieldName] : null;
  $fields[fieldName+"_nombre"] = (alias+"_nombre" in data) ? data[alias+"_nombre"] : null;
  $fields[fieldName+"_contenido"] = (alias+"_contenido" in data) ? data[alias+"_contenido"] : null;
};






//***** Verificar y definir un entero para ser enviado al servidor *****
Format.prototype.checkInt = function(fieldName, $fields, $server, notNull, length){
  $server[fieldName] = "null";
  if(($fields[fieldName] == null) || ($fields[fieldName] == undefined) || ($fields[fieldName] === "")) return (notNull) ? 'No puede estar vacío': null;
  if(parseInt(length)) if(($fields[fieldName]) && ($fields[fieldName].length > length)) return "No puede superar " + length + " caracteres";
  var re = /^\d+$/;
  if(!re.test($fields[fieldName])) return "Ingrese un número válido";
  $server[fieldName] = $fields[fieldName];
  return null;
};



//***** Verificar y definir un flotante para ser enviado al servidor *****
Format.prototype.checkFloat = function(fieldName, $fields, $server, notNull, length){
  $server[fieldName] = "null";
  if(($fields[fieldName] == null) || ($fields[fieldName] == undefined) || ($fields[fieldName] === "")) return (notNull) ? 'No puede estar vacío': null;
  if(parseInt(length)) if(($fields[fieldName]) && ($fields[fieldName].length > length)) return "No puede superar " + length + " caracteres";
  if(typeof $fields[fieldName] == "string") $fields[fieldName] = $fields[fieldName].replace(",", ".");
  var re = /^[+-]?\d+(\.\d+)?$/;
  if(!re.test($fields[fieldName])) return "Ingrese un número válido";
  $server[fieldName] = $fields[fieldName];
  return null;
};
  

/**
 * verificar y definir una fecha para ser enviada al servidor
 * @param {String} fieldName Nombre del field
 * @param {Fields} $fields Todos los fields
 *
 * @return {mixed} Resultado del chequeo: null (sin errores) string (descripción del error)
 */
Format.prototype.checkDate = function(fieldName, $fields, $server, notNull){
  $server[fieldName] = "null";
  if($fields[fieldName + "_date"] === undefined) return "Ingrese una fecha valida";
  if(!$fields[fieldName + "_date"]) { return (notNull) ? "No puede estar vacío" : null; }
  var d = $fields[fieldName + "_date"];
  $server[fieldName] = [ d.getFullYear(), (d.getMonth()+1).padLeft(), d.getDate().padLeft()].join('-');
  return null;
};

/**
 * formatear una fecha t hora para ser enviada al servidor
 * @param {String} fieldName Nombre del field
 * @param {Fields} $fields Todos los fields
 *
 * @return {mixed} Resultado del chequeo: null (sin errores) string (descripción del error)
 */
Format.prototype.checkTimestamp = function(fieldName, $fields, $server, notNull){
  $server[fieldName] = "null";

  var date = null;
  var time = null;    

  if($fields[fieldName + "_date"] === undefined) return "Ingrese una fecha valida";
  if(!$fields[fieldName + "_date"]) { return (notNull) ? "No puede estar vacía la fecha" : null; }
  var d = $fields[fieldName + "_date"];
  var date = [ d.getFullYear(), (d.getMonth()+1).padLeft(), d.getDate().padLeft()].join('-')

  if($fields[fieldName + "_time"] === undefined) return "Ingrese una hora válida";
  if(!$fields[fieldName + "_time"]) { return (notNull) ? "No puede estar vacía la hora" : null; }  

  var timeAux = new Date($fields[fieldName + "_time"].getTime() - 180*60000);
  time = timeAux.toISOString().substring(11, 19);
  
  if(date && time) $server[fieldName] = date + " " + time;
  return null;

};


//***** Chequear y definir hora para enviar al servidor *****
Format.prototype.checkTime = function(fieldName, $fields, $server, notNull){
  $server[fieldName] = "null";

  if($fields[fieldName + "_time"] === undefined) return "Ingrese una hora válida";
  if(!$fields[fieldName + "_time"]) { return (notNull) ? "No puede estar vacío" : null; }  

  var time = new Date($fields[fieldName + "_time"].getTime() - 180*60000);
  $server[fieldName] = time.toISOString().substring(11, 19);
  return null;
};


//***** Chequear y definir anio para enviar al servidor *****
Format.prototype.checkYear = function(fieldName, $fields, $server, notNull){
  $server[fieldName] = "null";
  if($fields[fieldName + "_date"] === undefined) return "Ingrese una año válido";
  if(!$fields[fieldName + "_date"]) { return (notNull) ? "No puede estar vacío" : null; }
  var d = $fields[fieldName + "_date"];
  $server[fieldName] = [ d.getFullYear(), (d.getMonth()+1).padLeft(), d.getDate().padLeft()].join('-');
  return null;
};


//***** Verificar y definir un entero para ser enviado al servidor *****
Format.prototype.checkName = function(fieldName, $fields, $server, notNull, length){
  $server[fieldName] = "null";
  if((!$fields[fieldName]) || ($fields[fieldName] == "")) return (notNull) ? 'No puede estar vacío': null;
  if(parseInt(length)) if(($fields[fieldName]) && ($fields[fieldName].length > length)) return "No puede superar " + length + " caracteres";
  var re = /^([a-z ñáéíóú']{2,60})$/i;
  if(!re.test($fields[fieldName])) return "Ingrese un nombre válido";
  $server[fieldName] = $fields[fieldName];
  return null;
};


//***** Verificar y definir un entero para ser enviado al servidor *****
Format.prototype.checkEmail = function(fieldName, $fields, $server, notNull, length){
  $server[fieldName] = "null";
  if((!$fields[fieldName]) || ($fields[fieldName] == "")) return (notNull) ? 'No puede estar vacío': null;
  if(parseInt(length)) if(($fields[fieldName]) && ($fields[fieldName].length > length)) return "No puede superar " + length + " caracteres";
  var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
  if(!re.test($fields[fieldName])) return "Ingrese un email válido";
  $server[fieldName] = $fields[fieldName];
  return null;
};



//***** Verificar y definir un entero para ser enviado al servidor *****
Format.prototype.checkFile = function(fieldName, $fields, $server, notNull, length){
  $server[fieldName] = "null";
  if(
    (!$fields[fieldName + "_file"]) || ($fields[fieldName + "_file"] == "")
    && (!$fields[fieldName + "_file"]) || ($fields[fieldName + "_file"] == "")
  ) return (notNull) ? 'No puede estar vacío': null;
  //if(parseInt(length)) if(($fields[fieldName]) && ($fields[fieldName].length > length)) return "No puede superar " + length + " caracteres";
  $server[fieldName] = $fields[fieldName + "_file"];
  return null;
};



Format.prototype.checkSelect = function(fieldName, $fields, $server, notNull){
  $server[fieldName] = "null";
  if((!$fields[fieldName + "_selected"]) || ($fields[fieldName + "_selected"] == "")) return (notNull) ? 'Debe seleccionar una opción': null;

  $server[fieldName] = ($fields[fieldName + "_selected"]) ? $fields[fieldName + "_selected"].id : "null";
  return null;
};

//***** Verificar y definir un checkbox para ser enviado al servidor *****
Format.prototype.checkCheckbox = function(fieldName, $fields, $server){
  $server[fieldName] = $fields[fieldName];
};

//***** Verificar y definir un flotante para ser enviado al servidor *****
Format.prototype.checkDefault = function(fieldName, $fields, $server, notNull, length){
  $server[fieldName] = "null";
  if((!$fields[fieldName]) || ($fields[fieldName] === "")) return (notNull) ? 'No puede estar vacío': null;
  if(parseInt(length)) if(($fields[fieldName]) && ($fields[fieldName].length > length)) return "No puede superar " + length + " caracteres";
  $server[fieldName] = $fields[fieldName];
  return null;
};







//***** definir field de busqueda avanzada date *****
Format.prototype.initializeSearchAdvancedDate = function(field, label, notNull){
  var input = (notNull) ? "main/html/search/inputDateNotNull.html" : "main/html/search/inputDateNull.html"
  return {field:field, label:label, input:input, option:"equal", value:null};
}

//***** definir field de busqueda avanzada text *****
Format.prototype.initializeSearchAdvancedText = function(field, label, notNull){
  var input = (notNull) ? "main/html/search/inputTextNotNull.html" : "main/html/search/inputTextNull.html"
  return {field:field, label:label, input:input, option:"approx", value:null};
}










//***** definir busqueda de date *****
Format.prototype.defineSearchDate = function($fields, $server, $index){
  if(!$fields[$index]["field"]) return;
  $server[$index] = {};
  $server[$index]["field"] = $fields[$index]["field"];
  $server[$index]["option"] = $fields[$index]["option"];
  $server[$index]["value"] = null;
  
  if(!$fields[$index]["value"]) { return; }
  var d = $fields[$index]["value"];
  $server[$index]["value"] = [ d.getFullYear(), (d.getMonth()+1).padLeft(), d.getDate().padLeft()].join('-');
};


//***** definir busqueda por defecto *****
Format.prototype.defineSearchDefault = function($fields, $server, $index){
  if(!$fields[$index]["field"]) return;
  $server[$index] = {};
  $server[$index]["field"] = $fields[$index]["field"];
  $server[$index]["option"] = $fields[$index]["option"];
  $server[$index]["value"] = $fields[$index]["value"];
};

