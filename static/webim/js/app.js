angular.module('myApp', [
    'ngRoute',
    'ng-iscroll',
    'myApp.websocket',
    'myApp.controllers',
    'myApp.services',
    'myApp.directive',
    'myApp.factorys',
    'myApp.filters',
]).config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/', {
        templateUrl: '/static/webim/partials/im.html',
        controller: 'AppIMController'
    });
}]);
