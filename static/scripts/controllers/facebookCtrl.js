app.controller("FacebookController", ['$scope', '$rootScope', '$state', '$localStorage', 'Restangular', 'Facebook',
    function ($scope, $rootScope, $state, $localStorage, Restangular, Facebook) {
        $scope.username = $localStorage.currentUser;
        $scope.login_fb = function() {
            Facebook.login()
            .then(function(fb_response) {
                //we come here only if JS sdk login was successful so lets 
                //make a request to our new view. I use Restangular, one can
                //use regular http request as well.
                var reqObj = {
                    "access_token": fb_response.authResponse.accessToken,
                    "backend": "facebook"
                };
                var u_b = Restangular.all('api/register/');
                u_b.post(reqObj)
                .then(function(response) {
                    $localStorage.currentUser = response.user;
                    $localStorage.userid = fb_response.authResponse.userID;
                    $localStorage.token = reqObj.access_token;
                    $scope.username = $localStorage.currentUser;
                    $state.go('dashboard');
                }, function(response) { /*error*/
                    $scope.login = {}
                    $scope.login.error = 'Sorry !! could not login';
                    //deal with error here. 
                });
            });
        }

    }
]);

