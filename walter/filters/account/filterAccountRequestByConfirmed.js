
var app = angular.module('mainApp');

app.filter('filterAccountRequestByConfirmed', function () {
	return function (accountRequests, filterconfirmed) {

		if(filterconfirmed == undefined){
			filterconfirmed = [];
			filterconfirmed.confirmed = true;
			filterconfirmed.unconfirmed = false;
		}

		var items = {
            filterconfirmed: filterconfirmed,
            out: []
        };

		 angular.forEach(accountRequests, function (accountRequest, key) {
            if (accountRequest.request.confirmed){
            	if(this.filterconfirmed.confirmed) {
					this.out.push(accountRequest);
            	}
            } else {
            	if(this.filterconfirmed.unconfirmed) {
					this.out.push(accountRequest);
            	}
            }

        }, items);
        return items.out;
	}
});
