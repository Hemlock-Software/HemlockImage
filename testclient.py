import requests

def main():
    image_path = input("Please enter the path to the image you want to upload: ")

    with open(image_path, 'rb') as img_file:
        response = requests.post('http://localhost:42069/api/v1/upload', files={'file': img_file})
        
    if response.status_code == 200:
        print("Upload successful. The image is available at the following URL:")
        print(response.json()['file_url'])
    else:
        print(f"Error: {response.json()['error']}")
    
    input("Press ENTER to finish...")

if __name__ == "__main__":
    main()
