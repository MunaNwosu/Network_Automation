import requests
import json



def mist_call(token,baseurl):
  #site_id: "825c653b-ac23-4edf-9f63-426077159fc6"
  #org_id: "6294c494-c4fe-4c24-b2f6-c2b51539d9c2"
  url1 = f"{baseurl}/orgs/6294c494-c4fe-4c24-b2f6-c2b51539d9c2/sites"
  url2 = f"{baseurl}/orgs/6294c494-c4fe-4c24-b2f6-c2b51539d9c2/wlans"
  url3 = f"{baseurl}/sites/825c653b-ac23-4edf-9f63-426077159fc6/stats/devices"

  payload = {}

  headers = {

    'Authorization': token

  }

  #sites
  response1 = requests.request("GET", url1, headers=headers, data=payload).json()
  #wlans
  response2 = requests.request("GET", url2, headers=headers, data=payload).json()
  #devices stats
  response3 = requests.request("GET", url3, headers=headers, data=payload).json()

  return response1, response2,response3

def mist_info(response1, response2,response3):

  pretty3 = json.dumps(response3, indent=4)
  print(pretty3)
  print("-"*30)

  #Amount of transmitting traffic to the clients, since reboot
  tx_bytes_24 = response3[0]['radio_stat']['band_24']['tx_bytes']/(1073741824)
  tx_bytes_5 = response3[0]['radio_stat']['band_5']['tx_bytes']/(1073741824)

	#Amount of receiving traffic from the clients, since reboot
  rx_bytes_24 = response3[0]['radio_stat']['band_24']['rx_bytes']/(1073741824)
  rx_bytes_5 = response3[0]['radio_stat']['band_5']['rx_bytes']/(1073741824)

  #Transmission utilization in percentage
  util_tx_24 = response3[0]['radio_stat']['band_24']['util_tx']
  util_tx_5 = response3[0]['radio_stat']['band_5']['util_tx']

  #number of clients
  num_clients_24 = response3[0]['radio_stat']['band_24']['num_clients']
  num_clients_5 = response3[0]['radio_stat']['band_5']['num_clients']
  total_clients = num_clients_24 + num_clients_5
  print("Total connected clients:", total_clients )

  influx_data = [tx_bytes_24,tx_bytes_5,rx_bytes_24,rx_bytes_5,util_tx_24,util_tx_5,total_clients]

  print(f'2.4 band uplink: {tx_bytes_24} GB\n'
        f'5 band uplink: {tx_bytes_5} GB\n'\
        f'2.4 band downlink: {rx_bytes_24} GB\n'
        f'5 band downlink: {rx_bytes_5} GB\n'
        f'2.4 band channel utlization: {util_tx_24}%\n'
        f'5 band channel utlization: {util_tx_5}%\n'
  )
  return influx_data