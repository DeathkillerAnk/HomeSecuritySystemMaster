var express = require("express"),
    app = express(),
    net = require('net'),
    bodyParser = require("body-parser");

    app.set("view engine","ejs");
    app.use(express.static("public"));
    app.use(bodyParser.urlencoded({extended:true}));

app.get("/home",function(req,res){
    res.render("home");
});

app.post("/train",function(req,res){
    console.log(req.body.name);
        var client = new net.Socket();
        client.connect(8005, '127.0.0.1', function() {
        	console.log('Connected');
        	client.write('{"rpc":"startRecording","args":['+req.body.name+']');
        });

        client.on('data', function(data) {
        	console.log('Received: ' + data);
        	client.destroy(); // kill client after server's response
        });

        client.on('close', function() {
        	console.log('Connection closed');
        });
    res.redirect("/home");
});


app.post("/startRecoding",function(req,res){
    // console.log(req.body.name);
        var client = new net.Socket();
        client.connect(8005, '127.0.0.1', function() {
        	console.log('Connected');
        	client.write('{"rpc":"startLearning","args":[]');
        });

        client.on('data', function(data) {
        	console.log('Received: ' + data);
        	client.destroy(); // kill client after server's response
        });

        client.on('close', function() {
        	console.log('Connection closed');
        });
    res.redirect("/home");
});


app.post("/delete",function(req,res){
    // console.log(req.body.name);
        var client = new net.Socket();
        client.connect(8005, '127.0.0.1', function() {
        	console.log('Connected');
        	client.write('{"rpc":"deleteCapturedData","args":[]');
        });

        client.on('data', function(data) {
        	console.log('Received: ' + data);
        	client.destroy(); // kill client after server's response
        });

        client.on('close', function() {
        	console.log('Connection closed');
        });
    res.redirect("/home");
});

app.post("/delete",function(req,res){
    // console.log(req.body.name);
        var client = new net.Socket();
        client.connect(8005, '127.0.0.1', function() {
        	console.log('Connected');
        	client.write('{"rpc":"startSurveillance","args":[]');
        });

        client.on('data', function(data) {
        	console.log('Received: ' + data);
        	client.destroy(); // kill client after server's response
        });

        client.on('close', function() {
        	console.log('Connection closed');
        });
    res.redirect("/home");
});


// var client = new net.Socket();
// client.connect(8005, '127.0.0.1', function() {
// 	console.log('Connected');
// 	client.write('{"rpc":"startRecording","args":["Aniket"]');
// });

// client.on('data', function(data) {
// 	console.log('Received: ' + data);
// 	client.destroy(); // kill client after server's response
// });

// client.on('close', function() {
// 	console.log('Connection closed');
// });


app.listen(3000,() => {
    console.log("started");
});