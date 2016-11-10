(function() {
		'use strict'
		angular
			.module('sileg')
			.service('Sileg', Sileg);

		Sileg.inject = ['$window', '$q', 'Login'];

		function Sileg($window, $q, Login) {

		  this.getUsers = getUsers;
			this.getCathedras = getCathedras;
			this.getPositionsByUser = getPositionsByUser;
			this.getPositionsByCathedra = getPositionsByCathedra;
			this.getCathedrasByIds = getCathedras;
			this.getUsersByIds = getCathedras;


		  function getUsers() {
        return $q.when([
					{id:1, name:"Ivan", lastname:"Castañeda",dni:31073351},
					{id:2, name:"Juan", lastname:"Pérez",dni:31123456}
				]);
		    //return Login.getPublicTransport().call('sileg.users');
  	  };

			function getCathedras() {
        return $q.when([
					{id:1,description:"Lengua"},
					{id:2,description:"Matemática"}
				]);
		    //return Login.getPrivateTransport().call('sileg.cathedras', [regex]);
  	  };

			function getPositionsByUser(user) {
				return $q.when([
					{id:1, cathedra:1, user:1},
					{id:2, cathedra:2, user:1},
				]);
				//return Login.getPrivateTransport().call('sileg.positionByUser', [regex]);
			};

			function getPositionsByCathedra(cathedra) {
				return $q.when([
					{id:1, cathedra:1, user:1},
					{id:3, cathedra:1, user:2},
				]);
				//return Login.getPrivateTransport().call('sileg.positionByCathedra', [regex]);
			};


		}



})();
