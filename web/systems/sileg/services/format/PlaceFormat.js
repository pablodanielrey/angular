angular
  .module('mainApp')
  .service('PlaceFormat',PlaceFormat);

PlaceFormat.inject = ["$q"];

function PlaceFormat($q) {
  Format.call(this);
  this.q = $q;
};

PlaceFormat.prototype = Object.create(Format.prototype);


PlaceFormat.prototype.letter = function(data, defecto){
  var defecto = (defecto) ? defecto : null;
  return ("description" in data) ? letter = data.description.charAt(0).toUpperCase() : defecto;
};


//***** inicializar datos *****
PlaceFormat.prototype.initialize = function(data){
  var fields = {};
  var deferred = this.q.defer();
  
  fields["id"] = this.defecto("id", data);
  fields["description"] = this.defecto("description", data);
  fields["letter"] = this.letter(data);

  deferred.resolve(fields);
  
  return deferred.promise;

};
