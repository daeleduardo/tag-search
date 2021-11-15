class Maps {

    tileServers = {};

    constructor() {
        this.tileServers = {
            OPENSTREETMAP: 1,
            MAPBOX: 2
        }
    }

    createMap = (param) => {
        if ((typeof param.divId !== "string")
            || (typeof param.lat !== "number")
            || (typeof param.lng !== "number")
            || (typeof param.zoom !== "number")
            || (typeof param.tileServer !== "number")
        ) {
            console.error(`Some parameter are invalid to create the map.`);
            return;
        }

        const map = L.map(param.divId, {
            center: [param.lat, param.lng],
            zoom: param.zoom
        });

        setTimeout(() => {
            map.invalidateSize(); 
        }, 500);

        if (param.tileServer == this.tileServers.MAPBOX) {
            if (param.mapKey === null || (typeof param.mapKey) === 'undefined') {
                console.error(`mapKey not found`);
                return;
            }

            L.tileLayer(`https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=${param.mapKey}`, {
                maxZoom: 18,
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                id: 'mapbox/streets-v11',
                tileSize: 512,
                zoomOffset: -1
            }).addTo(map);

        } else {

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 18,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                tileSize: 512,
                zoomOffset: -1
            }).addTo(map);
        }

        return map;

    }

    removeMarkers = (markers) => {
        if (!Array.isArray(markers)) {
            console.error(`Not possible to remove Markers expected Array, ${typeof markers} given`);
            return;
        }
        markers.forEach(marker => {
            map.removeLayer(marker);
        });
    }

    activeDebug = (map) => {
        const popup = L.popup();

        function onMapClick(e) {
            popup
                .setLatLng(e.latlng)
                .setContent(e.latlng.toString())
                .openOn(map);
        }

        map.on('click', onMapClick);
    }


}