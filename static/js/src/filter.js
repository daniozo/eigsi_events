let eventType;
let isPublic;
let byYear;

function getEventType(type) {
    if (eventType !== undefined && eventType === type) {
        eventType = undefined;
    } else {
        eventType = type;
    }
    console.log(eventType);
}

function getAccessibility(eventPublic) {
    if (isPublic !== undefined && isPublic === eventPublic) {
        isPublic = undefined;
    } else {
        isPublic = eventPublic;
    }
    console.log(isPublic);
}

function getYear(year) {
    byYear = year;
    console.log(byYear);
}

function buildParams() {
   const params = new URLSearchParams();
   if (eventType) params.append('eventType', eventType);
   if (isPublic !== undefined) params.append('isPublic', isPublic);
   if (byYear) params.append('year', byYear);

    console.log(params.toString());
    // return params;
}


        // <button onclick="geteventType('conference')">Type : Conférence</button>
        // <button onclick="geteventType('workshop')">Type : Atelier</button>