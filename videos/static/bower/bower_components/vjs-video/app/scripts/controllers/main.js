/*global angular, $ */
/**
 * @ngdoc function
 * @name vjsVideoApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the vjsVideoApp
 */
angular.module('vjsVideoApp').controller('MainCtrl', [
    '$scope',
    function(scope) {
        'use strict';

        var mediaObj = {
                sources: [
                    {
                        src:
                            '//s3.amazonaws.com/lonnygomes.com/assets/8269691015_hd.mp4',
                        type: 'video/mp4'
                    },
                    {
                        src: 'http://vjs.zencdn.net/v/oceans.webm',
                        type: 'video/webm'
                    }
                ],
                tracks: [
                    {
                        kind: 'subtitles',
                        label: 'English subtitles',
                        src: 'assets/subtitles.vtt',
                        srclang: 'en',
                        default: true
                    }
                ],
                poster:
                    '//s3.amazonaws.com/lonnygomes.com/assets/8269691015_hd_poster.jpg'
            },
            mediaAltObj = {
                sources: [
                    {
                        src:
                            'http://html5videoformatconverter.com/data/images/happyfit2.mp4',
                        type: 'video/mp4'
                    },
                    {
                        src:
                            'http://html5videoformatconverter.com/data/images/happyfit2.webm',
                        type: 'video/webm'
                    }
                ],
                tracks: [],
                poster:
                    'http://html5videoformatconverter.com/data/images/screen.jpg'
            },
            audioMediaObj = {
                sources: [
                    {
                        src:
                            'http://s3.amazonaws.com/lonnygomes.com/assets/DJ-MassDefect-Fado.mp3',
                        type: 'audio/mp3'
                    }
                ],
                tracks: [
                    {
                        kind: 'subtitles',
                        label: 'English subtitles',
                        src: 'assets/audio_subtitles.vtt',
                        srclang: 'en',
                        default: true
                    }
                ],
                poster:
                    'http://s3.amazonaws.com/lonnygomes.com/assets/mass_defect_poster.jpg'
            },
            isToggled = false;

        this.awesomeThings = ['HTML5 Boilerplate', 'AngularJS', 'Karma'];

        scope.toggleMedia = function() {
            isToggled = !isToggled;
            scope.mediaToggle = isToggled ? mediaObj : mediaAltObj;
        };

        scope.toggleAudio = function() {
            scope.mediaToggle = audioMediaObj;
        };

        scope.options = {
            loop: true
        };

        scope.isSmallScreen = function() {
            return $(window).width() < 650 ? true : false;
        };

        scope.media = mediaObj;

        scope.mediaToggle = mediaAltObj;

        scope.$on('vjsVideoReady', function(e, data) {
            //data contains `id` and `vid`
        });
    }
]);
