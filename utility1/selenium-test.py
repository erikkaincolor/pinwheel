from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

# TO RUN IN CHROME BROWSER:
# `python selenium-test.py`

# Initialize Selenium WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()

# ch*tgpt helper func
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
    """
    Validate the search terms from a file and combine them into a single string 
    with exactly one space between valid terms.
    """
    terms = validate_search_terms(file_path)
    return " ".join(terms)


def main(combined_search_terms):
    try:
        # Load the website
        url =f"https://www.irs.gov/prior-year-forms-and-instructions?"

        driver.get(url)

        # Type search in the search field and submit
        search_field = driver.find_element(By.ID, "edit-find")  # Assuming your input field has ID "edit-find"
        search_field.send_keys(combined_search_terms)

        submit_button = driver.find_element(By.ID, "edit-submit-pup-picklists")  # Assuming your submit button has ID "edit-submit-pup-picklists"
        sleep(5)  # Allow scrolling animation

        submit_button.click()
        sleep(10)

        # Wait for the results page
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Revision Date"))
        )




        driver.quit()


       
    except Exception as e:
        print(f"An error occurred: {e}")
    


if __name__ == "__main__":
    file_path = 'utility1/search_terms.txt'

    try:
        # Combine validated search terms into a single string
        combined_search_terms = combine_terms_from_file(file_path)
        print("Combined Search Terms:", combined_search_terms)  # For debugging/verification
        # Pass the combined terms to the main function
        main(combined_search_terms)
    except ValueError as e:
        print(e)
