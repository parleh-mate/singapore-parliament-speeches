from bs4 import BeautifulSoup
import re

# Specify the path to your HTML file
html_file_path = "/Users/jeremy.chia/Documents/Github/singapore-parliament-speeches/scripts/resource-archive-html/2000-08-25.html"

# Read HTML content from the file
with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Read HTML content from the file
with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")


def extract_names(heading_text, end_keyword):
    heading = soup.find("div", text=heading_text)
    if heading:
        names = heading.find_all_next("br")
        extracted_names = []
        for br_tag in names:
            next_sibling = br_tag.next_sibling
            if next_sibling and next_sibling.string:
                name = next_sibling.string.strip()
                # Skip lines with "Column"
                if end_keyword.lower() in name.lower():
                    break
                extracted_names.append(name)
        return extracted_names
    return []


# Extract and print names of members present
present_names = extract_names("PRESENT:", "ABSENT:")
print("Members Present:")
for name in present_names:
    print(name)

# Extract and print names of members absent
absent_names = extract_names("ABSENT:", "ASSENT TO BILLS PASSED")
print("\nMembers Absent:")
for name in absent_names:
    print(name)
