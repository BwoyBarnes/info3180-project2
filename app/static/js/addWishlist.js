// Your JavaScript Code here
var app = angular.module('thumbnail',[]);



app.controller( 'myController', function($scope, $http, $window){
	
	$scope.link = "";
    $scope.title = "";
	$scope.description = "";
	$scope.imgLink = "";
	$scope.prevImage = "";

	$scope.loadImages = function($event) {
		var getImages = {
			method: 'POST',
			url: '/api/thumbnails',
			data: JSON.stringify({ 'url': $scope.link }),
			headers: { 'Content-Type': 'application/json'},
		}
		$http(getImages).then(function(response){
			$scope.images = response.data["thumbnails"];
			$scope.$apply();
		});
	}

	$scope.selectedImage = function($event) {
		$('.selectedImage').not(this).removeClass('selectedImage');
		$(event.currentTarget).addClass( "selectedImage" )
		$scope.imgLink = $(event.currentTarget).closest('img').context.children["0"].currentSrc;
  	};

	$scope.submitWishlist = function($event){
		var submissionlink = '/api/users/' + location.pathname.split('/')[1] + '/wishlist'

		var sendWishlist = {
			method: 'POST',
			url: submissionlink,
			data: { "title": $scope.title,
  					"description": $scope.description,
  					'url': $scope.link,
  					"thumbnail_url": $scope.imgLink
			},
			headers: { 'Content-Type': 'application/json'},
		}
		$http(sendWishlist).then(function(response){
				$window.location.href = '/wishlist';			
		});
	}
	
});