#This function downloads the most recent report from a scheduled Simpli.fi template. Some changes have been made since it was last tested, so it may initially run with errors and need some revision.

def simplifi_get_report(organization_id, template_id, schedule_id, save_directory, save_filename_prefix, api_app_key, api_user_key):

    import datetime #for timestamp in filename
    import requests #to run 'get' requests

    #make API call to get Simpli.fi report
    headers = {"X-App-Key": api_app_key, "X-User-Key": api_user_key}
    endpoint = "https://app.simpli.fi/api/organizations/" + organization_id + "/report_center/reports/" + str(template_id) + "/schedules/" + str(schedule_id)
    response = requests.get(endpoint, 
                        headers=headers)

    print(response.status_code) #to see status to make sure it was successful

    json_data = response.json() #covert json response to python dictionary
    download_url = json_data["schedules"][0]["downloads"][0]["download_link"] #retrieve download URL of latest report from dictionary
    get_file = requests.get(download_url) #download file

    current_datetime = str(datetime.datetime.now())
    current_datetime = current_datetime.replace(':','-').replace(" ","-").replace(".","-")
    directory_and_filename = save_directory + save_filename_prefix + "_" + current_datetime + ".csv"

    #write file
    with open(directory_and_filename, "xb") as file:
        file.write(get_file.content)

