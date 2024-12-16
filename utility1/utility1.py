from bs4 import BeautifulSoup
import requests
from time import sleep 
import json #for output
import sys #system args I get from user
from dotenv import load_dotenv
import os
from collections import defaultdict
from urllib.parse import urlparse, parse_qs

# Load environment variables
load_dotenv('env/secrets/.env')

# ######################
# # Task:
# Taking a list of tax form names (ex: "Form W-2", "Form 1095-C"), search the website and return some
# informational results. Specifically, you must return the "Product Number", the "Title", and the maximum and
# minimum years the form is available for download


# [x] i want to go to the priors site via selenium
# [x] search for one item, then for a two-word query, etc
# [x] after i search i want to parse the html, 
# [x] using html results (now lists), create an empty dict and save to utility1.html
    # [x] gather the product numbers, title, min/max, make a k:v pair 
    # [x] gather the min year and max year without clicking revision buttons...this will come form a list of revision date years and i get the first and last index of that list <---initaial logic, until i realized min/max of each doc (give me notions of data normalization, so i made my own qualifiers for 'sameness' since they werent specified)


# ######################



# helper func from ch*tgpt
def validate_search_terms(file_path):
    """Validate and read search terms from the file."""
    try:
        with open(file_path, "r") as file:
            terms = [line.strip() for line in file if line.strip()]
            if not terms:
                raise ValueError("Search terms file is empty or incorrectly formatted.")
            for term in terms:
                if ' ' in term and len(term.split()) > 2:
                    raise ValueError(f"Invalid term '{term}' detected. Only single words or two-word terms are allowed.")
            return terms
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")


















def combine_terms_from_file(file_path):
    terms = validate_search_terms(file_path)
    return " ".join(terms)

def main(search_terms):

    base_url =f"https://www.irs.gov/prior-year-forms-and-instructions?find={search_terms}&product_number=&date=&title=&items_per_page=25&page="
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
    # print("env variables test")
    # print(os.getenv("HEADERS_HOST"))

    
    data_list = []

    while current_url:
        session = requests.Session()
        
        # no longer going the post route
        # if post, send via json though body...fix/find <input> value = elementfor submit btn
        # data = {
        #         '<input> value': search_terms,
        #         'edit-submit-pup-picklists': 'Search'  # Assuming this is the name of the submit button field
        #     }

        search_results = session.get(current_url, headers=headers)
        # Check if request was successful
        if search_results.status_code == 200:
            soup = BeautifulSoup(search_results.content, 'html.parser')
            items = soup.find_all('tr') 
            # dont use years=[], instead use occurrences
            occurrences = defaultdict(list)  # Dictionary to store occurrences of each <td> combination...my logic for this is that theyre the 'same' and therefore 'occur' >1  if they have the same name and form_number.

            for item in items:
                td_number = item.find('td', {'class': 'views-field views-field-natural-sort-field views-field-prior-year-products-picklist-number'})
                td_title = item.find('td', {'class': 'views-field views-field-prior-year-products-picklist-title'})
                

                if td_number and td_title:
                    a_tag_number = td_number.find('a')
                    if a_tag_number and td_title:
                        product_num = a_tag_number.text.strip() 
                        title = td_title.text.strip() 
                        
                        key = (product_num, title)
                    
                        td_year = item.find('td', {'class': 'views-field views-field-prior-year-products-picklist-revision-date'})
                        if td_year:
                            year = int(td_year.text.strip()) 
                            occurrences[key].append(year)
                        
            # Determine min and max years for each combo using years list attached to occurrence key id 
            for key, years in occurrences.items():
                min_yr = min(years)
                max_yr = max(years)
                data_list.append({
                    'form_number': key[0],
                    'form_title': key[1],
                    'min_year': min_yr,
                    'max_year': max_yr
                })
        
            # Convert list of dictionaries to JSON
            json_data = json.dumps(data_list, indent=4)

            with open('utility1/utility1_results.html', 'w', encoding='utf-8') as file:
                file.write(json_data)  # Save the formatted HTML
            # print(json_data)
            print(f"Processed page {current_url}.")
        

    # at first i thought i needed to get the min/max of the queried items in general
    # initial logic, failed

                # if sum(td_number and td_title) in items >1:
                #         td_year = item.find('td', {'class': 'views-field views-field-prior-year-products-picklist-revision-date'})             
                #         years.append(td_year.text.strip())
                #         sorted(years)
                #         min_yr= years[-1]
                #         max_yr=years[0]
                #         data_list.append({
                #                 "min_year": min_yr,
                #                 "max_year": max_yr
                #             })

    # another attempt
            # years =[]
            # for item in items:
            #     td_year = item.find('td', {'class': 'views-field views-field-prior-year-products-picklist-revision-date'})
            #     # print(td_year) 
            #     # <td class="views-field views-field-prior-year-products-picklist-revision-date" headers="view-prior-year-products-picklist-revision-date-table-column">2021        </td>
            #     if td_year:
            #         year = td_year.text.strip()  # Get the title text
            #         years.append(year)
            #         sorted(years)
            #         print(year)
            # min_year = years[-1]
            # max_year = years[0]

            # print("min year:", min_year)   
            # print("max year:", max_year)    
    

        
        
            # Find the "Next" button and update current_url
            next_button = soup.find('a', {'rel': 'next'})  
            if next_button:
                # chatgpt
                href = next_button['href']
                current_url = f"https://www.irs.gov/prior-year-forms-and-instructions{href}"  # Use the full relative path from the href

            else:
                print("No 'Next' button found. Ending pagination.")
                current_url = None
        else:
            print(f"Failed to retrieve data: {search_results.status_code}")


        
    # used to print table rows to console
            #   https://www.youtube.com/watch?v=lC6mucyD17k
            # soup = BeautifulSoup(search_results.content, 'html.parser')
            # tbody = soup.tbody
            # trs = tbody.contents
            # print(trs)











if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Type here what file you'll use for you search terms. Each term must be on new line. To run: 'python utility2.py' <path_to_search_terms_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]

    #  # Read the search term from a file
    # if validate_search_terms(file_path):
    #     with open("search_terms.txt", "r") as file:
    #         search_terms = file.read().strip()
    #     main(search_terms)
    # else:
    #     print("Check that your search terms are seperated on new lines")
    try:
        # Combine validated search terms into a single string
        combined_search_terms = combine_terms_from_file(file_path)
        print("Search Terms:", combined_search_terms)  # For debugging/verification
        # Pass the combined terms to the main function
        main(combined_search_terms)
    except ValueError as e:
        print(e)

    