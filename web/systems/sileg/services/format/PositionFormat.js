angular
  .module('mainApp')
  .service('PositionFormat',PositionFormat);

PositionFormat.inject = ["$q"];

function PositionFormat($q) {
  Format.call(this);
  this.q = $q;
};

PositionFormat.prototype = Object.create(Format.prototype);


//***** inicializar datos *****
PositionFormat.prototype.initialize = function(data){
  var fields = {};
  var deferred = this.q.defer();
  
  fields["id"] = this.defecto("id", data);
  fields["description"] = this.defecto("description", data);

  deferred.resolve(fields);
  
  return deferred.promise;

};
