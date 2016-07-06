angular
  .module('mainApp')
  .service('UserFormat',UserFormat);

UserFormat.inject = []

function UserFormat() {

  this.format = function(user) {
     letter = user.lastname.charAt(0).toUpperCase();
     return {id:user.id, letter:letter, name:user.name, lastname:user.lastname};
  }
  
  

  

}
