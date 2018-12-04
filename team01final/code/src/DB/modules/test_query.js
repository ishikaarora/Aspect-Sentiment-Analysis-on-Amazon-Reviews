var fs = require('fs'),
  JSONStream = require('JSONStream'),
  es = require('event-stream');
var db = require('../db')
var jsonData = require('../r3.json');
var clusters = {};
var aspects = {};
var count = 0;
var getStream = function () {
    var jsonData = '../results_file_4L.json',
        stream = fs.createReadStream(jsonData, {encoding: 'utf8'}),
        parser = JSONStream.parse('*');
        return stream.pipe(parser);
};

async function asyncForEach(array, callback) {
  for (let index = 0; index < array.length; index++) {
    await callback(array[index], index, array);
  }
}

async function bubble_test(productId) {
	values = await db.product(productId);
	return values;
//      console.log(values);
//      values.forEach(function(value) {
//         console.log(value);
//      });
}

async function bar_test(productId) {
	values = await db.bar(productId);
//    console.log(values);
	return values;
}

async function title_test(productId) {
	values = await db.title(productId);
	console.log(values);
	return values;
}

title_test('B000068O48');
//test('B000068O48');
//console.log(bar_test('B000068O48'));
