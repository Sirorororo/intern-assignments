from playwright.sync_api import sync_playwright
import requests
import json
import os
from ocr import OCR

product_desc = {}

with sync_playwright() as p:
    # Launch Chromium browser in headless mode
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Navigate to the webpage
    page.goto("https://www.yhdfa.vn/product/A/A04/MAD01-61?productModel=")

    cookies = page.context.cookies()
    headers = {
        "User-Agent": page.evaluate('navigator.userAgent'),
        "Referer": page.url
    }

    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])


    # Retrieving the category, sub-category and title of the product.

    category = page.locator('//div[@class="el-breadcrumb"]/span[3]/span[1]').text_content().strip()
    sub_category = page.locator('//div[@class="el-breadcrumb"]/span[4]/span[1]').text_content().strip()
    product_name = page.locator('//div[@class="el-breadcrumb"]/span[5]/span[1]').text_content().strip()

    product_desc["category"] = category
    product_desc["sub_category"] = sub_category
    product_desc["product_name"] = product_name


    # Trying to retrieve the PARAMETERS

    parameter_selection = page.locator('div.filterItem.parameter > div > div')
    div_texts = parameter_selection.all_text_contents()

    if div_texts:
        parameters = {}
        # Loop through each text content and print it
        for text in div_texts:
            text = text.strip()
            separated_strings = [s.strip() for s in text.split('\n')]
            parameters[separated_strings[0]] = separated_strings[1]
        
        product_desc["parameters"] = parameters


    # Get all possible product configurations
    product_configs={}
    product_config = page.locator('div.filterItem.product > div > div')
    config_texts = product_config.all_text_contents()

    for text in config_texts:
        text = text.strip()
        separated_strings = [s.strip() for s in text.split('\n')]
        product_configs[separated_strings[0]] = separated_strings[-1]

    product_desc["product_config"] = product_configs 


    # Get the product image
    product_image = page.locator('div.el-carousel__container img')
    image_src = product_image.get_attribute('data-src')
    product_desc["product_image_src"] = image_src

    # Requesting for the resource from current session
    response = session.get(image_src, headers=headers)

    # Structuring the folder paths
    folder_path = f"{product_desc['product_name']}/product_image/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(f'{folder_path}/product.jpg', 'wb') as file:
            file.write(response.content)


    # Extracting data from the Details, Available machine params and 3D model preview
    nav_bar = page.locator('div.el-tabs__nav.is-top div')
    nav_bar_count = nav_bar.count()

    details = {}
    if nav_bar_count >= 2:
        # Details
        details_tab = page.locator('div.technicalDrawingTagBox span').all_text_contents()

        # Material Drawing
        image_locator = page.locator('div.imgBox.imgBox1 img')
        material_src = image_locator.get_attribute("src")
        details["material_src"] = material_src

        response = session.get(material_src, headers=headers)
        folder_path = f"{product_desc['product_name']}/material_src/"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(f'{folder_path}/material.jpg', 'wb') as file:
            file.write(response.content)

        # Parameter
        parameters = page.locator('div.parameterImagesTabBtnBox button').all_text_contents()
        image_locator = page.locator('div.imgBox.imgBox2 div.moveDiv > div div')
        count = image_locator.count()

        folder_path = f"{product_desc['product_name']}/parameter_src/"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        parameter_src = {}
        for i in range(count):
            div = image_locator.nth(i)
            img_locator = div.locator('img')
            img_count = img_locator.count()
            
            img_list = []
            for j in range(img_count):
                img_src = img_locator.nth(j)
                param_src = img_src.get_attribute('data-src')
                response = session.get(param_src, headers=headers)
                with open(f'{folder_path}/{parameters[i].strip()}-{j}.jpg', 'wb') as file:
                    file.write(response.content)
                img_list.append(param_src)

            parameter_src[parameters[i].strip()] = img_list

        details["parameter_src"] = parameter_src
    
    product_desc["detail"] = details

    if nav_bar_count == 3:
    # Available machining parameters
        av_parameters = page.locator('//div[@id="pane-Avaliable machining parameters"]//img')
        av_machine_params = av_parameters.get_attribute('data-src')
        product_desc["available_machine_params_src"] = av_machine_params

        folder_path = f"{product_desc['product_name']}/av_machine_params_src/"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        response = session.get(av_machine_params, headers=headers)
        with open(f'{folder_path}/av_machine_params.jpg', 'wb') as file:
            file.write(response.content)

    
    print(json.dumps(product_desc,indent=4))
    
    ocr = OCR()
    ocr.ocr_product(product_desc["product_name"])

    browser.close()





    # response = session.get(image_src, headers=headers)

    # if response.status_code == 200:
    #     with open(f'Product/product_image/{product_desc["product_name"]}.jpg', 'wb') as file:
    #         file.write(response.content)
    #     print("Image downloaded successfully.")
    # else:
    #     print(f"Failed to download the image. Status code: {response.status_code}")


