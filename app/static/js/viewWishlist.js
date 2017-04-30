// Your JavaScript Code here
var app = angular.module('viewWishlist',[]);

app.controller( 'myController', function($scope, $http, $window){
    var submissionlink = '/api/users/' + location.pathname.split('/')[1] + '/wishlist';

	$http.get(submissionlink).then(function(response){
        $scope.Wishlist = response.data["data"]["items"];
    });

    $scope.removeWishlist = function($event, itemid){
		var submissionlink = '/api/users/' + location.pathname.split('/')[1] + '/wishlist/' + itemid;

		var sendWishlist = {
			method: 'DELETE',
			url: submissionlink,
			data: { "itemid": itemid },
			headers: { 'Content-Type': 'application/json'},
		}
		$http(sendWishlist).then(function(response){
				$window.location.href = '/wishlist';			
		});
	}
});