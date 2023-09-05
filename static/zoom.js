// JavaScript for image zoom
function zoomImage(imageUrl) {
  var zoomPane = document.getElementById("zoom-pane");
  var zoomedImg = document.getElementById("zoomed-img");
  var zoomableImg = document.getElementById("zoomable-image"); // Added this line

  zoomedImg.src = imageUrl;
  zoomableImg.style.display = "none"; // Hide the original image while zoomed

  zoomPane.style.display = "block";
}

function closeZoomPane() {
  var zoomPane = document.getElementById("zoom-pane");
  var zoomableImg = document.getElementById("zoomable-image"); // Added this line

  zoomableImg.style.display = "block"; // Show the original image when zoom pane is closed
  zoomPane.style.display = "none";
}
