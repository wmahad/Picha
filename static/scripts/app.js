var app = angular.module('PichaApp', ['restangular', 'ngResource', 'ui.router', 'ngStorage', 'ngFileUpload']);

app.config(function($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {
    $stateProvider

    //States for auth
    .state('main_page', {
        url: '/',
        controller: 'FacebookController',
        templateUrl: '/static/templates/home_page.html',
        data: {
            requireLogin: false
        }
    })

    // .state('imageEffects', {
    //     url: '/dashboard/:id',
    //     controller: 'EffectsController',
    //     templateUrl: '/static/templates/effects.html',
    //     data: {
    //         requireLogin: true
    //     }
    // })

    //dashboard state definition
    .state('dashboard', {
        url: '/dashboard',        
        views: {

            // the main template will be placed here (relatively named)
            '': {
                templateUrl: '/static/templates/dashboard.html',
                controller: 'DashboardCtrl',
            },

            // the child views will be defined here (absolutely named)
            'navBarView@dashboard': {
                templateUrl: '/static/templates/navView.html',
                controller: 'DashboardCtrl',
            }
        },
        data: {
            requireLogin: true
        }
    })

    //logout state definition
    .state('logout', {
        url: '/logout',
        controller: function($state, $localStorage, Restangular) {
            Restangular.one('api/logout/')
                .get()
                .then(function(response) {
                    $localStorage.$reset();
                    $state.go('main_page');
                });
        },
        data: {
            requireLogin: true
        }
    })

    //Dashboard view
    .state('dashboard.textView', {
        templateUrl: '/static/templates/textBox.html'
    })

    //filters view
    .state('dashboard.filters', {
        templateUrl: '/static/templates/imageFilters.html'
    })

    // nested list with just some random string data
    .state('dashboard.enhancements', {
        templateUrl: '/static/templates/imageEnhancements.html'
    })


    $urlRouterProvider.otherwise('/');

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    // $httpProvider.interceptors.push('httpRequestInterceptor');

    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
});


app.run(function($rootScope, $state, $localStorage) {

    $rootScope.$on('$stateChangeStart', function(event, toState, toParams) {
        var requireLogin = toState.data.requireLogin;

        if (requireLogin && typeof $localStorage.currentUser === 'undefined') {
            event.preventDefault();
            $state.go('main_page');
        }

        if (!requireLogin && typeof $localStorage.currentUser !== 'undefined') {
            event.preventDefault();
            $state.go('dashboard');
        }

    });

});
