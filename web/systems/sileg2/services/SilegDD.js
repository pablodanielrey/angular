(function() {
		'use strict'
		angular
			.module('sileg')
			.service('SilegDD', SilegDD);

		SilegDD.inject = ['Sileg'];

		function SilegDD($q, Sileg) {

      this.issueDetail = issueDetail; //get issue and childs witch users and creators

      function issueDetail(id){

      };
    }


})();
