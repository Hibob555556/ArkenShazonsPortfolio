let solarChart = null;

Module.onRuntimeInitialized = () => {
  //#region wasm functions
  // import get_solar_elevation function from main.c
  const getSolarElevation = Module.cwrap("get_solar_elevation", "number", [
    "number",
    "number",
    "number",
    "number",
    "number",
    "number",
    "number",
    "number",
    "number",
    "number",
  ]);
  //#endregion

  //#region Daily Data
  document.getElementById("calc-elevation").onclick = () => {
    // get current time data
    const time = getRealTime();

    // get geo data
    const geoData = getGeoData();

    // set geo data
    const latitude = geoData[0];
    const longitude = geoData[1];
    const alt = geoData[2];

    // set time data
    const year = time[0];
    const month = time[1];
    const day = time[2];
    const sec = time[5];

    // set time zone data
    const tz_off = time[6];

    const dataPoints = [];
    const labels = [];

    for (let hour = 0; hour < 24; hour++) {
      for (let min = 0; min < 60; min += 10) {
        const elevation = getSolarElevation(
          latitude,
          longitude,
          year,
          month,
          day,
          hour,
          min,
          sec,
          alt,
          tz_off
        );
        dataPoints.push(elevation);
        labels.push(
          `${hour.toString().padStart(2, "0")}:${min
            .toString()
            .padStart(2, "0")}`
        );
      }
    }

    popChart(dataPoints, labels);
  };
  //#endregion

  //#region Current Elevation
  document.getElementById("calc-curr-elevation").onclick = () => {
    // get geo data
    const geoData = getGeoData();

    // set geo data
    const latitude = geoData[0];
    const longitude = geoData[1];
    const altitude = geoData[2];

    // get the time
    const time = getRealTime();

    // get the current elevation
    const elevation = getSolarElevation(
      latitude,
      longitude,
      time[0],
      time[1],
      time[2],
      time[3],
      time[4],
      time[5],
      altitude,
      time[6]
    );

    // display the result
    setResult(`Solar Elevation: ${elevation}`);
  };

  document.getElementById("show-sky").onclick = () => {
    // get geo data
    const geoData = getGeoData();

    // set geo data
    const latitude = geoData[0];
    const longitude = geoData[1];
    const altitude = geoData[2];

    // get the time
    const time = getRealTime();

    // get the current elevation
    const elevation = getSolarElevation(
      latitude,
      longitude,
      time[0],
      time[1],
      time[2],
      time[3],
      time[4],
      time[5],
      altitude,
      time[6]
    );

    // display upper left in morning and upper right at night
    if (elevation < 0 && time[3] < 12) displayMoon();
    else if (elevation < 0 && time[3] > 12) displayMoon();
    else if (elevation > 0) displaySun(elevation);
  };
  //#endregion
};

//#region display functions
function setResult(res) {
  // get the result container
  const resContainer = document.getElementById("result");

  // set the text of the container to the result
  resContainer.textContent = res;
}

function popChart(dataPoints, labels) {
  // get the 2d context of the canvas
  const ctx = document.getElementById("solarChart").getContext("2d");

  // If chart exists, update it
  if (solarChart) {
    // set the chart labels (x axis)
    solarChart.data.labels = labels;

    // set the data for the chart (y axis)
    solarChart.data.datasets[0].data = dataPoints;

    // update the chart
    solarChart.update();
  } else {
    // Otherwise, create the chart
    solarChart = new Chart(ctx, {
      type: "line", // chart type
      data: {
        labels: labels, // set the labels (x axis)
        datasets: [
          {
            label: "Solar Elevation (°)",
            data: dataPoints, // set the data to display on the chart
            borderColor: "orange",
            backgroundColor: "rgba(255, 165, 0, 0.2)",
            tension: 0.3,
            fill: true,
            pointRadius: 2,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          // display the legend
          legend: { display: true },
          tooltip: { enabled: true },
        },
        scales: {
          x: {
            // create x axis title and set it to be displayed
            title: { display: true, text: "Time of Day" },
          },
          y: {
            // create y axis title and set it to be displayed
            title: { display: true, text: "Elevation (degrees)" },
            min: -20, // set y axis min/max
            max: 90,
          },
        },
      },
    });
  }
}
//#endregion

//#region time functions
/**
 * @description Returns the time info (year, month, day, hour, minute, second, tz offset)
 * @returns {Array<Number>}
 */
function getRealTime() {
  // create a date object
  const date = new Date();

  // get the date information
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hour = date.getHours();
  const minute = date.getMinutes();
  const second = date.getSeconds();

  // get timezone offset information
  const tz_offset = date.getTimezoneOffset() / 60;

  // create the real time array
  let realTime = [year, month, day, hour, minute, second, tz_offset * -1];
  console.log(realTime);

  // return the real time
  return realTime;
}
//#endregion

//#region geo functions
function getGeoData() {
  // get the geoData from the inputs
  const lat = document.getElementById("latitude").value;
  const long = document.getElementById("longitude").value;
  const alt = document.getElementById("altitude").value;

  // create and output the geoData array
  const geoData = [lat, long, alt];
  console.log(geoData);

  // return the geo data specified by the user
  return geoData;
}
//#endregion

//#region page styles
// create images to stor the sun and moon SVGs
const moon = new Image();
const sun = new Image();

const skyDisplay = document.getElementById("sky-display");
const skyCtx = skyDisplay.getContext("2d");

// set image source for moon/sun
moon.src = "./src/moon.svg";
sun.src = "./src/sun.svg";

function displaySun(elevation = 0) {
  skyCtx.clearRect(0, 0, skyDisplay.width, skyDisplay.height);
  drawDaySky();
  skyCtx.drawImage(sun, 0, 0, 100, 100);
}

function displayMoon(elevation = 0) {
  skyCtx.clearRect(0, 0, skyDisplay.width, skyDisplay.height);
  drawNightSky();
  skyCtx.drawImage(moon, 300, 0, 100, 100);
}

function drawNightSky() {
  skyCtx.fillStyle = "black"; // set the background to be black
  skyCtx.fillRect(0, 0, skyDisplay.width, skyDisplay.height);

  const starCount = 200; // number of stars

  for (let i = 0; i < starCount; i++) {
    const x = Math.random() * skyDisplay.width;
    const y = Math.random() * skyDisplay.height;
    const radius = Math.random() * 1.5 + 0.2; // small random size for stars

    skyCtx.beginPath();
    skyCtx.arc(x, y, radius, 0, 2 * Math.PI);
    skyCtx.fillStyle = "white";
    skyCtx.fill();
  }
}

function drawDaySky() {
  // Create a vertical gradient (top = light blue, bottom = deeper blue)
  const gradient = skyCtx.createLinearGradient(0, 0, 0, skyDisplay.height);
  gradient.addColorStop(0, "#87CEEB"); // Light sky blue (top)
  gradient.addColorStop(1, "#4682B4"); // Steel blue (bottom)

  // Fill the canvas with the gradient
  skyCtx.fillStyle = gradient;
  skyCtx.fillRect(0, 0, skyDisplay.width, skyDisplay.height);

  // draw clouds so its not boring...
  drawCloud(100, 100, .5);
  drawCloud(300, 150, 0.9);
  drawCloud(500, 80, .75);
  drawCloud(650, 130, .6);
}

// Function to draw a simple puffy cloud
function drawCloud(x, y, scale = 1) {
  skyCtx.beginPath();
  skyCtx.arc(x, y, 20 * scale, 0, Math.PI * 2);
  skyCtx.arc(x + 25 * scale, y - 10 * scale, 25 * scale, 0, Math.PI * 2);
  skyCtx.arc(x + 55 * scale, y, 20 * scale, 0, Math.PI * 2);
  skyCtx.arc(x + 30 * scale, y + 10 * scale, 30 * scale, 0, Math.PI * 2);
  skyCtx.fillStyle = "white";
  skyCtx.fill();
}
//#endregion
