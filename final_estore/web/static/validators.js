function validateTimes(startTime, endTime) {
    const timestampStart = Date.parse(startTime);
    const timestampEnd = Date.parse(endTime);

    // Check if dates are valid
    if (isNaN(timestampStart) == true || isNaN(timestampEnd) == true) {
        return false;
    } else {
        // Check if start date is after end date
        if (timestampStart > timestampEnd) {
            return false;
        }
    }
    return true;
}

function validateDate(date) {
    const timestamp = Date.parse(date);
    return !isNaN(timestamp);
}

function validateTemperature(temperature) {
    return !isNaN(temperature);
}

function validateNric(nric) {
    return nric.length == 4;
}