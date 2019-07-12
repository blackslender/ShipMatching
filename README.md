---
topic: Vessel-Cargo matching API application
languages:
  - python
products:
  - Azure App Service
  - Azure Web Apps
---

# Vessel-Cargo matching API application for Azure App Service (Python - Linux)

This is the RESTful application for the Vessel-Cargo matching problem. No data will be stored, only the matching result will be calculated and responsed

## Request

### Request URL

http://localhost:5000/cal

### Request format

There is only one GET request allowed. The request data are JSON strings which include:

* "data": 2d-array of input data. The array should be a rectangle array, which mean all rows have the same length. Each row represents a vessel, and each column represents a cargo.

Example:

```json
{
  "data": [
    [1,2,3,4,5],
    [2,3,4,5,6],
    [3,4,5,6,7],
    [4,5,6,7,8]]
}
```

## Response

Responses are JSON strings which include:

* "success": Boolean variable, true if the request was successfully processed
* "error": Occured error if the request was not successfully processed
* "data": Result if the calculation is done
  * "profitability": Total value of the best choice by algorithm
  * "pairs": List of objects, each element represent a tuple with vessel index, cargo index and that pair's value. Indexs start from 1
    * "vessel"
    * "cargo"
    * "value"

Example response with success

```json
{
    "success": true,
    "data": {
        "profitability": 20,
        "pairs": [
            {
                "vessel": 1,
                "cargo": 2,
                "value": 2
            },
            {
                "vessel": 4,
                "cargo": 5,
                "value": 8
            },
            {
                "vessel": 3,
                "cargo": 4,
                "value": 6
            },
            {
                "vessel": 2,
                "cargo": 3,
                "value": 4
            }
        ]
    },
    "error": null
}
```