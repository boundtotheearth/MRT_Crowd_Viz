function get_crowd_viz() {
  var day_type = 'WEEKDAY'
  if(document.getElementById('weekday_radio_input').checked) {
    day_type = 'WEEKDAY'
  } else if (document.getElementById('weekend_radio_input').checked) {
    day_type = 'WEEKEND'
  }
  const start_station = document.getElementById('start_station_input').value
  const end_station = document.getElementById('end_station_input').value

  console.log(day_type, start_station, end_station)
  axios.get(`https://boundtotheearth.pythonanywhere.com/${day_type}/${start_station}/${end_station}`)
    .then(function (response) {
      console.log(response)
      document.getElementById('heatmap_svg').innerHTML = response.data
    })
    .catch(function (error) {
      // handle error
      console.log(error);
    })
}