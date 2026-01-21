// Assuming you have a map initialized
var heatmapData = [];

// Fetch the JSON data
fetch('data/rata_rata_historis/hujan_klimatologi_januari_1991-2020.json')
    .then(response => response.json())
    .then(data => {
        data.forEach(point => {
            heatmapData.push([point.latitude, point.longitude, point.rainfall]); // Adjust according to your JSON structure
        });

        // Create the heatmap layer
        var heat = L.heatLayer(heatmapData, { radius: 25 }).addTo(map);
    })
    .catch(error => console.error('Error fetching the data:', error));
