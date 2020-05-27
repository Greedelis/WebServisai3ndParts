from flask import Flask, request, jsonify, abort, Response
import json
import requests 
import xmltodict
app = Flask(__name__)

URL = "http://arnweb:5000/"

parts = [
    {"id" : 0,
     "manufacturer": "AMD",
     "name": "Ryzen 7 3800x",
     "type": "CPU",
     "price": "331.90",
     "phone" : "1"
     },
    {"id": 1,
     "manufacturer": "AMD",
     "name": "Ryzen 5 3600",
     "type": "CPU",
     "price": "181.00",
     "phone" : "2"
     },
    {"id": 2,
     "manufacturer": "ASRock",
     "name": "AB350 PRO4",
     "type": "Motherboard",
     "price": "74.69",
     "phone" : "4"
     }
]

new_id = 3
#GET
#POST - Create/Add
#DELETE
#PUT - Update/Modify

@app.route("/")
def home():
    return "<h1>PC parts list</h1><a href='http://localhost:5000/api/parts'>All parts</a>"



@app.route("/api/parts", methods = ["GET", "POST"])
def api_parts():
    if request.method == "GET":
        if "name" in request.args:
            temp_parts = []
            for part in parts:
                temp_parts.append({"id" : (part.get("id")), "name": part.get("name")})
            return jsonify(temp_parts)
        return jsonify(parts)

    elif request.method == "POST":
        new_data = request.get_json("force=True")
        if "name" in new_data and "manufacturer" in new_data and "type" in new_data and "price" in new_data and "phone" in new_data:
            global new_id
            new_part = {
                "id": new_id,
                "manufacturer": new_data["manufacturer"],
                "name": new_data["name"],
                "type": new_data["type"],
                "price": new_data["price"],
                "phone": new_data["phone"]
            }
            parts.append(new_part)
            new_id+=1
            return Response(response=(json.dumps({"Success":"Part was added"})), status=201, headers={"location": "/api/parts/"+str(new_id-1), "id" : str(new_id-1)}, mimetype="application/json")
        else:
            error_msg = "no "
            if "name" not in new_data:
                error_msg += "name "
            if "manufacturer" not in new_data:
                error_msg += "manufacturer "
            if "type" not in new_data:
                error_msg += "type "
            if "price" not in new_data:
                error_msg += "price "
            if "phone" not in new_data:
                error_msg += "phone "
            error_msg += "have been declared"

            return Response(json.dumps({"Failure" : error_msg}),status=400,mimetype="application/json")
    else:
        abort(404)


@app.route("/api/parts/<int:part_id>", methods = ["GET", "DELETE", "PUT"])
def api_part_id(part_id):
    part = [part for part in parts if part["id"] == part_id]
    if len(part) == 0:
        abort(404)
    
    if request.method == "GET":
        return jsonify(part)

    elif request.method == "DELETE":
        for party in parts:
            if party["id"] == part_id:
                parts.remove(party)
                return Response(json.dumps({"Success" : "Deleted"}),status=204, mimetype="application/json")
    
    elif request.method == "PUT":
        new_data = request.get_json("force=True")
        response = ""
        if "name" in new_data:
            part[0]["name"] = new_data["name"]
            response += "name "
        if "manufacturer" in new_data:
            part[0]["manufacturer"] = new_data["manufacturer"]
            response += "manufacturer "
        if "type" in new_data:
            part[0]["type"] = new_data["type"]
            response += "type "
        if "price" in new_data:
            part[0]["price"] = new_data["price"]
            response += "price "
        if "phone" in new_data:
            part[0]["phone"] = new_data["phone"]
            response += "phone "
        response += "have been changed"
       

        if "name" not in new_data and "manufacturer" not in new_data and "type" not in new_data and "price" not in new_data and "phone" not in new_data:
            return Response(json.dumps({"Failed" : "no "}))

        return Response(json.dumps(part),status=200, mimetype="application/json")

@app.route("/api/phones", methods = ["GET", "POST"])
def api_phones():
    if request.method == "GET":  
        req = requests.get(URL + "phones/")
        return jsonify(req.json())
    elif request.method == "POST":
        new_data = request.get_json("force=True")
        resp = requests.post(URL+"phones", json = (new_data), )
        if str(resp.status_code) == "400" or str(resp.status_code) == "404":
            return Response(json.dumps({"Failure" : resp.text}),status=resp.status_code,mimetype="application/json")
        else:
             return Response(json.dumps({"Success" : resp.text}),status=resp.status_code,mimetype="application/json")

@app.route("/api/parts/<int:part_id>/phone", methods = ["GET"])
def api_phone_info(part_id):
    part = [part for part in parts if part["id"] == part_id]
    if len(part) == 0:
        abort(404)
    
    if request.method == "GET":
        req = requests.get(URL+"phones/"+str(part[0]["phone"]))
        return jsonify(req.json())

@app.route("/api/fullParts", methods = ["GET", "POST"])
def test():
    if request.method == "GET":
        temp_parts = []
        for a in parts:
            b = a.copy()
            try:
                req = requests.get(URL+"phones/"+str(a["phone"]))
                b["phone"] = (req.json())
            except requests.exceptions.RequestException as e:
                print(e)
            temp_parts.append(b)
        return jsonify(temp_parts)
    else:
        new_data = request.get_json("force=True")
        phone_data = new_data["phone"]
        if request.method == "POST":
            try:
                resp = requests.post(URL+"phones", json = (new_data["phone"]))
            except requests.exceptions.RequestException as e:
                return Response(json.dumps({"Failure" : "Cant connect to server"}),status="503",mimetype="application/json")
            if str(resp.status_code) == "400" or str(resp.status_code) == "404":
                return Response(json.dumps({"Failure" : resp.text}),status=resp.status_code,mimetype="application/json")
            else:
                if "name" in new_data and "manufacturer" in new_data and "type" in new_data and "price" in new_data:
                    global new_id
                    new_part = {
                        "id": new_id,
                        "manufacturer": new_data["manufacturer"],
                        "name": new_data["name"],
                        "type": new_data["type"],
                        "price": new_data["price"],
                        "phone": resp.headers["id"]
                    }
                    parts.append(new_part)
                    new_id+=1
                    return Response(response=(json.dumps({"Success":"Part was added"})), status=201, headers={"location": "/api/parts/"+str(new_id-1), "id" : str(new_id-1)}, mimetype="application/json")
                else:
                    error_msg = "no "
                    if "name" not in new_data:
                        error_msg += "name "
                    if "manufacturer" not in new_data:
                        error_msg += "manufacturer "
                    if "type" not in new_data:
                        error_msg += "type "
                    if "price" not in new_data:
                        error_msg += "price "
                    if "phone" not in new_data:
                        error_msg += "phone "
                    error_msg += "have been declared"
                    return Response(json.dumps({"Failure" : error_msg}),status=400,mimetype="application/json")

@app.route("/api/fullParts/<int:part_id>", methods = ["GET", "DELETE", "PUT"])
def fullpats(part_id):

    part = [part for part in parts if part["id"] == part_id]
    if len(part) == 0:
        abort(404)
    
    if request.method == "GET":
        b = part.copy()
        try:
            req = requests.get(URL+"phones/"+(b[0]["phone"]))
            b[0]["phone"] = (req.json())
        except requests.exceptions.RequestException as e:
            print(e)
        return jsonify(b)

    elif request.method == "DELETE":
        for party in parts:
            if party["id"] == part_id:
                parts.remove(party)
                return Response(json.dumps({"Success" : "Deleted"}),status=204, mimetype="application/json")
    
    elif request.method == "PUT":
        new_data = request.get_json("force=True")
        response = ""
        if "name" in new_data:
            part[0]["name"] = new_data["name"]
            response += "name "
        if "manufacturer" in new_data:
            part[0]["manufacturer"] = new_data["manufacturer"]
            response += "manufacturer "
        if "type" in new_data:
            part[0]["type"] = new_data["type"]
            response += "type "
        if "price" in new_data:
            part[0]["price"] = new_data["price"]
            response += "price "
        if "phone" in new_data:
            try:
                requ = requests.put(URL+"phones/"+ str(part[0]["phone"]), json = new_data["phone"])
                response += "phone "
            except requests.exceptions.RequestException as e:
                response += "(phone  could not be changed because of connection error)"
        response += "have been changed"
        if "name" not in new_data and "manufacturer" not in new_data and "type" not in new_data and "price" not in new_data and "phone" not in new_data:
            return Response(json.dumps({"Failed" : "no "}))
        

        return Response(json.dumps(part),status=200, mimetype="application/json")

@app.route("/soap", methods = ["POST"])
def saop():

    xml_data = request.data
    # return(xml_data)
    dic = xmltodict.parse(xml_data)
    json_data = json.dumps(dic)
    items = list(dic.items())

    resp = """<?xml version="1.0" encoding="utf-8"?>\n<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope/" soap:encodingStyle="http://www.w3.org/2003/05/soap-encoding">
    <par:Body>\n"""
    if "par:getAllParts" in json_data:
        resp += "<resp:getAllPartsResponse>\n"
        if "id" in json_data:
            items = list((list((list(items[0][1].items()))[2][1].items()))[0][1].items())
            part_id = items[1][1]

            part = [part for part in parts if str(part["id"]) == part_id]
            if len(part) > 0:
                resp += "<return>"
                resp += "<part>\n" 
                resp += "<id>" + str(part[0]["id"]) + "</id>\n"
                resp += "<name>" + str(part[0]["name"]) + "</name>\n"
                resp += "<manufacturer>" + str(part[0]["manufacturer"]) + "</manufacturer>\n"
                resp += "<type>" + str(part[0]["type"]) + "</type>\n"
                resp += "<price>" + str(part[0]["price"]) + "</price>\n"
                resp += "<phone>" + str(part[0]["phone"]) + "</phone>\n"
                resp += "</part>\n</return>"
                resp += "</resp:getPartResponse>\n</par:Body>\n</soap:Envelope>"
            else:
                resp += "<failure>No part with this id</failure>"
                resp += "</resp:getPartResponse>\n</par:Body>\n</soap:Envelope>"
        else:
            for part in parts:
                resp += "<return>"
                resp += "<part>\n"   
                resp += "<id>" + str(part["id"]) + "</id>\n"
                resp += "<name>" + str(part["name"]) + "</name>\n"
                resp += "<manufacturer>" + str(part["manufacturer"]) + "</manufacturer>\n"
                resp += "<type>" + str(part["type"]) + "</type>\n"
                resp += "<price>" + str(part["price"]) + "</price>\n"
                resp += "<phone>" + str(part["phone"]) + "</phone>\n"
                resp += "</part>\n</return>"
            resp += "</resp:getAllPartsResponse>\n</par:Body>\n</soap:Envelope>"
    elif "par:getPart" in json_data:
        resp += "<resp:getPartResponse>"
        if "id" in json_data:
            items = list((list((list(items[0][1].items()))[2][1].items()))[0][1].items())
            part_id = items[1][1]

            part = [part for part in parts if str(part["id"]) == part_id]
            if len(part) > 0:
                resp += "<id>" + str(part[0]["id"]) + "</id>\n"
                resp += "<name>" + str(part[0]["name"]) + "</name>\n"
                resp += "<manufacturer>" + str(part[0]["manufacturer"]) + "</manufacturer>\n"
                resp += "<type>" + str(part[0]["type"]) + "</type>\n"
                resp += "<price>" + str(part[0]["price"]) + "</price>\n"
                resp += "<phone>" + str(part[0]["phone"]) + "</phone>\n"
                resp += "</resp:getPartResponse>\n</par:Body>\n</soap:Envelope>"
            else:
                resp += "<failure>No part with this id</failure>"
                resp += "</resp:getPartResponse>\n</par:Body>\n</soap:Envelope>"
        else:
            resp += "<failure>No id tag</failure>"
            resp += "</resp:getPartResponse>\n</par:Body>\n</soap:Envelope>"   
    elif "par:addPart" in json_data:
        resp += "<resp:getPartResponse>"
        items = list((list((list(items[0][1].items()))[2][1].items()))[0][1].items())
        json_da = json.dumps(items)
        json_da = json.loads(json_da)
        global new_id
        new_part = {
            "id": new_id,
            "manufacturer": "",
            "name": "",
            "type": "",
            "price": "",
            "phone": ""
        }
        pars = 0;
        for par in json_da:
            if par[0] == "par:name":
                new_part["name"] = par[1]
                pars+=1
            elif par[0] == "par:manufacturer":
                new_part["manufacturer"] = par[1]
                pars+=1
            elif par[0] == "par:type":
                new_part["type"] = par[1]
                pars+=1
            elif par[0] == "par:price":
                new_part["price"] = par[1]
                pars+=1
            elif par[0] == "par:phone":
                new_part["phone"] = par[1]
                pars+=1
        if pars == 5:
            parts.append(new_part)
            new_id+=1   
            resp += "<response>new part was added</response>"
            resp += "</resp:getPartResponse>"
        else:
            resp += "<failure>not enough data tags</failure>"
            resp += "</resp:getPartResponse>"
    elif "par:removePart" in json_data:
        resp += "<resp:removePartResponse>"
        if "id" in json_data:
            items = list((list((list(items[0][1].items()))[2][1].items()))[0][1].items())
            part_id = items[1][1]
            part = [part for part in parts if str(part["id"]) == part_id]
            if len(part) > 0:

                for party in parts:
                    if str(party["id"]) == part_id:
                        parts.remove(party)
                        resp += "<response>part was removed from system</response>"
                        resp += "</resp:removePartResponse>\n</par:Body>\n</soap:Envelope>"

            else:
                resp += "<failure>No part with this id</failure>"
                resp += "</resp:removePartResponse>\n</par:Body>\n</soap:Envelope>"
        else:
            resp += "<respofailurense>No id tag</failure>"
            resp += "</resp:removePartResponse>\n</par:Body>\n</soap:Envelope>"   
    elif "par:updatePart" in json_data:
        resp += "<resp:updatePartResponse>\n<return>"
        if "id" in json_data:
            items = list((list((list(items[0][1].items()))[2][1].items()))[0][1].items())
            part_id = items[1][1]
            json_da = json.dumps(items)
            json_da = json.loads(json_da)
            part = [part for part in parts if str(part["id"]) == part_id]
            if len(part) > 0:
                for par in json_da:
                    if par[0] == "par:name":
                        part[0]["name"] = par[1]
                    elif par[0] == "par:manufacturer":
                        part[0]["manufacturer"] = par[1]
                    elif par[0] == "par:type":
                        part[0]["type"] = par[1]
                    elif par[0] == "par:price":
                        part[0]["price"] = par[1]
                    elif par[0] == "par:phone":
                        part[0]["phone"] = par[1]      
                resp += "<response>Part info was updated</response>"
                resp += "</resp:updatePartResponse>\n</par:Body>\n</soap:Envelope>"
        
            else:
                resp += "<failure>No part with this id</failure>"
                resp += "</resp:updatePartResponse>\n</par:Body>\n</soap:Envelope>"
        else:
            resp += "<failure>No id tag</failure>"
            resp += "</resp:updatePartResponse>\n</par:Body>\n</soap:Envelope>"  
    elif "par:getFullPart" in json_data:
        resp += "<resp:getFullPartResponse>"
        if "id" in json_data:
            items = list((list((list(items[0][1].items()))[2][1].items()))[0][1].items())
            part_id = items[1][1]

            part = [part for part in parts if str(part["id"]) == part_id]
            if len(part) > 0:
                resp += "<id>" + str(part[0]["id"]) + "</id>\n"
                resp += "<name>" + str(part[0]["name"]) + "</name>\n"
                resp += "<manufacturer>" + str(part[0]["manufacturer"]) + "</manufacturer>\n"
                resp += "<type>" + str(part[0]["type"]) + "</type>\n"
                resp += "<price>" + str(part[0]["price"]) + "</price>\n"
                resp += "<phone>"
                try:
                    req = requests.get(URL+"phones/"+(part[0]["phone"]))
                    for par in req:
                        data = tuple(req.json().items())
                        for d in data:
                            resp += "<" + str(d[0]) + ">" + str(d[1]) + "</" + str(d[0]) + ">"
                except requests.exceptions.RequestException as e:
                    print(e)
                    resp += str(part[0]["phone"]) + "</phone>\n"
                resp += "</resp:getFullPartResponse>\n</par:Body>\n</soap:Envelope>"
            else:
                resp += "<failure>No part with this id</failure>"
                resp += "</resp:getPartResponse>\n</par:Body>\n</soap:Envelope>"
        else:
            resp += "<failure>No id tag</failure>"
            resp += "</resp:getPartResponse>\n</par:Body>\n</soap:Envelope>"   
    
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
