angular
  .module('mainApp')
  .service('Designation',Designation);

Designation.inject = ["$rootScope","$wamp", "$q"]

function Designation($rootScope, $wamp, $q) {

  //***** buscar por id *****
  this.findById = function(ids) { 
    var defer = $q.defer();
    
    var promise = $wamp.call('sileg.findDesignationsByIds', [ids]); 
    
    promise.then(
      function(designations){
        for(var i = 0; i < designations.length; i++){
          if(designations[i]["start"]){
            var date = new Date(designations[i]["start"]);
            designations[i]["start"] = new Date(date.getTime() + 180*60000); //sumamos 3 horas correspondientes a la hora local   Date(designations[i]["start"]);   
          }
        }
        defer.resolve(designations);
      },
      function(error){
        defer.reject(error);
      }
    );
    
    return defer.promise;
  };
  
  
    
  
  //***** buscar  *****
  this.findBySearch = function(search) { return $wamp.call('sileg.findDesignationsBySearch', [search]); }
  
  //***** persist *****
   this.persist = function(designation) { return $wamp.call('sileg.persistDesignation', [designation]); }
 
}
