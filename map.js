// Javascript file to control over the map

var mymap = L.map('mapid').setView([34.2, -118.17], 16);

	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		id: 'mapbox.streets'
	}).addTo(mymap);

	L.marker([34.2, -118.17]).addTo(mymap)
		.bindPopup("<b>Jet Propulsion Lab</b>").openPopup();
	

	var popup = L.popup();

	function onMapClick(e) {
		popup
			.setLatLng(e.latlng)
			.setContent("Latitude: " + e.latlng.lat.toFixed(2) + " Longitude: "+e.latlng.lng.toFixed(2))
			.openOn(mymap);
	}

	function onLocate(lat,lng) {
		var info = "Latitude:"+lat+"  Longitude:"+lng;
		L.marker([lat, lng]).addTo(mymap)
		.bindPopup(info).openPopup();
	}


	mymap.on('click', onMapClick);
