
from bs4 import BeautifulSoup
import requests
from time import sleep 
import sys 
from dotenv import load_dotenv
import os

#################################################
# things to be aware of:
# the tax form name query must equal the form number ("form w-2" is a form number for the irs, and not the name of the form like everyday people refer to it as)

####### order of execution:
# dunder main                                   
# [ x ] main                                         needs json of form year and form number
# [ x ] validate search                              needs tax form query via file path, return the validated term and year(s) in a tuple
# [ x ] request_search_results                       returns list of dicts with year, form num and link   
# [ x ] process_search_results                       needs list of dicts, and downloads each search result within specified year range to a folder with form num
#################################################


# Load environment variables
load_dotenv('env/secrets/.env')

# For utility2 I made it uber modular
def main():

# call these functions in this order:
    validate_search_terms()
    search_results = request_search_results()
    process_search_results(search_results)

def validate_search_terms(file_path = 'utility2/queries.txt'):
    try:
        with open(file_path, "r") as file:
            lines = [line.strip() for line in file if line.strip()]

            # Ensure there are exactly two lines in the file
            if len(lines) != 2:
                raise ValueError("The file must contain exactly two lines: a term and a year or year range.")

            # Validate the search term (first line)
            term = lines[0]
            if len(term.split()) > 2:
                raise ValueError(f"Invalid term '{term}'. Only single or two-word terms are allowed.")

            # Validate the year or year range (second line)
            year_line = lines[1]
            if "-" in year_line:
                start_year, end_year = year_line.split("-")
                if not (start_year.strip().isdigit() and end_year.strip().isdigit()):
                    raise ValueError(f"Invalid year range '{year_line}'. Must be in the format 'xxxx - xxxx'.")
                if int(start_year) > int(end_year):
                    raise ValueError(f"Invalid year range '{year_line}'. Start year must be less than or equal to end year.")
            else:
                if not year_line.isdigit():
                    raise ValueError(f"Invalid year '{year_line}'. Must be a four-digit year.")

            # Return the validated term and year(s) in a tuple
            # ('Form W-2', '2000 - 2024') <----tuple
            return term, year_line

    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
def request_search_results():
    search_term, years_to_save = validate_search_terms()  # Call the function directly to get the results

    base_url =f"https://www.irs.gov/prior-year-forms-and-instructions?find={search_term}&product_number=&date=&title=&items_per_page=25&page="
    count = 0
    current_url = f"{base_url}{count}"
    headers = {
    "Host": os.getenv("HEADERS_HOST"),
    "User-Agent": os.getenv("USER_AGENT"),
    "Accept": os.getenv("ACCEPT"),
    "Accept-Language": os.getenv("ACCEPT_LANGUAGE"),
    "Accept-Encoding": os.getenv("ACCEPT_ENCODING"),
    "X-Requested-With": os.getenv("X_REQUESTED_WITH"),
    "Connection": "keep-alive",
    "Referer": os.getenv("REFERER"),
    "Cookie": os.getenv("COOKIE"),
    "Sec-Fetch-Dest": os.getenv("SEC_FETCH_DEST"),
    "Sec-Fetch-Mode": os.getenv("SEC_FETCH_MODE"),
    "Sec-Fetch-Site": os.getenv("SEC_FETCH_SITE"),
    "Priority": os.getenv("PRIORITY"),
    "TE": os.getenv("TE"),
}
    results_dict_list = []

    ##########################
    # logic for requesting specific year range only
    if '-' in years_to_save:  # Parse the year range (e.g., "2000-2024")
        start_year, end_year = map(int, years_to_save.split('-'))
    else:
        start_year, end_year = int(years_to_save), int(years_to_save)  # Single year case
    ##########################

    while current_url:
        session = requests.Session()
        search_results = session.get(current_url, headers=headers)

        # Check if request was successful
        if search_results.status_code == 200:
            soup = BeautifulSoup(search_results.content, 'html.parser')
            items = soup.find_all('tr') 

            for item in items:
                # td stands for <td> table data
                td_number = item.find('td', {'class': 'views-field views-field-natural-sort-field views-field-prior-year-products-picklist-number'})
                td_year = item.find('td', {'class': 'views-field views-field-prior-year-products-picklist-revision-date'})

                if td_number:
                    a_tag_number = td_number.find('a')

                    if a_tag_number:
                        product_num = a_tag_number.text.strip() 
                        year_tag = td_year.text.strip() 
                        year = int(year_tag)
                        pdf_link = a_tag_number['href']

                        # Check if the year is in the specified range
                        if start_year <= year <= end_year:
                            if product_num == search_term:
                                results_dict_list.append({
                                    'form_number': product_num,
                                    'year': year,
                                    'link': pdf_link
                                })                        

            print(f"Processed page: {current_url}.")
            # print(results_dict_list)   

            # Find the "Next" button and update current_url
            next_button = soup.find('a', {'rel': 'next'})  
            if next_button:
                href = next_button['href']
                current_url = f"https://www.irs.gov/prior-year-forms-and-instructions{href}"
                
            else:
                print("No 'Next' button found. Ending pagination.")
                print(f"Successfully processed page(s) for '{search_term}' query within the {years_to_save} year ranges!")
                current_url = None
        else:
            print(f"Failed to retrieve data: {search_results.status_code}")
    
    return results_dict_list

def process_search_results(results):

    search_results=results
    # [{'form_number': 'Publication 80', 'year': 2023, 'link': '/pub/irs-prior/p80--2023.pdf'}, {'form_number': 'Publication 80', 'year': 2022, 'link': '/pub/irs-prior/p80--2022.pdf'}, {'form_number': 'Publication 80', 'year': 2021, 'link': '/pub/irs-prior/p80--2021.pdf'}]
    
    for result in search_results:
        pdf_link = f"https://www.irs.gov{result['link']}" #hovering over pagination elements on site and getting the endpoint from there
        form_name = result['form_number']
        file_name = f"{form_name} - {result['year']}.pdf"

        # Create the directory if it doesn't exist
        directory_path = os.path.join(f'utility2/pdfs/{form_name}')
        os.makedirs(directory_path, exist_ok=True)

        # Download the PDF
        response = requests.get(pdf_link)
        if response.status_code == 200:
            # folder name == form numer/file name
            pdf_path = os.path.join(directory_path, file_name)
            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(response.content)
            print(f"Downloaded {file_name}")
        else:
            print(f"Failed to download {file_name}")



if __name__ == "__main__":
    if len(sys.argv) != 1:
        print(" To run: 'python utility2/utility2.py'")
        sys.exit(1)
    main()

