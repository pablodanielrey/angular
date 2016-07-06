angular
  .module('mainApp')
  .service('PlaceFormat',PlaceFormat);

PlaceFormat.inject = []

function PlaceFormat() {

  this.format = function(place) {
     letter = place.description.charAt(0).toUpperCase();
     return {id:place.id, letter:letter, description:place.description};
  }
  
  

  

}
