angular
  .module('mainApp')
  .service('DesignationFormat',DesignationFormat);

DesignationFormat.inject = ["Users"]

function DesignationFormat(Users) {
  Format.call(this);
  
  this.userServer = Users;

}

DesignationFormat.prototype = Object.create(Format.prototype)


DesignationFormat.prototype.user = function(fields, data, defecto){
  this.defecto("userId", fields, data, null);  
  
  var userId = (fieldName in data) ? data[fieldName] : defecto;

  if(userId){
    this.userServer.findById([userId]).then(
      function(response){
        console.log(user);
      },
      function(error){
        console.log(error)
      }
    );
  }
}


//***** inicializar datos para ser visualizados en un formulario *****
DesignationFormat.prototype.initializeForm = function(data){
  var fields = {}; //un metodo de inicializacion puede definir varios valores para un mismo field
  
  this.integer("id", fields, data, null);
  this.date("start", fields, data, null);
  this.date("end", fields, data, null);
  this.defecto("description", fields, data, null);  
  this.user(fields, data, null);
};

