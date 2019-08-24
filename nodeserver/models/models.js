var mongoose = require('mongoose');

//Define a schema
var Schema = mongoose.Schema;

mongoose.connect('mongodb://localhost/test', {useNewUrlParser: true});

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
    console.log("database has been connected")
});


var users = new Schema({
  a_string: String,
  a_date: Date
});


module.exports = Schema;