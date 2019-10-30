# Example for multiple page in one city
import requests
import logging
from connection_to_db import execute_query

logging.basicConfig(filename='app.log', filemode='w')

number_of_company = 1


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
    global number_of_company
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
    print(f"Insert company success: {number_of_company}: {company_name}")
    number_of_company += 1


def generate_data_for_one_city(city_name="ha_noi"):
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
            res = requests.get(url_company_detail)
            insert_to_company(company=res.json())

        print("**********page complete**********: ", city_name, " ", page)
        page = page + 1  # tăng page để tăng vòng lặp
    print("city done: ", city_name)


list_city_name = ['tien-giang', 'hung-yen', 'ha-noi', 'tp-ho-chi-minh', 'ca-mau', 'dac-lac', 'nam-dinh', 'quang-ninh', 'dak-nong', 'da-nang', 'hai-duong', 'long-an', 'ben-tre', 'dong-thap', 'vinh-long', 'kien-giang', 'tra-vinh', 'soc-trang', 'bac-ninh', 'thanh-hoa', 'vung-tau', 'dong-nai', 'binh-duong', 'thai-nguyen', 'thai-binh', 'can-tho', 'nghe-an', 'hue', 'binh-phuoc', 'quang-nam', 'quang-ngai',
                  'ninh-thuan', 'lao-cai', 'hai-phong', 'an-giang', 'phu-tho', 'tay-ninh', 'khanh-hoa', 'phu-yen', 'hoa-binh', 'tuyen-quang', 'lai-chau', 'hau-giang', 'lam-dong', 'lang-son', 'ha-nam', 'bac-can', 'binh-dinh', 'cao-bang', 'son-la', 'quang-binh', 'quang-tri', 'gia-lai', 'bac-giang', 'ha-tinh', 'ninh-binh', 'binh-thuan', 'kon-tum', 'vinh-phuc', 'bac-lieu', 'yen-bai', 'dien-bien', 'ha-giang', 'chua-ro']

if __name__ == "__main__":
    for city in list_city_name:
        generate_data_for_one_city(city_name=city)