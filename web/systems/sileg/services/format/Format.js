
//***** Metodos de uso general para dar formato *****
app.service("Format", Format);

function Format(){}


//***** Formatear una fecha *****
Format.prototype.defecto =  function(fieldName, data, defecto){
  if(!defecto) defecto = null;
  return (fieldName in data) ? data[fieldName] : defecto;
}


//***** Formatear un entero *****
Format.prototype.integer = function(fieldName, data, defecto){
  if(!defecto) defecto = null; 
  return (fieldName in data && !isNaN(parseInt(data[fieldName]))) ? parseInt(data[fieldName]) : defecto;
};


//***** Formatear una fecha *****
Format.prototype.date =  function(fieldName, data, defecto){
  if(!defecto) defecto = null; 
  var aux = (fieldName in data) ? data[fieldName] : null;

  if(aux){
    var date = new Date(aux); //se define un date con el dato de la base de datos... la base de datos esta en utc, el date se define con la fecha en utc pero la hora en formato local, por ende habra que sumar 3 horas.
    return new Date(date.getTime() + 180*60000); //sumamos 3 horas correspondientes a la hora local
  }
   
  return defecto;
 
};




/**
 * verificar y definir una fecha para ser enviada al servidor
 * @param {String} fieldName Nombre del field
 * @param {Fields} $fields Todos los fields
 *
 * @return {mixed} Resultado del chequeo: null (sin errores) string (descripción del error)
 */
Format.prototype.checkDate = function(fieldName, $fields, notNull){
  if($fields[fieldName] === undefined) return "Ingrese una fecha valida";
  if(!$fields[fieldName]) { return (notNull) ? "No puede estar vacío" : null; }
  return null;
};



