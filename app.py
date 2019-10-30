# Example for multiple page in one city
import requests
import logging
from threading import Thread
import threading
from connection_to_db import execute_query

logging.basicConfig(filename='app.log', filemode='w')


def split_name(full_name):
    """
        Tách tên: "Nguyễn Hữu Hiếu A"
        RETURN:
            - "Nguyễn Hữu Hiếu" -> ('Nguyeenx', 'Hữu', 'Hiếu')
            - "Nguyeenx Hữu"    -> ('Nguyeenx', '', 'Hữu')
            - "Nguyeenx"        -> ('', '', 'Nguyeenx')

    """
    if full_name is '' or None:
        return ('', '', '')
    full_name_array = full_name.split(" ")
    lastname = full_name_array.pop(-1)
    surname = full_name_array.pop(0) if len(full_name_array) != 0 else ""
    middlename = " ".join(full_name_array)
    return (surname, middlename, lastname)


def insert_to_company(company):
    # print(company)
    company_name = company["Title"]
    registered_address = company["NoiDangKyQuanLy_CoQuanTitle"]
    company_address = company["DiaChiCongTy"]
    owner_name = company["ChuSoHuu"]
    occupation = company["NganhNgheTitle"]
    tax_number = company["MaSoThue"]
    city = company["TinhThanhTitle"]
    district = company["QuanHuyenTitle"]
    ward = company["PhuongXaTitle"]
    full_name = company["ChuSoHuu"]
    surname, middlename, lastname = split_name(full_name)
    url = f"""https://thongtindoanhnghiep.co/api/company/{tax_number}"""
    query = f"""
    INSERT INTO public.company_info(
            company_name, url, registered_address, company_address, owner_name, occupation, tax_number, city, district, ward, full_name, surname, middlename, lastname)
    VALUES ( 
    $$ '{company_name}'$$,
    $$ '{url}'$$,
    $$ '{registered_address}'$$, 
    $$ '{company_address}'$$,
    $$ '{owner_name}'$$,
    $$ '{occupation}'$$,
    $$ '{tax_number}'$$,
    $$ '{city}'$$,
    $$ '{district}'$$,
    $$ '{ward}'$$,
    $$ '{full_name}'$$,
    $$ '{surname}'$$,
    $$ '{middlename}'$$,
    $$ '{lastname}'$$) ON CONFLICT (tax_number) DO NOTHING;
    """
    execute_query(query)
    print(f"Insert company success: {city}: {company_name}")


def generate_data_for_one_city(city_name="ha_noi"):
    print("city name: ", city_name)
    page = 1
    while True:
        url = f"https://thongtindoanhnghiep.co/api/company?l={city_name}&&r=100&&p={page}"
        response = requests.get(url)
        response.encoding = 'utf-8'
        content = response.json()
        list_data_sort_company = content["LtsItems"]
        # tổng số doanh nghiệp trong 1 thành phố
        total_in_one_city = int(content["Option"]["TotalRow"])
        if page * 100 > total_in_one_city:
            print(page * 100, ' ', total_in_one_city)
            break
        for company in list_data_sort_company:
            # với mỗi công ty ta lấy info và inserst vào db
            url_company_detail = f"""https://thongtindoanhnghiep.co/api/company/{company["MaSoThue"]}"""
            if str(company["MaSoThue"]) == '1201514416':
                return
            res = requests.get(url_company_detail)
            insert_to_company(company=res.json())

        print("**********page complete**********: ", city_name, " ", page)
        page = page + 1  # tăng page để tăng vòng lặp
    print("city done: ", city_name)


list_city_name1 = ['tien-giang', 'hung-yen', 'ha-noi', 'tp-ho-chi-minh',
                   'ca-mau', 'dac-lac', 'nam-dinh', 'quang-ninh', 'dak-nong', 'da-nang']
list_city_name2 = ['hai-duong', 'long-an', 'ben-tre', 'dong-thap', 'vinh-long',
                   'kien-giang', 'tra-vinh', 'soc-trang', 'bac-ninh', 'thanh-hoa', 'vung-tau']
list_city_name3 = ['dong-nai', 'binh-duong', 'thai-nguyen', 'thai-binh', 'can-tho',
                   'nghe-an', 'hue', 'binh-phuoc', 'quang-nam', 'quang-ngai', 'ninh-thuan', 'ninh-binh', 'binh-thuan', 'kon-tum', 'vinh-phuc', ]
list_city_name4 = ['lao-cai', 'hai-phong', 'an-giang', 'phu-tho', 'tay-ninh',
                   'khanh-hoa', 'phu-yen', 'hoa-binh', 'tuyen-quang', 'lai-chau', 'hau-giang']
list_city_name5 = ['lam-dong', 'lang-son', 'ha-nam', 'bac-can', 'binh-dinh',
                   'cao-bang', 'son-la', 'quang-binh', 'quang-tri', 'gia-lai', 'bac-giang', 'ha-tinh', 'bac-lieu', 'yen-bai', 'dien-bien', 'ha-giang', 'chua-ro']


def generate_from_list_city(cities):
    """
        Sử dụng để chạy đa luồng
        - Lấy ra dữ liệu từ mảng các thành phố
    """
    for city in cities:
        generate_data_for_one_city(city_name=city)


if __name__ == "__main__":
    try:
        thread1 = threading.Thread(
            target=generate_from_list_city, args=(list_city_name1,))
        thread2 = threading.Thread(
            target=generate_from_list_city, args=(list_city_name2,))
        thread3 = threading.Thread(
            target=generate_from_list_city, args=(list_city_name3,))
        thread4 = threading.Thread(
            target=generate_from_list_city, args=(list_city_name4,))
        thread5 = threading.Thread(
            target=generate_from_list_city, args=(list_city_name5,))
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        # thread5.start()
    except:
        print("error")
