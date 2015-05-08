var app = angular.module('mainApp');

app.controller('UserAssistanceManagementCtrl', ["$scope", "$rootScope", "$timeout", "$window", "Session", "Assistance", "Profiles", "Notifications", "Utils", function($scope, $rootScope, $timeout, $window, Session, Assistance, Profiles, Notifications, Utils) {

	$scope.model = {
		justification102Selected: false,
	};

	
  $scope.clearSelections = function() {
		$scope.model.justification102Selected = false;
	};


	/**
	 * cargar datos de la session
	 */
	$scope.initialize = function(){
		$scope.clearSelections();


		$scope.model.session = Session.getCurrentSession();
		if ((!$scope.model.session) || (!$scope.model.session.user_id)) {
			alert("Error: Session no definida");
			$window.location.href = "/#/logout";
        } else {
			Profiles.checkAccess(Session.getSessionId(),'ADMIN-ASSISTANCE,USER-ASSISTANCE',
				function(ok) {
					if (ok != 'granted') {
						$window.location.href = "/#/logout";
					}
				},
				function (error) {
					Notifications.message(error);
				}
			);
		}
	};


	$scope.$on('JustificationsRequestsUpdatedEvent', function(event, data) {
		if ($scope.model.session.user_id == data.user_id) {
			$scope.loadRequestedLicences();
		}
	});

	$scope.$on('JustificationStatusChangedEvent', function(event, data) {
		for (var i = 0; i < $scope.model.requestedLicences.length; i++) {
			if ($scope.model.requestedLicences[i].id == data.request_id) {
				$scope.loadRequestedLicences();
				break;
			}
		}
	});






    $timeout(function() {
        $scope.initialize();
    }, 0);

}]);
