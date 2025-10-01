import hashlib
import requests
import readimg

from PIL import Image

def add_border(input_image_path, output_image_path):
    img = Image.open(input_image_path)
    
    border_size_x = int(img.width * 0.1)
    border_size_y = int(img.height * 0.1)
    
    new_img = Image.new("RGB", (img.width + 2 * border_size_x, img.height + 2 * border_size_y), "white")
    
    new_img.paste(img, (border_size_x, border_size_y))

    new_img.save(output_image_path)

def get_hash_file(image_path, hash_algorithm='sha256'):
    hash_func = hashlib.new(hash_algorithm)

    try:

        with open(image_path, 'rb') as image_file:
            while chunk := image_file.read(4096):
                hash_func.update(chunk)

        return hash_func.hexdigest()
    except:
        return False

def get_image_hash_from_url(image_url, hash_algorithm='sha256'):
    hash_func = hashlib.new(hash_algorithm)

    response = requests.get(image_url, stream=True)
    
    if response.status_code == 200:
        for chunk in response.iter_content(4096):
            hash_func.update(chunk)
        return hash_func.hexdigest()
    else:
        print(f"Err0: {response.status_code}")
        return None

def download_and_check_image(image_url, given_hash, save_path, hash_algorithm='sha256'):
    downloaded_hash = get_image_hash_from_url(image_url, hash_algorithm)
    
    if downloaded_hash:
        print(f"Downloaded hash: {downloaded_hash}")

        if downloaded_hash != given_hash:
            print("The hashes are different")
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded {save_path}")
                return True
            else:
                print(f"Err: {response.status_code}")
                return False
        else:
            print("The hashes are the same")
            return None
    else:
        print("Can't process hash")
        return False

image_url = 'https://www.vpnbook.com/password.php'
save_path = 'password.png'
given_hash = get_hash_file(save_path)

saved_img_result = download_and_check_image(image_url, given_hash, save_path)

if saved_img_result:
    bordered_path = "bordered_" + save_path
    add_border(save_path, bordered_path)
    
    result = readimg.confirm_tests(bordered_path)
    print(result)
    
    with open("pswd.txt", "w") as f:
        f.write(result)

    print("saved to pswd.txt")