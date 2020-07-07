var util = require('util');
var events = require('events');

var RaspStatus = {
  NORMAL: 0,
  CHECK: 1,
};

function Rasp() {
  events.EventEmitter.call(this);
  this.status = RaspStatus.NORMAL;
}

util.inherits(Rasp, events.EventEmitter);

Rasp.prototype.info = function(temperature) {
  console.log("rasp-info-prototype");
  var time = temperature * 10;
  var self = this;
  console.log('응답 내용 : ');
  // data search await 연구
  setTimeout(function() {
    var result = 100;
    self.emit('ready', result);
  }, time);
};

module.exports.Rasp = Rasp; // prototype 메서드
module.exports.RaspStatus = RaspStatus; // 상태