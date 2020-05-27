const express = require('express');
const storage = require('./model.js');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const port = 5000;
 
app.route('/phones/')
    .get((req, resp) => {
        resp.send(storage.getAll());            
    })
    .post((req, resp) => {
        const obj = req.body;

        if (obj.brand && obj.model && obj.price) {
            var id = storage.add(obj);
            resp.location('/phones/' + id);
            resp.set("id", id)
            resp.sendStatus(201);
            return;
        }

        resp.status(400).send("Missing or wrong parameters");
    })
    .put((req, resp) => {
        resp.sendStatus(405);
    })
    .patch((req, resp) => {
        resp.sendStatus(405);
    })
    .delete((req, resp) => {
        resp.sendStatus(405);
    });

app.route('/phones/:id')
    .get((req, resp) => {
        const id = req.params.id;
        const obj = storage.get(id);

        if (obj) {
            resp.send(obj);            
            return;
        }

        resp.sendStatus(404);
    })
    .post((req, resp) => {
        resp.sendStatus(405);
    }) 
    .put((req, resp) => {
        const id = req.params.id;
        const obj = req.body;
        const success = storage.replace(id, obj);

        if (success) {
            resp.sendStatus(200);            
            return;
        }

        resp.sendStatus(404);
    })
    .patch((req, resp) => {
        const id = req.params.id;
        const obj = req.body;
        const success = storage.edit(id, obj);

        if (success) {
            resp.sendStatus(200);            
            return;
        }

        resp.sendStatus(404);
    })
    .delete((req, resp) => {
        const id = req.params.id;
        const success = storage.remove(id);

        if (success) {
            resp.sendStatus(200);            
            return;
        }

        resp.sendStatus(404);
    })

    

app.listen(port);
console.log('My server started on port: ' + port);
