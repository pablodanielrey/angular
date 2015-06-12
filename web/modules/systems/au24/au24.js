var app = angular.module('mainApp');

app.controller("Au24Ctrl", function($scope, $rootScope, $timeout, Au24, Session) {

	$scope.loadAu24Data = function() {
		var session = Session.getCurrentSession();

	    if (session == null) {
	      return;
	    }

	    if (session.selectedUser == undefined || session.selectedUser == null) {
	      return;
		}


		Au24.findAu24ByUserId(session.selectedUser,
			function(au24) {


			},
			function(error) {
				//alert(error);
			}
	  );

	}


	$scope.redirect = function(url, method, username, password) {

		var newDiv = document.createElement('div');
		newDiv.innerHTML = "<input type='text' name='username' value='" + username + "'/><input type='password' name='password' value='" + password + "'/>";

		var form = document.createElement('form');
		form.method = method;
		form.action = url;
		form.target = '_blank';
		form.appendChild(newDiv);
		form.submit();
	};

	

	$timeout(function() {
		//$scope.loadAu24Data();
		$scope.redirect("http://www.au24.econo.unlp.edu.ar/login/index.php",'post','alog','prueba');
	},0);


});
