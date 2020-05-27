# WebHomework

## How to run with docker after cloning

**docker build -t arnoldaz/webhomework .**

**docker run -p 5000:5000 -d arnoldaz/webhomework**

## Usage

### GET

**GET ALL**

`localhost:5000/phones`

**Responses**
- Array of objects on success

**GET BY ID**

`localhost:5000/phones/<id>`

**Responses**
- Object on success
- `404` on failure

### POST

`localhost:5000/phones` + JSON data

Example JSON data:

{
    "brand": "A",
    "model": "B",
    "price": "C"
}

New phone will be created with auto generated ID

**Responses**
- `201` on success
- `404` on failure

### PUT

`localhost:5000/phones/<id>` + JSON data

Will change object leaving same id

**Responses**
- `200` on success
- `404` on failure

### PATCH

`localhost:5000/phones/<id>` + JSON data

Will edit given fields

**Responses**
- `200` on success
- `404` on failure

### DELETE

`localhost:5000/phones/<id>`

**Responses**
- `200` on success
- `404` on failure