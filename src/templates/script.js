console.log("Javascript is successfully loaded");
var slider = document.getElementById("myRange");
var output = document.getElementById("compressPercentage");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function () {
  output.innerHTML = this.value;
};