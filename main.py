from CentralTokenAuth import CentralTokenAuth
from decorest import GET, RestClient, accept, backend, on, timeout


# REST-Client with decorest
@backend('httpx')
@timeout(60)
class Central(RestClient):

    @GET('/firmware/v1/devices/{serial}')
    @accept('application/json')
    @on(200, lambda r: r.json())
    @on(400, lambda r: r.json())
    def get_firmware_details_of_device(self, serial: str):
        """
        Get Firmware details for a specific device, applicable only
        for MAS Switches, Aruba Switches and Controllers
        
        ---
        
        https://developer.arubanetworks.com/aruba-central/reference/apifirmwareget_device_firmware_details
        """


# Configure central instance
base_url = 'https://internal-apigw.central.arubanetworks.com'

# Cofigure credentials
client_id_file = './client_id.json'
credential_file = './credential.json'

# Create client
central_client = Central(base_url,
                         backend='httpx',
                         auth=CentralTokenAuth(
                             base_url=base_url,
                             client_id_file=client_id_file,
                             credential_file=credential_file))

# Target Firmware
target_firmware = '16.10.0021'

# Check in an endless loop
while True:
    # Read the Serial Number via the Console
    serial = input('Serial? ')

    # Central Firmware Status API Call with Serial
    try:
        firmware_details = central_client.get_firmware_details_of_device(
            serial)

        # Evaluate Result
        if firmware_details['firmware_version'] == target_firmware:
            print('Correct Firmware')
        else:
            print('Still upgrading')
    except Exception as err:
        print(err)
