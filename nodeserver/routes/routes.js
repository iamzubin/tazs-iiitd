const bodyParser = require('body-parser');

var controller = require("../controller/controller.js");
var transferERC20 = require("../controller/transferERC20.js")
var appRouter = function (app) {

    app.get("/", function (req, res) {
        t = controller.initContract()
        res.status(200).send({ message: t });
  });

  app.post("/signup", function(req,res){
      console.log(req.body.name)
      res.status(200).send({message: 'Hello Darkness my old friend'})
  });
  app.post("/transaction", function(req,res){
    console.log("user exiting:" + req.body.username + " transaction worth " + req.body.cost +" ETH ")
    res.status(200).send({message: "user exiting:" + req.body.username + " transaction worth " + req.body.cost +" ETH "})
    
  });
  app.post("/checkBalance", function(req,res){
    console.log("user exiting:" + req.body.username + " transection worth " + req.body.cost +" ETH ")
    transferERC20.balance()
    res.status(200).send({message: "balance"})
    
  });

}

module.exports = appRouter;