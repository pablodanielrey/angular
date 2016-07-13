angular
  .module('mainApp')
  .service('UserFormat',UserFormat);

UserFormat.inject = ["$q"];

function UserFormat($q) {
  Format.call(this);
  this.q = $q;
};

UserFormat.prototype = Object.create(Format.prototype);


UserFormat.prototype.letter = function(data, defecto){
  var defecto = (defecto) ? defecto : null;
  return ("lastname" in data) ? letter = data.lastname.charAt(0).toUpperCase() : defecto;
};



//***** inicializar datos *****
UserFormat.prototype.initialize = function(data){
  var fields = {};
  var promises = [];
  var deferred = this.q.defer();
  
  
  fields["id"] = this.defecto("id", data);
  fields["name"] = this.defecto("name", data);
  fields["lastname"] = this.defecto("lastname", data);
  fields["letter"] = this.letter(data);

  deferred.resolve(fields);
  
  return deferred.promise;

};
