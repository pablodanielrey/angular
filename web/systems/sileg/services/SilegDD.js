(function() {
		'use strict'
		angular
			.module('sileg')
			.service('SilegDD', SilegDD);

		SilegDD.inject = ['Sileg'];

		function SilegDD($q, Sileg){

      this.getUsers = getUsers;
			this.getCathedras = getCathedras;
			this.findPositionsActiveByUser = findPositionsActiveByUser;



		  function getUsers() { return Sileg.getUsers(); };
			function getCathedras() { return Sileg.getCathedras(); };
			function findPositionsActiveByUser(userId) { return Sileg.findPositionsActiveByUser(userId); };







    };


})();
