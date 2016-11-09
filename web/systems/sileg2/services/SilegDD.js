(function() {
		'use strict'
		angular
			.module('sileg')
			.service('SilegDD', SilegDD);

		SilegDD.inject = ['Sileg'];

		function SilegDD($q, Sileg){

      this.getTeachers = getTeachers;
			this.getCathedras = getCathedras;
			this.getCathedrasByIds = getCathedras;
			this.getUsersByIds = getCathedras;
			this.getPositionsByUser = getPositionsByUser;
			this._assignCathedrasToPositions = _assignCathedrasToPositions;
			this._assignUsersToPositions = _assignUsersToPositions;


		  function getTeachers() { return Sileg.getTeachers(); };
			function getCathedras() { return Sileg.getCathedras(); };
			function getCathedrasByIds(ids) { return Sileg.getCathedrasByIds(ids); };
			function getUsersByIds(ids) { return Sileg.getUsersByIds(ids); };


			function _assignCathedrasToPositions(positions){
				var ids = [];
				for (var i = 0; i < positions.length; i++){	ids.push(positions[i].cathedra);	}
				if(!ids.length) return $q.when(positions);

				return this.getCathedrasByIds(ids).then(
					function(cathedras){
						for(var i = 0; i < positions.length; i++){
							for(var j = 0; j < cathedras.length; j++){ positions[i].cathedra_ = (position[i].cathedra == cathedras[j].id) ? cathedras[j] : null; }
						}
						return positions;
					}
				)
			}

			function _assignUsersToPositions(positions){
				var ids = [];
				for (var i = 0; i < positions.length; i++){	ids.push(positions[i].user);	}
				if(!ids.length) return $q.when(positions);

				return this.getUsersByIds(ids).then(
					function(users){
						for(var i = 0; i < positions.length; i++){
							for(var j = 0; j < users.length; j++){ positions[i].user_ = (position[i].users == cathedras[j].id) ? users[j] : null; };
						}
						return positions;
					}
				)
			}

			function getPositionsByUser(user) { return Sileg.getPositionsByUser(user).then(_assignCathedrasToPositions); };
			function getPositionsByCathedra(cathedra) { return Sileg.getPositionsByCathedra(cathedra).then(_assignUsersToPositions); };


    };


})();
