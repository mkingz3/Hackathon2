import requests
from bs4 import BeautifulSoup as BS
import csv 

def get_html(url):

    response = requests.get(url)
    return response.text

def get_data(html):
    soup = BS(html, 'lxml')
    catalog = soup.find('div', class_ = 'list-view')
    phones = catalog.find_all('div', class_ = 'item product_listbox oh')
    # print(phones)
    for phone in phones:
        try:
            title = phone.find('div', class_ = 'listbox_title oh').text.strip()
        except AttributeError:
            title = 'No title'    
            # print(title)
        try:
            price = phone.find('div', class_ = 'listbox_price text-center').text
            # print(price)
        except AttributeError:
            price = 'No price'
        try:        
            img = phone.find('div', class_ = 'listbox_img pull-left').find('img').get('src')
            # print(img)
        except AttributeError:
            img = 'No img'
    
        data = {
            'title': title,
            'price': price,
            'image': img,
            }
        write_in_file_csv(data)
        write_in_file_txt([title, ' ', price, ' ', img, '\n'])
        # break

def write_in_file_csv(data):
    with open('phones.csv', 'a') as file:
        names = ['title', 'price', 'image']
        writer = csv.DictWriter(file, delimiter=',' or ' ', fieldnames=names)
        writer.writerow(data) 


def write_in_file_txt(data):
    with open('phones.txt', 'a') as file:
        file.writelines(data)



def main():
    try: 
        for i in range(1, 28):
            url = f'https://www.kivano.kg/mobilnye-telefony?page={i}'
            html = get_html(url)
            get_data(html)
            print(f'спарсили {i} страницу')
            # break

    except AttributeError:
        print('Last page')

if __name__ == '__main__':
    main()