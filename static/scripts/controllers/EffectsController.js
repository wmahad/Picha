app.controller('EffectsController', function($scope, $stateParams, MainFactory) {
    var data = {
        id: $stateParams.id
    }
    
    MainFactory.ModifyImage
    .getImageEffects(data, function (response) {
    	console.log(response)
        $scope.showOriginalImage = response.image;
        $scope.displayImageEffect = $scope.showOriginalImage;
        console.log($scope.showOriginalImage)
        MainFactory.ImageEffect
        .getImageEffcts(data, function (response) {
            $scope.EffectImages = response;
        });
    });


});


