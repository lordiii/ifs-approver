'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:NavcontrollerCtrl
 * @description
 * # NavcontrollerCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp').controller('NavCtrl', function ($scope, $location) {
  $scope.isActive = function (route) {
    return route === $location.path();
  };
});
