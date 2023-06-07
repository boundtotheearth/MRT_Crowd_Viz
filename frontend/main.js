function get_crowd_viz() {
  var day_type = 'WEEKDAY'
  if(document.getElementById('weekday_radio_input').checked) {
    day_type = 'WEEKDAY'
  } else if (document.getElementById('weekend_radio_input').checked) {
    day_type = 'WEEKEND'
  }

  const start_station = document.getElementById('start_station_input')
  const end_station = document.getElementById('end_station_input')

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
  var stations = ['Buangkok (NE15)',
    'Holland Village (CC21)',
    'Pioneer (EW28)',
    'Marymount (CC16)',
    'Soo Teck (PW7)',
    'Joo Koon (EW29)',
    'Outram Park (EW16/NE3/TE17)',
    'Petir (BP7)',
    'Orchard (TE14/NS22)',
    'Upper Thomson (TE8)',
    'Woodlands (NS9/TE2)',
    'Tampines West (DT31)',
    'Tanah Merah (EW4)',
    'MacPherson (CC10/DT26)',
    'Nibong (PW5)',
    'Woodlands  (NS9/TE2)',
    'Marsiling (NS8)',
    'Woodleigh (NE11)',
    'Bukit Panjang (BP6/DT1)',
    'Caldecott (CC17/TE9)',
    'Tiong Bahru (EW17)',
    'Tai Seng (CC11)',
    'Queenstown (EW19)',
    'Sembawang (NS11)',
    'City Hall (NS25/EW13)',
    'Yew Tee (NS5)',
    'Sam Kee (PW1)',
    'Jalan Besar (DT22)',
    'Chinese Garden (EW25)',
    'Nicoll Highway (CC5)',
    'Chinatown (NE4/DT19)',
    'Bendemeer (DT23)',
    'Choa Chu Kang (NS4/BP1)',
    'Keat Hong (BP3)',
    'Renjong (SW8)',
    'Somerset (NS23)',
    'Springleaf (TE4)',
    'Clementi (EW23)',
    'Bartley (CC12)',
    'Compassvale (SE1)',
    'Bencoolen (DT21)',
    'Commonwealth (EW20)',
    'Jurong East (EW24/NS1)',
    'Admiralty (NS10)',
    'Boon Keng (NE9)',
    'Promenade (CC4/DT15)',
    'Dover (EW22)',
    'Boon Lay (EW27)',
    'Rochor (DT13)',
    'Sixth Avenue (DT7)',
    'Tongkang (SW7)',
    'Kaki Bukit (DT28)',
    'Sumang (PW6)',
    'Labrador Park (CC27)',
    'Bedok North (DT29)',
    'Kallang (EW10)',
    'Toa Payoh (NS19)',
    'Sengkang (NE16/STC)',
    'Woodlands North  (TE1)',
    'Mattar (DT25)',
    'Dakota (CC8)',
    'Coral Edge (PE3)',
    'Bugis (EW12/DT14)',
    'Kembangan (EW6)',
    'Fernvale (SW5)',
    'Punggol Point (PW3)',
    'Haw Par Villa (CC25)',
    'Newton (NS21/DT11)',
    'Mountbatten (CC7)',
    'Bukit Gombak (NS3)',
    'Cashew (DT2)',
    'Yio Chu Kang (NS15)',
    'Eunos (EW7)',
    'Little India (NE7/DT12)',
    'Samudera (PW4)',
    'Ang Mo Kio (NS16)',
    'Pasir Ris (EW1)',
    'Woodlands South  (TE3)',
    'King Albert Park (DT6)',
    'Bayfront (CE1/DT16)',
    'Paya Lebar (EW8/CC9)',
    'Geylang Bahru (DT24)',
    'Serangoon (NE12/CC13)',
    'Aljunied (EW9)',
    'Bedok Reservoir (DT30)',
    'Shenton Way (TE19)',
    'South View (BP2)',
    'Cheng Lim (SW1)',
    'Segar (BP11)',
    'Buona Vista (EW21/CC22)',
    'Potong Pasir (NE10)',
    'Raffles Place (EW14/NS26)',
    'Mayflower (TE6)',
    'Hougang (NE14)',
    'Simei (EW3)',
    'Stadium (CC6)',
    'Tan Kah Kee (DT8)',
    'Ubi (DT27)',
    'Marina Bay (NS27/CE2/TE20)',
    'Marina South Pier (NS28)',
    'Clarke Quay (NE5)',
    'Senja (BP13)',
    'Oasis (PE6)',
    'Beauty World (DT5)',
    'Tuas West Road (EW32)',
    'Layar (SW6)',
    'Bishan (NS17/CC15)',
    'Changi Airport (CG2)',
    'Teck Whye (BP4)',
    'Tuas Link (EW33)',
    'Redhill (EW18)',
    'Rumbia (SE2)',
    'Cove (PE1)',
    'Kangkar (SE4)',
    'Kranji (NS7)',
    'Expo (CG1/DT35)',
    'Tanjong Pagar (EW15)',
    'HarbourFront (NE1/CC29)',
    'Tampines (EW2/DT32)',
    'Bright Hill (TE7)',
    'Lakeside (EW26)',
    'Napier (TE12)',
    'Gardens by the Bay (TE22)',
    'Kupang (SW3)',
    'Novena (NS20)',
    'Khatib (NS14)',
    'Meridian (PE2)',
    'Bakau (SE3)',
    'Braddell (NS18)',
    'Damai (PE7)',
    'Bukit Batok (NS2)',
    'Fajar (BP10)',
    'Hillview (DT3)',
    'Kovan (NE13)',
    'Lavender (EW11)',
    'Bangkit (BP9)',
    'Canberra (NS12)',
    'Havelock (TE16)',
    'Riviera (PE4)',
    'Dhoby Ghaut (NS24/NE6/CC1)',
    'Telok Blangah (CC28)',
    'Lentor (TE5)',
    'Farrer Road (CC20)',
    'Upper Changi (DT34)',
    'Thanggam (SW4)',
    'Jelapang (BP12)',
    'Downtown (DT17)',
    'Yishun (NS13)',
    'Tuas Crescent (EW31)',
    'Farrer Park (NE8)',
    'Farmway (SW2)',
    'Kadaloor (PE5)',
    'Bedok (EW5)',
    'Maxwell (TE18)',
    'Stevens (DT10/TE11)',
    'Gul Circle (EW30)',
    'Pasir Panjang (CC26)',
    'Orchard Boulevard (TE13)',
    'Botanic Gardens (CC19/DT9)',
    'Bras Basah (CC2)',
    'Esplanade (CC3)',
    'Phoenix (BP5)',
    'Great World (TE15)',
    'Fort Canning (DT20)',
    'Tampines East (DT33)',
    'Ranggung (SE5)',
    'Pending (BP8)',
    'Punggol (NE17/PTC)',
    'Telok Ayer (DT18)',
    'Lorong Chuan (CC14)',
    'one-north (CC23)',
    'Kent Ridge (CC24)'
  ]

  list_ele.innerHTML = ""
  stations.forEach((element, i) => {
    var option = document.createElement('option')
    option.value = element.match(/\(([^)]+)\)/)[1].replace("/", "_")
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
