import requests

def download_image(image_url, save_path):
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"{save_path}")
    else:
        print("HTTP code:", response.status_code)
