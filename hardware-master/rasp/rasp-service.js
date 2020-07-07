var util = require('util');
var bleno = require('../');

var RaspInfoCharacteristic = require('./rasp-info-characteristic');

function RaspService(rasp) {
    bleno.PrimaryService.call(this, {
        uuid: '13333333333333333333333333333337',
        characteristics: [
            new RaspInfoCharacteristic(rasp)
        ]
    });
}

util.inherits(RaspService, bleno.PrimaryService);

module.exports = RaspService;
