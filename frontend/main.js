function get_crowd_viz() {
  var day_type = 'WEEKDAY'
  if(document.getElementById('weekday_radio_input').checked) {
    day_type = 'WEEKDAY'
  } else if (document.getElementById('weekend_radio_input').checked) {
    day_type = 'WEEKEND'
  }

  const start_station = document.getElementById('start_station_list').value
  const end_station = document.getElementById('end_station_list').value

  document.getElementById('heatmap_spinner').classList.remove('d-none')

  axios.get(`https://boundtotheearth.pythonanywhere.com/${day_type}/${start_station}/${end_station}`)
    .then(function (response) {
      console.log(response)
      document.getElementById('heatmap_div').innerHTML = response.data
      document.getElementById('heatmap_svg').classList.add("w-100", "h-auto")
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
  var stations = ['Admiralty (NS10)',
    'Aljunied (EW9)',
    'Ang Mo Kio (NS16)',
    'Bakau (SE3)',
    'Bangkit (BP9)',
    'Bartley (CC12)',
    'Bayfront (CE1/DT16)',
    'Beauty World (DT5)',
    'Bedok (EW5)',
    'Bedok North (DT29)',
    'Bedok Reservoir (DT30)',
    'Bencoolen (DT21)',
    'Bendemeer (DT23)',
    'Bishan (NS17/CC15)',
    'Boon Keng (NE9)',
    'Boon Lay (EW27)',
    'Botanic Gardens (CC19/DT9)',
    'Braddell (NS18)',
    'Bras Basah (CC2)',
    'Bright Hill (TE7)',
    'Buangkok (NE15)',
    'Bugis (EW12/DT14)',
    'Bukit Batok (NS2)',
    'Bukit Gombak (NS3)',
    'Bukit Panjang (BP6/DT1)',
    'Buona Vista (EW21/CC22)',
    'Caldecott (CC17/TE9)',
    'Canberra (NS12)',
    'Cashew (DT2)',
    'Changi Airport (CG2)',
    'Cheng Lim (SW1)',
    'Chinatown (NE4/DT19)',
    'Chinese Garden (EW25)',
    'Choa Chu Kang (NS4/BP1)',
    'City Hall (NS25/EW13)',
    'Clarke Quay (NE5)',
    'Clementi (EW23)',
    'Commonwealth (EW20)',
    'Compassvale (SE1)',
    'Coral Edge (PE3)',
    'Cove (PE1)',
    'Dakota (CC8)',
    'Damai (PE7)',
    'Dhoby Ghaut (NS24/NE6/CC1)',
    'Dover (EW22)',
    'Downtown (DT17)',
    'Esplanade (CC3)',
    'Eunos (EW7)',
    'Expo (CG1/DT35)',
    'Fajar (BP10)',
    'Farmway (SW2)',
    'Farrer Park (NE8)',
    'Farrer Road (CC20)',
    'Fernvale (SW5)',
    'Fort Canning (DT20)',
    'Gardens by the Bay (TE22)',
    'Geylang Bahru (DT24)',
    'Great World (TE15)',
    'Gul Circle (EW30)',
    'HarbourFront (NE1/CC29)',
    'Havelock (TE16)',
    'Haw Par Villa (CC25)',
    'Hillview (DT3)',
    'Holland Village (CC21)',
    'Hougang (NE14)',
    'Jalan Besar (DT22)',
    'Jelapang (BP12)',
    'Joo Koon (EW29)',
    'Jurong East (EW24/NS1)',
    'Kadaloor (PE5)',
    'Kaki Bukit (DT28)',
    'Kallang (EW10)',
    'Kangkar (SE4)',
    'Keat Hong (BP3)',
    'Kembangan (EW6)',
    'Kent Ridge (CC24)',
    'Khatib (NS14)',
    'King Albert Park (DT6)',
    'Kovan (NE13)',
    'Kranji (NS7)',
    'Kupang (SW3)',
    'Labrador Park (CC27)',
    'Lakeside (EW26)',
    'Lavender (EW11)',
    'Layar (SW6)',
    'Lentor (TE5)',
    'Little India (NE7/DT12)',
    'Lorong Chuan (CC14)',
    'MacPherson (CC10/DT26)',
    'Marina Bay (NS27/CE2/TE20)',
    'Marina South Pier (NS28)',
    'Marsiling (NS8)',
    'Marymount (CC16)',
    'Mattar (DT25)',
    'Maxwell (TE18)',
    'Mayflower (TE6)',
    'Meridian (PE2)',
    'Mountbatten (CC7)',
    'Napier (TE12)',
    'Newton (NS21/DT11)',
    'Nibong (PW5)',
    'Nicoll Highway (CC5)',
    'Novena (NS20)',
    'Oasis (PE6)',
    'one-north (CC23)',
    'Orchard (TE14/NS22)',
    'Orchard Boulevard (TE13)',
    'Outram Park (EW16/NE3/TE17)',
    'Pasir Panjang (CC26)',
    'Pasir Ris (EW1)',
    'Paya Lebar (EW8/CC9)',
    'Pending (BP8)',
    'Petir (BP7)',
    'Phoenix (BP5)',
    'Pioneer (EW28)',
    'Potong Pasir (NE10)',
    'Promenade (CC4/DT15)',
    'Punggol (NE17/PTC)',
    'Punggol Point (PW3)',
    'Queenstown (EW19)',
    'Raffles Place (EW14/NS26)',
    'Ranggung (SE5)',
    'Redhill (EW18)',
    'Renjong (SW8)',
    'Riviera (PE4)',
    'Rochor (DT13)',
    'Rumbia (SE2)',
    'Sam Kee (PW1)',
    'Samudera (PW4)',
    'Segar (BP11)',
    'Sembawang (NS11)',
    'Sengkang (NE16/STC)',
    'Senja (BP13)',
    'Serangoon (NE12/CC13)',
    'Shenton Way (TE19)',
    'Simei (EW3)',
    'Sixth Avenue (DT7)',
    'Somerset (NS23)',
    'Soo Teck (PW7)',
    'South View (BP2)',
    'Springleaf (TE4)',
    'Stadium (CC6)',
    'Stevens (DT10/TE11)',
    'Sumang (PW6)',
    'Tai Seng (CC11)',
    'Tampines (EW2/DT32)',
    'Tampines East (DT33)',
    'Tampines West (DT31)',
    'Tan Kah Kee (DT8)',
    'Tanah Merah (EW4)',
    'Tanjong Pagar (EW15)',
    'Teck Whye (BP4)',
    'Telok Ayer (DT18)',
    'Telok Blangah (CC28)',
    'Thanggam (SW4)',
    'Tiong Bahru (EW17)',
    'Toa Payoh (NS19)',
    'Tongkang (SW7)',
    'Tuas Crescent (EW31)',
    'Tuas Link (EW33)',
    'Tuas West Road (EW32)',
    'Ubi (DT27)',
    'Upper Changi (DT34)',
    'Upper Thomson (TE8)',
    'Woodlands  (NS9/TE2)',
    'Woodlands (NS9/TE2)',
    'Woodlands North  (TE1)',
    'Woodlands South  (TE3)',
    'Woodleigh (NE11)',
    'Yew Tee (NS5)',
    'Yio Chu Kang (NS15)',
    'Yishun (NS13)'
    ]

  list_ele.innerHTML = ""
  stations.forEach((element, i) => {
    var option = document.createElement('option')
    option.value = element.match(/\(([^)]+)\)/)[1].replace(/\//g, "_")
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
