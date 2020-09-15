angular.module('logs').component('logs', {
        // Note: The URL is relative to our `index.html` file
        templateUrl: 'static/js/app/logs/logs.template.html',
	bindings: {
		mainPage: '='
	},
        controller: ['$scope', 'log', 'scopeWatchService', '$http','helperService', 'pagerService',
            function LogsController($scope, log, scopeWatchService, $http, helperService, pagerService) {
		self = this
		var didSectionListWrapperLoad = false;

		self.sortBy = '-id';
		self.searchField = 'string';
		self.searchTerm = ''

		self.itemsPerPage = 50;
		self.pageType = 'logs';
		helperService.setNumberOfItemsPerPage(self.itemsPerPage);

		self.nextPage = function (currentPage) {
			var input = {
				currentPage: currentPage,
				pageType: self.pageType,
				log: self.log,
				searchTerm: self.searchTerm,
				searchField: self.searchField,
				sortBy: self.sortBy
			};
			self.logLines = pagerService.getNextPage(input);
			self.logLines.$promise.then(function (res) {
				var paginationInfo = {
					pageType: input.pageType,
					pageInfo: res[1]
				};
				scopeWatchService.paginationInit(paginationInfo);
				self.logs = helperService.resourceToArray(res[0]);
				self.logs.forEach(function(log) {
					self.formatLog(log);
				});
			});
		};

		self.formatLog = function (log) {
			if (log.age_seconds < 60) {
				log.age_str = Math.floor(log.age_seconds) + " seconds";
			} else if (log.age_seconds < 60 * 60) {
				log.age_str = Math.floor((log.age_seconds / 60)) + " minutes";
			} else if (log.age_seconds < 60 * 60 * 60) {
				log.age_str = Math.floor((log.age_seconds / (60 * 60))) + " hours";
			} else {
				hours = log.age_seconds / (60 * 60);
				hours = Math.floor(hours % 24);
				days = Math.floor(log.age_seconds / (60 * 60 * 24));
				log.age_str = days + " days " + hours + " hours";
			}
		}

		$scope.$on("logLoaded", function (event, scene) {
			self.log = log;
			self.nextPage(0);
		});

		$scope.$on("paginationChange", function (event, pageInfo) {
			if (pageInfo.pageType == self.pageType){
				self.nextPage(pageInfo.page)
			}
		});

               self.changeNumberOfItemsPerPage = function () {
                    helperService.setNumberOfItemsPerPage(self.itemsPerPage);
                };

            $scope.$on("addLogToList", function (event, log) {
                self.log.push(log)
            });

            $scope.$on("sortOrderChanged", function (event, sortOrder) {
	                if (sortOrder['sectionType'] == 'logs') {
				if (sortOrder['sortBy'] != undefined) {	// TODO: why do we get an 'undefined' here?
					self.log = [];
					self.sortBy = sortOrder['sortBy'];
				}
				if (sortOrder.mainPage == undefined || sortOrder.mainPage == true ) {
					self.nextPage(0);
				}
				didSectionListWrapperLoad = true;
			}
		});

            if (!didSectionListWrapperLoad) {
                scopeWatchService.didSectionListWrapperLoaded('logs')
            }
            }
        ]
    }
);
