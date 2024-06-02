#ALL CODE BY AKHILESH GOPAN
#CREDITS TO NASA FOR API
import time
import requests
import datetime
import os
from PIL import Image, ImageSequence
from calendar import monthrange
import cv2
import numpy as np
import imageio

text = """
INSTRUCTIONS:
1. The year must be a 4 digit number. (ex: 20xx)
2. The year must be from 2015 to 2024
3. The month must be a 2 digit number. (ex: 02) for february
4. The month must be between 01 to 12
5. The day must be a 2 digit number. (ex: 02)
6. The day must be between 01 to the max number of days in a month
7. Do not enter Alphabets

WARNING:
DO NOT COPY MY CODE AND NOT GIVE CREDIT AS IT IS VERY BAD TO STEAL CODE!

CREDITS:
API: NASA
PROGRAMMER: Akhilesh Gopan
IDEA BY: Akhilesh Gopan
"""

print(text)


try:
    os.mkdir('photos')
except Exception as e:
    pass

current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month
current_day = datetime.datetime.now().day

Year = input("Year: ")
Month = input("Month: ")
Day = input("Day: ")
try:

    if len(Year) > 4 or len(Year) < 4:
        print("The Year must be 4 digits long.")
        print("Restarting program...")
        time.sleep(2)
        # os.startfile("EarthViewer.exe")
        exit()

    if len(Month) > 2 or len(Month) < 2:
        print("The Month must be 2 digits long.")
        print("Restarting program...")
        time.sleep(2)
        # os.startfile("EarthViewer.exe")
        exit()

    if len(Day) > 2 or len(Day) < 2:
        print("The Day must be 2 digits long.")
        print("Restarting program...")
        time.sleep(2)
        # os.startfile("EarthViewer.exe")
        exit()

    try:
        Year = int(Year)
        Month = int(Month)
        Day = int(Day)
    except Exception as e:
        print("Provide Numbers not String characters or floats.")
        print("Restarting program...")
        time.sleep(2)
        # os.startfile("EarthViewer.exe")
        exit()

    number_of_days_in_month = monthrange(Year, Month)[1]

    if Year < 2015 or Year > current_year:
        print(f"The Year value must be between 2015 and {current_year}")
        print("Restarting program...")
        time.sleep(2)
        # os.startfile("EarthViewer.exe")
        exit()

    if (Month < 1 or Month > current_month) and (Year == current_year):
        print(f"The Year value must be between 01 and {current_month}")
        print("Restarting program...")
        time.sleep(2)
        # os.startfile("EarthViewer.exe")
        exit()

    if (Month < 1 or Month > 12) and (Year != current_year):
        print(f"The Year value must be between 01 and {current_month}")
        print("Restarting program...")
        time.sleep(2)
        # os.startfile("EarthViewer.exe")
        exit()

    if (Day < 1 or Day > current_day) and (Year == current_year) and (Month == current_month):
        print(f"The Day value must be between 01 and {current_day}")
        print("Restarting program...")
        time.sleep(2)
        # os.startfile("EarthViewer.exe)
        exit()

    if (Day < 1 or Day > number_of_days_in_month):
        print(f"The Day value must be between 01 and {number_of_days_in_month}")
        print("Restarting program...")
        time.sleep(2)
        # os.startfile("EarthViewer.exe")
        exit()


except Exception as e:
    print(
        "Something could have gone wrong on the API's end due to the user suggesting a date in which the sattelite might have not taken any images,\nSorry for the inconvinience\nTry a different date.")
    print(f"Restarting program...")
    time.sleep(2)
    # os.startfile("EarthViewer.exe")
    exit()

try:
    if (len(str(Month)) == 1) and (len(str(Day)) == 2):
        date = f'{Year}-0{Month}-{Day}'

    if (len(str(Day)) == 1) and (len(str(Month)) == 2):
        date = f'{Year}-{Month}-0{Day}'

    if (len(str(Month)) == 1) and (len(str(Day)) == 1):
        date = f'{Year}-0{Month}-0{Day}'

    if (len(str(Month)) == 2) and (len(str(Day)) == 2):
        date = f'{Year}-{Month}-{Day}'
    # print(date)

except Exception as e:
    pass
    time.sleep(2)
    # os.startfile("EarthViewer.exe")
    exit()

def get_epic_imagery(date=None, size='natural', api_key=None):
    if date is None:
        date = datetime.datetime.now().strftime('%Y-%m-%d')

    url = f'https://api.nasa.gov/EPIC/api/natural/date/{date}'
    params = {
        'api_key': api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        epic_data = response.json()
        image_urls = [img['image'] for img in epic_data]
        return image_urls
    else:
        print(f"Failed to retrieve EPIC imagery. Status code: {response.status_code}")
        return None


def process_frame(frame):
    # Resize the frame if needed
    new_width, new_height = 600, 600  # Adjust dimensions as needed
    resized_frame = cv2.resize(frame, (new_width, new_height))

    # Convert frame to grayscale
    gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    # Apply preprocessing techniques (e.g., thresholding) to enhance contrast
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on a separate image
    contour_image = np.zeros_like(resized_frame)
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)  # Adjust the thickness value here

    # Combine the contour image with the original frame
    output_frame = cv2.addWeighted(resized_frame, 0.8, contour_image, 0.2, 0)

    return output_frame


if __name__ == "__main__":
    api_key = '94Hn7vK7B1vHM8vjdNYG8C1TnmPXdlBjZBQEYIdB'

    image_urls = get_epic_imagery(date, api_key=api_key)

    if image_urls:
        try:
            os.mkdir(f'photos/{date}')

        except Exception as e:
            print(f"Sorry, but this folder on this date exists. Here's the error {e}")
            time.sleep(2)
            # os.startfile("EarthViewer.exe")
            exit()

        for idx, url in enumerate(image_urls):
            total_url = f'https://api.nasa.gov/EPIC/archive/natural/{date[0:4]}/{date[5:7]}/{date[8:10]}/png/{url}.png?api_key={api_key}'
            data = requests.get(total_url).content
            # print(f"Image {idx + 1}: {url}")
            # print(total_url)
            f = open(f'photos/{date}/{url}.png', 'wb')

            f.write(data)
            f.close()
            print(f"Succesfully outputed {url}.png at photos/{date}")

        filenames = os.listdir(f'photos/{date}')
        img = []
        for filename in filenames:
            img.append(Image.open(f'photos/{date}/{filename}'))

        img[0].save(f'photos/{date}/Earth on {date}.gif', save_all=True, append_images=img[1:], duration=200, loop=0)

        print(f"Succesfully outputed Earth on {date}.gif at photos/{date}")
        contourgif = input("Do you want a contour gif? (Y or N): ")

        try:
            # 2021 - 02 - 11
            if (contourgif == 'Y') or (contourgif == 'y'):
                input_file = f'photos/{date}/Earth on {date}.gif'
                gif_reader = imageio.get_reader(input_file)

                # Process each frame and store in a list
                processed_frames = [process_frame(frame) for frame in gif_reader]

                # Write the processed frames to a new GIF file
                output_file = f'photos/{date}/Earth on {date} with contours.gif'
                imageio.mimsave(output_file, processed_frames, loop=0, duration=300)

                print("Output GIF with contours saved as:", output_file)

            else:
                pass

        except Exception as e:
            pass

    else:
        print("Failed to retrieve EPIC imagery.")
        time.sleep(2)
        # print(date)
        # os.startfile("EarthViewer.exe")
        exit()


