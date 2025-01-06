import json
import unittest
import datetime

# Load the data files
with open("./data-1.json", "r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json", "r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json", "r") as f:
    jsonExpectedResult = json.load(f)

# Helper function to convert from ISO format to milliseconds
def convert_to_milliseconds(timestamp_iso):
    # If it's already an integer (milliseconds), just return it
    if isinstance(timestamp_iso, int):
        return timestamp_iso
    # Otherwise, assume it's in ISO format and convert it
    dt = datetime.datetime.fromisoformat(timestamp_iso.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1000)

def convertFromFormat1(jsonObject):
    # Convert the timestamp from ISO format to milliseconds
    jsonObject["timestamp"] = convert_to_milliseconds(jsonObject["timestamp"])

    # Split the location string into separate fields
    location_parts = jsonObject["location"].split("/")
    jsonObject["location"] = {
        "country": location_parts[0],
        "city": location_parts[1],
        "area": location_parts[2],
        "factory": location_parts[3],
        "section": location_parts[4],
    }

    # Add operationStatus and temp to the result
    jsonObject["data"] = {
        "status": jsonObject.get("operationStatus"),
        "temperature": jsonObject.get("temp")
    }

    # Return the result with deviceID and deviceType fields unchanged
    jsonObject["deviceID"] = jsonObject.pop("deviceID", None)
    jsonObject["deviceType"] = jsonObject.pop("deviceType", None)

    # Clean up and return the result
    jsonObject.pop("operationStatus", None)
    jsonObject.pop("temp", None)
    return jsonObject

def convertFromFormat2(jsonObject):
    # Convert the timestamp from ISO format to milliseconds
    jsonObject["timestamp"] = convert_to_milliseconds(jsonObject["timestamp"])

    # Flatten the device object into deviceID and deviceType
    jsonObject["deviceID"] = jsonObject["device"]["id"]
    jsonObject["deviceType"] = jsonObject["device"]["type"]

    # Combine the location fields into the location object
    jsonObject["location"] = {
        "country": jsonObject.get("country"),
        "city": jsonObject.get("city"),
        "area": jsonObject.get("area"),
        "factory": jsonObject.get("factory"),
        "section": jsonObject.get("section"),
    }

    # Add the data field with status and temperature
    jsonObject["data"] = jsonObject.get("data")

    # Clean up and return the result
    jsonObject.pop("device", None)
    jsonObject.pop("country", None)
    jsonObject.pop("city", None)
    jsonObject.pop("area", None)
    jsonObject.pop("factory", None)
    jsonObject.pop("section", None)
    return jsonObject

def main(jsonObject):
    result = {}

    if jsonObject.get('device') is None:
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result

class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()
