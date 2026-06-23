// Mapa (Leaflet + OpenStreetMap) para marcar a localização do evento.

(function () {
    "use strict";

    var el = document.getElementById("mapa-vaga");
    if (!el || typeof L === "undefined") return;

    var latInput = document.getElementById("id_latitude");
    var lngInput = document.getElementById("id_longitude");

    var temCoord = latInput && latInput.value && lngInput && lngInput.value;
    var latIni = temCoord ? parseFloat(latInput.value) : -14.235;   // centro do Brasil
    var lngIni = temCoord ? parseFloat(lngInput.value) : -51.925;
    var zoomIni = temCoord ? 15 : 4;

    var map = L.map("mapa-vaga").setView([latIni, lngIni], zoomIni);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "© OpenStreetMap"
    }).addTo(map);

    var marker = temCoord ? L.marker([latIni, lngIni]).addTo(map) : null;

    function setMarker(lat, lng) {
        if (marker) {
            marker.setLatLng([lat, lng]);
        } else {
            marker = L.marker([lat, lng]).addTo(map);
        }
        latInput.value = lat.toFixed(6);
        lngInput.value = lng.toFixed(6);
    }

    map.on("click", function (e) {
        setMarker(e.latlng.lat, e.latlng.lng);
    });

    var btn = document.getElementById("buscar-endereco");
    var endInput = document.getElementById("id_endereco");

    if (btn && endInput) {
        btn.addEventListener("click", function () {
            var q = endInput.value.trim();
            if (!q) {
                alert("Digite o endereço antes de buscar.");
                return;
            }
            var icon = btn.querySelector("i");
            btn.disabled = true;
            if (icon) { icon.className = "fa-solid fa-spinner fa-spin"; }

            fetch("https://nominatim.openstreetmap.org/search?format=json&limit=1&q=" + encodeURIComponent(q), {
                headers: { "Accept": "application/json" }
            })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (data && data.length) {
                    var lat = parseFloat(data[0].lat);
                    var lng = parseFloat(data[0].lon);
                    map.setView([lat, lng], 16);
                    setMarker(lat, lng);
                } else {
                    alert("Endereço não encontrado. Marque o local clicando no mapa.");
                }
            })
            .catch(function () {
                alert("Não foi possível buscar o endereço agora. Marque clicando no mapa.");
            })
            .finally(function () {
                btn.disabled = false;
                if (icon) { icon.className = "fa-solid fa-magnifying-glass"; }
            });
        });
    }

    setTimeout(function () { map.invalidateSize(); }, 200);
})();
