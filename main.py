import json
import sys
import argparse
import requests
from bs4 import BeautifulSoup
import gzip
import shutil
import os
import re
#
# sitemap_url = 'https://www.booking.com/sitembk-hotel-index.xml'
#
# response = requests.get(sitemap_url)
# soup = BeautifulSoup(response.content, "xml")
# texts = str(soup.findAll(text=True)).replace('\\n', '')
# # the links compressed for all the hotels
# child = soup.find_all("sitemap")
# for link in child:
#     if "en-us" in link.find("loc").text:
#         print(link.find("loc").text)
#         r = requests.get(link.find("loc").text, allow_redirects=True)
#         open(r'C:\Users\philo\Desktop\booking.com\temp.xml.gz', 'wb').write(r.content)
#         decompressed_file_path = r'C:\Users\philo\Desktop\booking.com\temp.xml'
#         with gzip.open(r'C:\Users\philo\Desktop\booking.com\temp.xml.gz', 'rb') as f_in:
#             with open(decompressed_file_path, 'wb') as f_out:
#                 shutil.copyfileobj(f_in, f_out)
#         with open(decompressed_file_path, 'r') as f:
#             hotels_content = f.read()
#             hotelsSoup = BeautifulSoup(hotels_content, 'xml')
#             hotel_links = hotelsSoup.find_all("url")
#             for url in hotel_links:
#                 if "/us/" in url.find("loc").text or "/ca/" in url.find("loc").text:
#                     with open(r'C:\Users\philo\Desktop\booking.com\extracted_links.txt', 'a',
#                               encoding='utf-8') as output_file:
#                         output_file.write(url.find("loc").text + '\n')
#


with open(r'C:\Users\philo\Desktop\booking.com\extracted_links.txt', 'r') as file:
    links = file.readlines()

for link in links:
    response = requests.get(link)
    print(link)
    soup = BeautifulSoup(response.content, 'lxml')
    address = soup.find('span', {'class': 'hp_address_subtitle js-hp_address_subtitle jq_tooltip'})
    name = soup.find('h2', {'class': 'd2fee87262 pp-header__title'})
    rating_stars_element = soup.find('span', attrs={"data-testid": "rating-stars"})
    rating_squares_element = soup.find('span', attrs={"data-testid": "rating-squares"})
    NoStars = 0
    if rating_stars_element:
        NoStars = len(rating_stars_element)
    elif rating_squares_element:
        NoStars = len(rating_squares_element)

    notAvailable = soup.find_all('span', {'class': 'a53cbfa6de'})
    notFound = soup.find('div', {'class': 'header-404'})
    if not name:
        filename = r"C:\Users\philo\Desktop\booking.com\NotWorking.txt"
        with open(filename, "a") as file:
            file.write(link + "\n")
        continue

    if notAvailable:
        notAvailable = soup.find_all('span', {'class': 'a53cbfa6de'}).pop()

    if "These properties match your search but are outside" in notAvailable.text or notFound:
        filename = r"C:\Users\philo\Desktop\booking.com\NotWorking.txt"
        with open(filename, "a") as file:
            file.write(link + "\n")
        continue
    else:
        links_with_style = soup.find_all('a', class_='bh-photo-grid-item')
        img_links = [re.search(r'url\((.*?)\)', link['style']).group(1) for link in links_with_style if "/images/hotel" in link['style']]
        hotelPhotos = img_links[:5]
        Descrption = soup.find('p', {'class': 'a53cbfa6de b3efd73f69'})
        # print(Descrption.text)
        About = soup.find('div', {'class': 'e50d7535fa'})
        AllContent = About.find_all('div', {'class': 'f1e6195c8b'})
        activities_list = []
        general_list = []
        parking_list = []
        internet_list = []
        services_list = []

        for tag in AllContent:
            ContentType = tag.find('div', {'class': 'd1ca9115fe'})
            expandContent = tag.find_all('span', {'class': 'a5a5a75131'})
            littleInfo = tag.find('div', {'class': 'a53cbfa6de f45d8e4c32 df64fda51b'})
            if ContentType.text == "Activities":
                activities_content = [content.text for content in expandContent]
                activities_list.extend(activities_content)

            elif ContentType.text == "General":
                general_content = [content.text for content in expandContent]
                general_list.extend(general_content)

            elif ContentType.text == "Parking":
                parking_content = [content.text for content in expandContent]
                if littleInfo:
                    parking_list.append(littleInfo.text)
                parking_list.extend(parking_content)

            elif ContentType.text == "Internet":
                interests_content = [content.text for content in expandContent]
                if littleInfo:
                    internet_list.append(littleInfo.text)
                internet_list.extend(interests_content)

            elif ContentType.text == "Services":
                services_content = [content.text for content in expandContent]
                services_list.extend(services_content)

        # print("Activities List:", activities_list)
        # print("General List:", general_list)
        # print("Parking List:", parking_list)
        # print("Internet List:", internet_list)
        # print("Services List:", services_list)
        name_str = name.text
        address_str = address.text
        hotelPhotos_first_5 = hotelPhotos[:5]
        Descrption_str = Descrption.text
        activities_list = [str(tag) for tag in activities_list]
        general_list = [str(tag) for tag in general_list]
        parking_list = [str(tag) for tag in parking_list]
        internet_list = [str(tag) for tag in internet_list]
        services_list = [str(tag) for tag in services_list]
        hotelPhotos_list = [str(tag) for tag in hotelPhotos_first_5]
        data = {
            "name": name_str,
            "address": address_str,
            "star_rating": NoStars,
            "photos": hotelPhotos_list,
            "description": Descrption_str,
            "Activities": activities_list,
            "General": general_list,
            "Parking": parking_list,
            "Internet": internet_list,
            "Services": services_list,
        }
        file_path = r"C:\Users\philo\Desktop\booking.com\hotel_data.json"
        with open(file_path, "a") as json_file:
            json.dump(data, json_file, indent=2)

#
#



# link = 'https://www.booking.com/hotel/eg/palmera-beach-resort.en-gb.html?aid=2369661&label=msn-0wuZ0McuYFtmhkKWlYu9Xg-80814291883222%3Atikwd-80814466519028%3Aloc-187%3Aneo%3Amte%3Alp187%3Adec%3Aqsbooking.com&sid=2055d364634e04d9ad2328a872aa9847&dest_id=900040497;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;hpos=1;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1703771279;srpvid=b6dc6101aae600ad;type=total;ucfs=1&#hotelTmpl'
# response = requests.get(link)
# if response.status_code is 200:
#     soup = BeautifulSoup(response.content, 'lxml')
#     notAvailable = soup.find_all('span', {'class': 'a53cbfa6de'})
#     notFound = soup.find('div', {'class': 'header-404'})
#     if notAvailable:
#         notAvailable = soup.find_all('span', {'class': 'a53cbfa6de'}).pop()
#
#     if "These properties match your search but are outside" in notAvailable.text or notFound:
#         print("Not valid link")
#         sys.exit()
#     else:
#         address = soup.find('span', {'class': 'hp_address_subtitle js-hp_address_subtitle jq_tooltip'})
#         name = soup.find('h2', {'class': 'd2fee87262 pp-header__title'})
#         if not name:
#             print("Not valid link")
#             sys.exit()
#         rating_stars_element = soup.find('span', attrs={"data-testid": "rating-stars"})
#         rating_squares_element = soup.find('span', attrs={"data-testid": "rating-squares"})
#         NoStars = 0
#         if rating_stars_element:
#             NoStars = len(rating_stars_element)
#         elif rating_squares_element:
#             NoStars = len(rating_squares_element)
#         links_with_style = soup.find_all('a', class_='bh-photo-grid-item')
#         img_links = [re.search(r'url\((.*?)\)', link['style']).group(1) for link in links_with_style if
#                      "/images/hotel" in link['style']]
#         hotelPhotos = img_links[:5]
#         Descrption = soup.find('p', {'class': 'a53cbfa6de b3efd73f69'})
#         # print(Descrption.text)
#         About = soup.find('div', {'class': 'e50d7535fa'})
#         AllContent = About.find_all('div', {'class': 'f1e6195c8b'})
#         activities_list = []
#         general_list = []
#         parking_list = []
#         internet_list = []
#         services_list = []
#
#         for tag in AllContent:
#             ContentType = tag.find('div', {'class': 'd1ca9115fe'})
#             expandContent = tag.find_all('span', {'class': 'a5a5a75131'})
#             littleInfo = tag.find('div', {'class': 'a53cbfa6de f45d8e4c32 df64fda51b'})
#             if ContentType.text == "Activities":
#                 activities_content = [content.text for content in expandContent]
#                 activities_list.extend(activities_content)
#
#             elif ContentType.text == "General":
#                 general_content = [content.text for content in expandContent]
#                 general_list.extend(general_content)
#
#             elif ContentType.text == "Parking":
#                 parking_content = [content.text for content in expandContent]
#                 if littleInfo:
#                     parking_list.append(littleInfo.text)
#                 parking_list.extend(parking_content)
#
#             elif ContentType.text == "Internet":
#                 interests_content = [content.text for content in expandContent]
#                 if littleInfo:
#                     internet_list.append(littleInfo.text)
#                 internet_list.extend(interests_content)
#
#             elif ContentType.text == "Services":
#                 services_content = [content.text for content in expandContent]
#                 services_list.extend(services_content)
#
#         # print("Activities List:", activities_list)
#         # print("General List:", general_list)
#         # print("Parking List:", parking_list)
#         # print("Internet List:", internet_list)
#         # print("Services List:", services_list)
#         name_str = name.text
#         address_str = address.text
#         hotelPhotos_first_5 = hotelPhotos[:5]
#         Descrption_str = Descrption.text
#         activities_list = [str(tag) for tag in activities_list]
#         general_list = [str(tag) for tag in general_list]
#         parking_list = [str(tag) for tag in parking_list]
#         internet_list = [str(tag) for tag in internet_list]
#         services_list = [str(tag) for tag in services_list]
#         hotelPhotos_list = [str(tag) for tag in hotelPhotos_first_5]
#         data = {
#             "name": name_str,
#             "address": address_str,
#             "star_rating": NoStars,
#             "photos": hotelPhotos_list,
#             "description": Descrption_str,
#             "Activities": activities_list,
#             "General": general_list,
#             "Parking": parking_list,
#             "Internet": internet_list,
#             "Services": services_list,
#         }
#         for key, value in data.items():
#             if isinstance(value, str):
#                 data[key] = value.replace('\n', '')
#         json_data = json.dumps(data, indent=2)
#         print(json_data)