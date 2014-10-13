'use strict';

/**
 * @ngdoc service
 * @name frontendApp.Imageservice
 * @description
 * # Imageservice
 * Service in the frontendApp.
 */
angular.module('frontendApp').service('Imageservice', function Imageservice($log, $q, $http, Config, $timeout) {

  // private
  var STATUS = {
    APPROVED: 3,
    REJECTED: 4
  };


  function fixDate(data) {
    data.forEach(function (item) {
      item.date = item.date * 1000;
    });
    return data;
  }

  function imageRequest(status, imageId) {
    return $http.put(Config.baseUrl + '/images/' + imageId, {
      status: status
    }).then(
      function ok(response) {
        if (response.data.status !== 'ok') {
          return $q.reject('Request error: ' + response.data.status || 'unknown');
        }
      },
      function error(response) {
        $log.error('error from server', response);
        return $q.reject('server error, status: ' + response.status || 'unknown');
      }
    );
  }

  // public

  this.STATUS = {
    OK: 1,
    NO_IMAGE: 2,
    APPROVED: 3,
    REJECTED: 4
  };

  this.FILTER = {
    ALL: '',
    MISSING: 'missing',
    HISTORY: 'processed'
  };

  /**
   *
   * @param {string} [filter] - use one of FILTER
   * @returns {*}
   */
  this.getImages = function (filter) {
    var config = {
      url: Config.baseUrl + '/images/',
      method: 'GET',
      params: {
        filter: filter || ''
      },
      withCredentials: true
    };
    return $http(config).then(
      function ok(response) {
        var respData = response.data;
        if (respData.status !== 'ok') {
          return $q.reject('Non ok status: ' + respData.status);
        }
        return fixDate(respData.data);
      }, function error(response) {
        $log.error('error from server', response);
        return $q.reject('server error, status: ' + response.status || 'unknown');
      }
    );
  };

  this.approveImage = function (imageId) {
    return imageRequest(STATUS.APPROVED, imageId);
  };

  this.rejectImage = function (imageId) {
    return imageRequest(STATUS.REJECTED, imageId);
  };

});
