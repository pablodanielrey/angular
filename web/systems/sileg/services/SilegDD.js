(function() {
		'use strict'
		angular
			.module('sileg')
			.service('SilegDD', SilegDD);

		SilegDD.inject = ['Sileg'];

		function SilegDD($q, Sileg){
      var self = this;
      this.getUsers = getUsers;
			this.getPlaces = getPlaces;
			this.findPositionsActiveByUser = findPositionsActiveByUser;
			this.findPositionsActiveByPlace = findPositionsActiveByPlace;
      this._defineLetter = _defineLetter



		  function getUsers() { return Sileg.getUsers().then(
 			  function(users){ return self._defineLetter(users, "lastname"); }
			)};

			function getPlaces() { return Sileg.getPlaces().then(
 			  function(users){ return self._defineLetter(users, "name"); }
			)};

			function findPositionsActiveByUser(userId) { return Sileg.findPositionsActiveByUser(userId); };
			function findPositionsActiveByPlace(placeId) { return Sileg.findPositionsActiveByPlace(placeId); };

			function _defineLetter(data, key) {
         for (var i = 0; i < data.length; i++){
					 data[i].letter = data[i][key].charAt(0)
				 }
				 return data;
			}

    };


})();
