app.controller("DashboardCtrl", function($location, $state, $rootScope, $scope, $localStorage, Upload, $timeout, Restangular, Facebook, MainFactory) {

    $rootScope.activateEnhancements = false;
    $rootScope.hideOtherView = true;
    $rootScope.showSpinnner = false;
    $rootScope.showThumbnail = false;
    $scope.username = $localStorage.currentUser;
    $scope.user_id = $localStorage.userid;

    $('[data-toggle="tooltip"]').tooltip()
    
    var url = $location.host(),
        protocol = $location.protocol(),
        port = $location.port();

    url = protocol + '://' + url + ':' + port + '/';

    // populate images in the gallery
    Restangular.all('api/photos/').getList().then(function(response) {
        $scope.userImages = response;
    });

    // Update the image in the database
    $scope.saveImage = function(image, imageID) {

        if (image !== "static/img/media_white.png") {
            if (image.indexOf(url) === -1) {
                image = url + image;
            }
            var data = {
                effect: image,
                photo_id: imageID
            };
            MainFactory.ImageEffect
                .saveImageEffct(data, function(response) {
                    $scope.resetEffects()
                });
        }
    };


    $scope.deleteImage = function(imageID) {
        $rootScope.showSpinnner = true;
        MainFactory.ModifyImage
            .DeleteImage({ id: imageID }, function(response) {
                $rootScope.showSpinnner = false;
                $rootScope.activateEnhancements = false;
                $rootScope.hideOtherView = true;
                $scope.$emit('updateData');
            })
    };

    // when you click on an image in the gallery
    $scope.setImageToEdit = function(imageUrl, imageId) {
        $rootScope.originalImage = imageUrl;
        $rootScope.displayImage = $rootScope.originalImage;
        $rootScope.imageToEditUrl = $rootScope.originalImage;
        $rootScope.imageToEditId = imageId;
        $rootScope.showThumbnail = true;
        $rootScope.activateEnhancements = false;
        $rootScope.hideOtherView = true;
    };

    //when you click on the displayed image 
    $scope.clickToEdit = function(imageUrl) {
        $rootScope.originalImage = imageUrl;
        $rootScope.displayImage = $rootScope.originalImage;
        $rootScope.activateEnhancements = false;
        $rootScope.hideOtherView = true;
    };

    // reset all effects applied to the image
    $scope.resetEffects = function() {
        if ($rootScope.displayImage !== "static/img/media_white.png") {
            MainFactory.Reset
                .resetEffects()
                .$promise
                .then(function(response) {
                    $rootScope.displayImage = $rootScope.originalImage;
                    $scope.selectedColor = 0;
                    $scope.selectedContrast = 0;
                    $scope.selectedBrightness = 0;
                    $scope.selectedSharpness = 0;
                    $rootScope.activateEnhancements = false;
                    $rootScope.hideOtherView = true;
                });
        }
    };

    // Show the enhancement controls
    $scope.showEnhancements = function() {
        $rootScope.activateEnhancements = false;
        $rootScope.hideOtherView = true;
    };

    //Apply enhancements on the image when a user sets 
    $scope.applyEnhancements = function(image, color, contrast, brightness, sharpness) {
        if (image !== "static/img/media_white.png") {
            var data = {
                image: image,
                x: color,
                y: contrast,
                z: brightness,
                w: sharpness
            }
            $rootScope.showSpinnner = true;
            MainFactory.Enhancement
                .getEnhancement(data)
                .$promise
                .then(function(response) {
                    $rootScope.displayImage = response.enhance;
                    $rootScope.showSpinnner = false;
                })
                .catch(function(error) {
                    $rootScope.showSpinnner = false;
                });
        }
    };

    // Show filters that can be applied on an image
    $scope.showFilters = function(image) {

        if (image !== "static/img/media_white.png") {
            $rootScope.showSpinnner = true;
            MainFactory.Filters
                .getAllImageFilters({ "image_url": image })
                .$promise
                .then(function(response) {
                    $rootScope.imageFilter = response
                    $rootScope.hideOtherView = false;
                    $rootScope.activateEnhancements = true;
                    $state.go('dashboard.filters');
                    $rootScope.showSpinnner = false;
                });


        }

    };

    //Apply selected filter on an image
    $scope.applyFilter = function(url) {
        $rootScope.displayImage = url;
    };

    // Rotate the image basing on what a user has clicked
    $scope.rotateImage = function(image, x) {
        if (image !== "static/img/media_white.png") {
            var data = {
                image: image,
                x: x
            }
            $rootScope.showSpinnner = true;
            MainFactory.Rotate
                .rotate(data)
                .$promise
                .then(function(response) {
                    $rootScope.displayImage = response.degree;
                    $rootScope.showSpinnner = false;

                })
                .catch(function(error) {
                    $rootScope.showSpinnner = false;
                });
        }
    };

    // Show textbox for a userr to input data
    $scope.showTextBox = function() {
        $rootScope.hideOtherView = false;
        $rootScope.activateEnhancements = true;
        $state.go('dashboard.textView');
    };

    // Draw text on an image
    $scope.drawText = function(image, text, position) {
        if (image !== "static/img/media_white.png") {
            var data = {
                image: image,
                text: text,
                position: position
            }
            if (position  && text ) {
                $rootScope.showSpinnner = true;
                MainFactory.Text
                    .DrawText(data)
                    .$promise
                    .then(function(response) {
                        $rootScope.displayImage = response.image_text;
                        $rootScope.showSpinnner = false;
                        $scope.image_text = ''
                    })
                    .catch(function(error) {
                        $rootScope.showSpinnner = false;
                    });
            }
        }
    };

    // Share Button
    $scope.SharePhoto = function(image) {
        if (image !== "static/img/media_white.png") {

            if (image.indexOf(url) === -1) {
                image = url + image;
            }

            FB.ui({
                method: 'feed',
                link: image,
                picture: image,
                caption: 'Share with love',
                message: ''
            });
        }
    };


    $scope.$on('updateData', function() {
        // populate images in the gallery
        Restangular.all('api/photos/').getList().then(function(response) {
            $scope.userImages = response;
        });
    });


    // image upload specific functions
    $scope.imageUrl = $scope.picFile = "static/img/media_white.png";
    $scope.uploadPic = function(file) {
        var fileName = Upload.rename(file, 'IMG_' + Date.now().toString() +
            file.name.substr(file.name.lastIndexOf('.'), file.name.length));

        file.upload = Upload.upload({
            url: 'api/photos/',
            data: {
                image: fileName,
                name: fileName.ngfName
            }
        });

        file.upload.then(function(response) {
            console.log(response)
            MainFactory.IMage.getImage({ name: response.data.name })
                .$promise
                .then(function(successResp) {
                    $rootScope.getImageUploaded = successResp;
                    $rootScope.imageToEditUrl = $rootScope.getImageUploaded.image_url;
                    $rootScope.imageToEditId = $scope.getImageUploaded.id;
                    $rootScope.showThumbnail = true;
                    $rootScope.activateEnhancements = false;
                    $rootScope.hideOtherView = true;
                });

            $scope.$emit('updateData');

            $timeout(function() {
                file.result = response.data;
                $scope.picFile = $scope.imageUrl;
            });

        }, function(response) {
            if (response.status > 0)
                console.log($scope.errorMsg = response.status + ': ' + response.data);
        }, function(evt) {
            // Math.min is to fix IE which reports 200% sometimes
            file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
            $scope.progressStyle = {
                'width': file.progress + '%'
            };
        });
    }

    $rootScope.displayImage = "static/img/media_white.png";
    $rootScope.imageToEditUrl = $rootScope.displayImage;

});
