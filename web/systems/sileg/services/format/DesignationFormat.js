angular
  .module('mainApp')
  .service('DesignationFormat',DesignationFormat);

DesignationFormat.inject = ["$q", "User", "Place", "Position", "UserFormat", "PlaceFormat", "PositionFormat"]

function DesignationFormat($q, User, Place, Position, UserFormat, PlaceFormat, PositionFormat) {
  Format.call(this);
  this.q = $q;
  
  this.userDao = User;
  this.placeDao = Place;
  this.positionDao = Position;
  
  this.userFormat = UserFormat;
  this.placeFormat = PlaceFormat;
  this.positionFormat = PositionFormat;

}

DesignationFormat.prototype = Object.create(Format.prototype);


DesignationFormat.prototype.initializeUser = function(fieldName, data, defecto){
  if(!defecto) defecto = null; 
  
  var deferred = this.q.defer();

  var user = {};
  var userId = this.defecto("userId", data, defecto);  

  self = this;
  if(userId){
    this.userDao.findById([userId]).then(
      function(rows){
        var userData = (rows.length) ? rows[0] : null
        self.userFormat.initialize(userData).then(
          function(user){ deferred.resolve(user); },
          function(error){ deferred.reject(error); }
        );
      },
      function(error){ deferred.reject(error); }
    );
  } else {
    deferred.resolve(null);
  }

  return deferred.promise;
}



DesignationFormat.prototype.initializePlace = function(fieldName, data, defecto){
  if(!defecto) defecto = null; 
  
  var deferred = this.q.defer();
  var placeId = this.defecto("placeId", data, defecto);  

  self = this;
  if(placeId){
    this.placeDao.findById([placeId]).then(
      function(rows){
        var placeData = (rows.length) ? rows[0] : null
        self.placeFormat.initialize(placeData).then(
          function(place){ deferred.resolve(place); },
          function(error){ deferred.reject(error); }
        );
      },
      function(error){ deferred.reject(error); }
    );
  } else {
    deferred.resolve(null);
  }

  return deferred.promise;
};


DesignationFormat.prototype.initializePosition = function(fieldName, data, defecto){
  if(!defecto) defecto = null; 
  
  var deferred = this.q.defer();
  var positionId = this.defecto("positionId", data, defecto);  

  self = this;
  if(positionId){
    this.positionDao.findById([positionId]).then(
      function(rows){
        var positionData = (rows.length) ? rows[0] : null
        self.positionFormat.initialize(positionData).then(
          function(position){ deferred.resolve(position); },
          function(error){ deferred.reject(error); }
        );
      },
      function(error){ deferred.reject(error); }
    );
  } else {
    deferred.resolve(null);
  }

  return deferred.promise;
}






//***** inicializar datos para ser visualizados en un formulario *****
DesignationFormat.prototype.initialize = function(data){
  var fields = {};
  var promises = [];
  var deferred = this.q.defer();
  
  fields["id"] = this.defecto("id", data);
  fields["start"] = this.date("start", data);
  fields["end"] = this.date("end", data);
  fields["description"] = this.defecto("description", data);  
  fields["record"] = this.defecto("record", data);
  fields["resolution"] = this.defecto("resolution", data);  
  
  var p1 = this.initializeUser("userId", data);
  var p2 = this.initializePlace("placeId", data)
  var p3 = this.initializePosition("positionId", data);

  this.q.all([p1, p2, p3]).then(
    function(response){ 
      fields["user"] = response[0],
      fields["place"] = response[1],
      fields["position"] = response[2],
      deferred.resolve(fields);
    },
 
    function(error) { deferred.reject(error); }
  );
  
  return deferred.promise;
};






