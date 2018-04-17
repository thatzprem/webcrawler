var routerApp = window.angular.module('routerApp', ['ui.router']);

routerApp.config(function($stateProvider, $urlRouterProvider) {

        $urlRouterProvider.otherwise('/home');

        $stateProvider
        // HOME STATES AND NESTED VIEWS ========================================
        .state('home', {
                url: '/home',
                controller: 'homeController'
            });
    });

routerApp.controller('homeController', function($scope, $http, $location) {

        window.console.log("In home controller...");
        $scope.activityModels = [];
        $scope.path = [];
        
        $scope.tocrawl = function(url, depth) {

            if (url === '' || typeof(url) === 'undefined') {
                window.alert("No URL provided. Please enter a valid URL");
                return;
            }
            
            if (depth === null || typeof(depth) === 'undefined') {
                depth = 1;
            }

            if (!/^(f|ht)tps?:\/\//i.test(url)) {
                url = "http://" + url;
            }

            // forming the url    
            var data = {
                url: url,
                depth: depth
            };
            var back_url = '/crawl/';

            $http.get(back_url, {
                    params: data,
                    data: JSON
                }).success(function(data, status, headers, config) {
                    $scope.response_data = data;
                    $scope.path.push(url);
                    return;
                })

            .error(function(data, status, headers, config) {
                    window.alert("Error ");
                    return;
                });
        };

    });