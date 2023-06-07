function get_crowd_viz() {
  var day_type = 'WEEKDAY'
  if(document.getElementById('weekday_radio_input').checked) {
    day_type = 'WEEKDAY'
  } else if (document.getElementById('weekend_radio_input').checked) {
    day_type = 'WEEKEND'
  }
  const start_station = document.getElementById('start_station_input').value
  const end_station = document.getElementById('end_station_input').value

  document.getElementById('heatmap_spinner').classList.remove('d-none')

  axios.get(`https://boundtotheearth.pythonanywhere.com/${day_type}/${start_station}/${end_station}`)
    .then(function (response) {
      console.log(response)
      document.getElementById('heatmap_svg').innerHTML = response.data
    })
    .catch(function (error) {
      // handle error
      console.log(error);
    })
    .finally(function () {
      document.getElementById('heatmap_spinner').classList.add('d-none')
    })
}

function build_station_dropdown(list_ele) {
  var stations = ['Punggol LRT (PE7)',
    'Thomson-East Coast Line (TE15)',
    'North East Line (NE11)',
    'Punggol LRT (PW5)',
    'Sengkang LRT (SE1)',
    'Downtown Line (NE4/DT19)',
    'East-West Line (EW4)',
    'East-West Line (EW27)',
    'East-West Line (EW6)',
    'Thomson-East Coast Line (TE1)',
    'Punggol LRT (PE4)',
    'Circle Line Extension (CE1/DT16)',
    'Downtown Line (EW12/DT14)',
    'North-South Line  (NS5)',
    'North-South Line  (NS15)',
    'North East Line (NE10)',
    'Thomson-East Coast Line (TE14/NS22)',
    'North East Line (NS24/NE6/CC1)',
    'Downtown Line (DT31)',
    'Thomson-East Coast Line (TE13)',
    'North-South Line  (TE14/NS22)',
    'Sengkang LRT (SW8)',
    'Bukit Panjang LRT (BP8)',
    'Downtown Line (DT10/TE11)',
    'Punggol LRT (PW4)',
    'North East Line (NE17/PTC)',
    'Sengkang LRT (SW4)',
    'East-West Line (EW3)',
    'North-South Line  (NS4/BP1)',
    'Downtown Line (DT24)',
    'Downtown Line (DT33)',
    'Sengkang LRT (SE3)',
    'Punggol LRT (PE5)',
    'North East Line (NE7/DT12)',
    'Bukit Panjang LRT (BP4)',
    'North-South Line  (NS3)',
    'Bukit Panjang LRT (NS4/BP1)',
    'Circle Line (CC14)',
    'Circle Line (EW8/CC9)',
    'Downtown Line (DT17)',
    'Downtown Line (CC10/DT26)',
    'Bukit Panjang LRT (BP11)',
    'North-South Line  (NS9/TE2)',
    'Downtown Line (DT23)',
    'Circle Line (CC10/DT26)',
    'North-South Line  (EW24/NS1)',
    'Downtown Line (EW2/DT32)',
    'Sengkang LRT (SW2)',
    'North East Line (NE5)',
    'North-South Line  (NS19)',
    'North-South Line  (NS21/DT11)',
    'Changi Airport Branch Line (CG2)',
    'North-South Line  (NS28)',
    'Sengkang LRT (SE4)',
    'Downtown Line (DT30)',
    'North-South Line  (NS23)',
    'East-West Line (EW10)',
    'Circle Line (CC17/TE9)',
    'Downtown Line (DT34)',
    'Circle Line (CC24)',
    'Downtown Line (DT22)',
    'Downtown Line (DT3)',
    'Downtown Line (DT29)',
    'Circle Line (CC23)',
    'East-West Line (EW33)',
    'Downtown Line (DT8)',
    'Downtown Line (DT25)',
    'Punggol LRT (PE2)',
    'Downtown Line (CC4/DT15)',
    'Circle Line (EW21/CC22)',
    'North East Line (NE13)',
    'East-West Line (EW11)',
    'Circle Line Extension (NS27/CE2/TE20)',
    'Thomson-East Coast Line (TE19)',
    'East-West Line (EW19)',
    'Downtown Line (NS21/DT11)',
    'Changi Airport Branch Line (CG1/DT35)',
    'Punggol LRT (PW1)',
    'Sengkang LRT (SW5)',
    'East-West Line (EW8/CC9)',
    'Circle Line (CC7)',
    'Thomson-East Coast Line (TE4)',
    'North-South Line  (NS24/NE6/CC1)',
    'Circle Line (NE12/CC13)',
    'North East Line (NE8)',
    'North East Line (EW16/NE3/TE17)',
    'North-South Line  (NS2)',
    'Sengkang LRT (SE5)',
    'Circle Line (CC21)',
    'Thomson-East Coast Line (NS27/CE2/TE20)',
    'North East Line (NE15)',
    'Downtown Line (DT7)',
    'Punggol LRT (PE3)',
    'East-West Line (EW31)',
    'Downtown Line (DT13)',
    'Punggol LRT (PW3)',
    'Downtown Line (DT21)',
    'North East Line (NE12/CC13)',
    'East-West Line (EW2/DT32)',
    'East-West Line (EW29)',
    'Thomson-East Coast Line (TE3)',
    'East-West Line (EW32)',
    'Bukit Panjang LRT (BP9)',
    'East-West Line (EW5)',
    'Downtown Line (BP6/DT1)',
    'Bukit Panjang LRT (BP12)',
    'North-South Line  (NS16)',
    'Circle Line (NS24/NE6/CC1)',
    'Bukit Panjang LRT (BP13)',
    'North-South Line  (EW14/NS26)',
    'Circle Line (CC19/DT9)',
    'Circle Line (CC4/DT15)',
    'Thomson-East Coast Line (TE6)',
    'Thomson-East Coast Line (NS9/TE2)',
    'Sengkang LRT (SW6)',
    'Circle Line (NS17/CC15)',
    'North-South Line  (NS27/CE2/TE20)',
    'Downtown Line (DT6)',
    'East-West Line (EW18)',
    'Downtown Line (DT5)',
    'Thomson-East Coast Line (TE8)',
    'Punggol LRT (NE17/PTC)',
    'East-West Line (EW14/NS26)',
    'Thomson-East Coast Line (TE12)',
    'Downtown Line (CE1/DT16)',
    'Sengkang LRT (NE16/STC)',
    'Thomson-East Coast Line (TE5)',
    'Downtown Line (DT28)',
    'Circle Line (CC28)',
    'Circle Line (CC8)',
    'North-South Line  (NS14)',
    'East-West Line (EW21/CC22)',
    'Downtown Line (DT2)',
    'Sengkang LRT (SW1)',
    'Bukit Panjang LRT (BP10)',
    'Circle Line (CC26)',
    'Bukit Panjang LRT (BP6/DT1)',
    'North-South Line  (NS25/EW13)',
    'Circle Line (CC11)',
    'North-South Line  (NS17/CC15)',
    'Downtown Line (NE7/DT12)',
    'East-West Line (EW17)',
    'North-South Line  (NS11)',
    'Bukit Panjang LRT (BP2)',
    'North-South Line  (NS20)',
    'East-West Line (NS25/EW13)',
    'Circle Line (CC5)',
    'Downtown Line (CG1/DT35)',
    'East-West Line (EW9)',
    'Bukit Panjang LRT (BP5)',
    'Bukit Panjang LRT (BP7)',
    'East-West Line (EW30)',
    'Punggol LRT (PW6)',
    'North-South Line  (NS8)',
    'Circle Line (CC20)',
    'East-West Line (EW28)',
    'North East Line (NE1/CC29)',
    'Thomson-East Coast Line (TE7)',
    'Punggol LRT (PW7)',
    'Bukit Panjang LRT (BP3)',
    'East-West Line (EW22)',
    'Downtown Line (DT18)',
    'Thomson-East Coast Line (TE16)',
    'Sengkang LRT (SW3)',
    'North East Line (NE16/STC)',
    'North East Line (NE14)',
    'North-South Line  (NS13)',
    'North-South Line  (NS10)',
    'Downtown Line (DT20)',
    'Circle Line (CC3)',
    'Circle Line (CC12)',
    'Circle Line (CC25)',
    'Thomson-East Coast Line (EW16/NE3/TE17)',
    'North-South Line  (NS12)',
    'Sengkang LRT (SW7)',
    'North-South Line  (NS18)',
    'Thomson-East Coast Line (DT10/TE11)',
    'East-West Line (EW25)',
    'East-West Line (EW7)',
    'Circle Line (CC27)',
    'East-West Line (EW20)',
    'Punggol LRT (PE1)',
    'Circle Line (CC6)',
    'Circle Line (CC2)',
    'East-West Line (EW12/DT14)',
    'Punggol LRT (PE6)',
    'Downtown Line (CC19/DT9)',
    'East-West Line (EW23)',
    'North East Line (NE9)',
    'East-West Line (EW1)',
    'East-West Line (EW15)',
    'Circle Line (CC16)',
    'North-South Line  (NS7)',
    'Circle Line (NE1/CC29)',
    'Downtown Line (DT27)',
    'East-West Line (EW24/NS1)',
    'East-West Line (EW16/NE3/TE17)',
    'East-West Line (EW26)',
    'Thomson-East Coast Line (TE22)',
    'Thomson-East Coast Line (TE18)',
    'Sengkang LRT (SE2)',
    'Thomson-East Coast Line (CC17/TE9)',
    'North East Line (NE4/DT19)'
  ]

  list_ele.innerHTML = ""
  stations.forEach((element, i) => {
    var option = document.createElement('option')
    option.value = element.match(/\(([^)]+)\)/)[1]
    option.text = element
    if(i == 0) {
      option.classList.add("selected")
    }
    
    list_ele.append(option)
  });
}

addEventListener("load", (event) => {
  console.log("HEllo")

  const start_station_list = document.getElementById("start_station_list")
  const end_station_list = document.getElementById("end_station_list")

  build_station_dropdown(start_station_list)
  build_station_dropdown(end_station_list)
});
