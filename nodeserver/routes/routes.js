
var controller = require("../controller/controller.js");

var appRouter = function (app) {

    app.get("/", function (req, res) {
        t = controller.initContract()
        res.status(200).send({ message: t });
  });

  app.get("/hello", function(req,res){
      res.status(200).send({message: 'Hello Darkness my old friend'})
  });

}

module.exports = appRouter;