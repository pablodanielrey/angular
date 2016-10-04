
app.controller("AccountRequestEditCtrl", function($rootScope, $scope, $timeout, Utils, Account, Session, Notifications) {

	$scope.accountRequests = [];
	$scope.accountRequest = {};

	$scope.initialize = function() {
		$scope.clearForm();
		var s = Session.getCurrentSession();
		if (s.accountRequestSelected == null || s.accountRequestSelected.length < 1) {
			return;
		}
		$scope.accountRequests = s.accountRequestSelected;
		$scope.accountRequest = $scope.accountRequests[0];
	}

	$scope.clearForm = function() {
		$scope.accountRequest = {};
		$scope.accountRequest = [];
	}


	$scope.resendAccountRequest = function() {
		Account.resendAccountRequest($scope.accountRequests,
			function(response) {
			},
			function(error) {
				Notifications.message(error);
			}
		);
	}

	$scope.approveAccountRequest = function() {

		Account.approveAccountsRequest($scope.accountRequests,
			function(response) {
				$rootScope.$broadcast('AccountRequestUpdated');
			},
			function(error) {
				Notifications.message(error);
			}
		);

		$scope.clearForm();
	};

	$scope.removeAccountRequest = function() {
		Account.removeAccountsRequest($scope.accountRequests,
			function(response) {
				$rootScope.$broadcast('AccountRequestUpdated');
			},
			function(error) {
				Notifications.message(error);
			}
		);

		$scope.clearForm();
	};

	$scope.rejectAccountRequest = function(){

		var account = $scope.accountRequests[0];

		Account.rejectAccountRequest(account.id,$scope.description,
			function(response) {
				$rootScope.$broadcast('AccountRequestUpdated');
			},
			function(error) {
				Notifications.message(error);
			}
		);

		$scope.clearForm();
	}


	$scope.$on('AccountRequestSelection', function(event,data) {
		$scope.initialize();
	});

	$timeout(function() {
		$scope.initialize();
	},0);

});
