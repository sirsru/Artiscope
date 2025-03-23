from bs4 import BeautifulSoup
from PIL import Image
from googlesearch import search
import requests
import io
import os
import hashlib
import re

logo = ''' 
░▒▓██████▓▒ ░▒▓███████▓▒ ▒▓████████▓▒ ▒▓█▓▒░ ▒▓███████▓▒ ░▒▓██████▓▒░ ░▒▓██████▓▒░ ▒▓███████▓▒░ ▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒ ▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒ ▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒ ▒▓█▓▒░░▒▓█▓▒ ▒▓█▓▒░░▒▓█▓▒ ▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒ ▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒ ▒▓█▓▒░      ░▒▓█▓▒░       ▒▓█▓▒░░▒▓█▓▒ ▒▓█▓▒░░▒▓█▓▒ ▒▓█▓▒░        
░▒▓████████▓▒ ▒▓███████▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒ ░▒▓██████▓▒ ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒ ▒▓███████▓▒░ ▒▓██████▓▒░   
░▒▓█▓▒░░▒▓█▓▒ ▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒       ░▒▓█▓▒ ▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒ ▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒ ▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒       ░▒▓█▓▒ ▒▓█▓▒░░▒▓█▓▒ ▒▓█▓▒░░▒▓█▓▒ ▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒ ▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒ ▒▓███████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░ ▒▓█▓▒░      ░▒▓████████▓▒░ 
https://github.com/sirsru/Artiscope
'''


def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 100


settings = {
    "max_width": get_terminal_width(),
    "check_similarity": True,
    "allowed_formats": ["PNG", "JPEG", "GIF", "BMP", "TIFF", "WEBP"]
}

def display_settings_menu():
    print(f"\n{CYAN}Settings{RESET}")
    print(f"1. {GREEN}Set maximum width/resolution for ASCII art ({settings['max_width']}){RESET}")
    print(f"2. {GREEN}Toggle image similarity check ({'Enabled' if settings['check_similarity'] else 'Disabled'}){RESET}")
    print(f"3. {GREEN}Set allowed image formats ({', '.join(settings['allowed_formats'])}){RESET}")
    print(f"4. {RED}Back to main menu{RESET}")
    print("Go to https://github.com/sirsru/Artiscope for more help!")
    choice = input(f"{GREEN}Enter your choice: {RESET}").strip()

    if choice == '1':
        new_width = input(f"{CYAN}Enter new maximum width for ASCII art: {RESET}")
        try:
            settings['max_width'] = int(new_width)
            print(f"{GREEN}Max width set to {settings['max_width']}{RESET}")
        except ValueError:
            print(f"{RED}Invalid input. Please enter a number.{RESET}")
    elif choice == '2':
        settings['check_similarity'] = not settings['check_similarity']
        print(f"{GREEN}Image similarity check {'enabled' if settings['check_similarity'] else 'disabled'}{RESET}")
    elif choice == '3':
        new_formats = input(f"{CYAN}Enter allowed image formats (comma separated): {RESET}")
        settings['allowed_formats'] = [fmt.strip().upper() for fmt in new_formats.split(',')]
        print(f"{GREEN}Allowed image formats updated to {', '.join(settings['allowed_formats'])}{RESET}")
    elif choice == '4':
        return
    else:
        print(f"{RED}Invalid choice, try again.{RESET}")
    display_settings_menu()


def check_network():
    try:
        response = requests.get('https://github.com/sirsru', timeout=15)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False


RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BLACK = "\033[30m"


def generate_image_hash(image):
    img = image.convert("L")
    img = img.resize((8, 8))
    pixels = list(img.getdata())
    avg_pixel_value = sum(pixels) / len(pixels)
    img_hash = ''.join(['1' if p > avg_pixel_value else '0' for p in pixels])
    return img_hash


def rgb_to_terminal_color(r, g, b):
    if r < 85:
        if g < 85:
            return BLACK
        elif g < 170:
            return GREEN
        else:
            return CYAN
    elif r < 170:
        if g < 85:
            return BLUE
        elif g < 170:
            return MAGENTA
        else:
            return YELLOW
    else:
        if g < 85:
            return RED
        elif g < 170:
            return WHITE
        else:
            return WHITE


def image_to_ascii(image_url, max_width=settings['max_width'], previous_image_hash=None):
    try:
        response = requests.get(image_url)
        img = Image.open(io.BytesIO(response.content))

        if img.format not in settings["allowed_formats"]:
            print(f"{YELLOW}Skipping unsupported image format: {img.format} (URL: {image_url}){RESET}")
            return None, previous_image_hash

        current_image_hash = generate_image_hash(img)
        if settings["check_similarity"] and previous_image_hash and current_image_hash == previous_image_hash:
            print(f"{MAGENTA}Skipping similar image.{RESET}")
            return None, previous_image_hash
    except Exception as e:
        print(f"{RED}Error fetching or opening image {image_url}: {e}{RESET}")
        return None, previous_image_hash

    terminal_width = 100
    width = min(max_width, terminal_width - 2)
    aspect_ratio = img.height / img.width
    height = int(aspect_ratio * width)
    img = img.resize((width, height))
    img = img.convert('RGB')

    ascii_chars = "██▓▒░/=-:_. "
    ascii_image = ""
    colored_ascii_art = []

    for pixel in img.getdata():
        r, g, b = pixel
        color = rgb_to_terminal_color(r, g, b)
        brightness = (r + g + b) // 3
        ascii_char = ascii_chars[brightness // 32]
        colored_ascii_art.append(f"{color}{ascii_char}{RESET}")

    ascii_image = "\n".join(["".join(colored_ascii_art[i:i + width]) for i in range(0, len(colored_ascii_art), width)])

    return ascii_image, current_image_hash


def scrape_and_convert_images(url, max_width=settings['max_width']):
    if not url.lower().startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        response = requests.get(url, allow_redirects=True)
        final_url = response.url
    except requests.exceptions.RequestException as e:
        print(f"{RED}Error fetching page {url}: {e}{RESET}")
        return []

    print(f"{CYAN}Page redirected to: {final_url}{RESET}")

    soup = BeautifulSoup(response.text, 'html.parser')

    images = soup.find_all('img')
    links = soup.find_all('a')
    forms = soup.find_all('form')
    input_fields = soup.find_all('input', {'type': 'text'})

    previous_image_hash = None
    for img in images:
        img_url = img.get('src')
        if img_url:
            if not img_url.startswith(('http://', 'https://')):
                img_url = final_url + img_url
            print(f"{CYAN}Converting image: {img_url}{RESET}")
            ascii_art, previous_image_hash = image_to_ascii(img_url, settings['max_width'], previous_image_hash)
            if ascii_art:
                print(f"{MAGENTA}ASCII Art for {img_url}:\n{RESET}")
                print(ascii_art)
                print("-" * 50)

    print(f"\n{YELLOW}Links on the page:{RESET}")
    links_list = []
    for idx, link in enumerate(links):
        link_text = link.get_text(strip=True)
        link_url = link.get('href')
        if link_url:
            if not link_url.startswith(('http://', 'https://')):
                link_url = final_url + link_url
            links_list.append((link_text, link_url))
            print(f"{GREEN}{idx + 1}. {link_text} - {link_url}{RESET}", end=' \n ')

    if input_fields:
        print(f"\n{CYAN}Input fields found on the page. Would you like to type in any?{RESET}")
        for idx, input_field in enumerate(input_fields):
            print(f"{GREEN}{idx + 1}. {input_field.get('name', 'Unnamed input field')}{RESET}")
        print(f"{YELLOW}Enter the number of the input field you want to interact with, or 0 to skip:{RESET}")
        choice = input(f"{GREEN}Enter your choice: {RESET}").strip()

        if choice.isdigit() and int(choice) > 0:
            input_field = input_fields[int(choice) - 1]
            field_name = input_field.get('name', 'Unnamed field')
            user_input = input(f"{CYAN}Enter your input for the field '{field_name}': {RESET}")
            print(f"{MAGENTA}You entered: {user_input}{RESET}")

    print()

    return links_list


from googlesearch import search

def google_search(query, num_results=10):
    results = []
    try:
        # Use googlesearch to fetch results
        for url in search(query, num_results=num_results):
            results.append(url)

        if results:
            return results
        else:
            print(f"{RED}No results found for '{query}'. Please try again.{RESET}")
            return []

    except Exception as e:
        print(f"{RED}Error fetching Google search results: {e}{RESET}")
        return []



def interactive_browsing():
    print(f"{CYAN}Welcome to Artiscope the interactive Ascii internet browser!{RESET}")

    if check_network():
        print(f"{GREEN}You are connected to the internet!{RESET}")
    else:
        print(f"{RED}You are not connected to the internet!{RESET}")

    while True:
        print(f"\n{BLUE}Main Menu{RESET}")
        print(f"1. Browse the web")
        print(f"2. {CYAN}Search the web{RESET}")
        print(f"3. {CYAN}Settings{RESET}")
        print(f"4. {RED}Exit{RESET}")

        choice = input(f"{GREEN}Enter your choice: {RESET}").strip()

        if choice == '1':
            url = input(f"{GREEN}Enter a URL to start browsing: {RESET}").strip()
            while True:
                print(f"\n{BLUE}Now browsing: {url}{RESET}")
                links = scrape_and_convert_images(url)
                print(f"\n{YELLOW}Options:{RESET}")
                print(f"1. {GREEN}Go to link # {RESET}.")
                print(f"2. {CYAN}Enter another URL{RESET}.")
                print(f"3. {CYAN}Search for something{RESET}.")
                print(f"4. {RED}Go back to Main Menu{RESET}.")

                choice = input(f"{GREEN}Enter your choice: {RESET}").strip()

                if choice == '1':
                    try:
                        link_choice = int(input(f"{CYAN}Enter the link number to visit: {RESET}")) - 1
                        selected_link = links[link_choice]
                        url = selected_link[1]
                        print(f"{MAGENTA}Going to {url}{RESET}")
                    except (ValueError, IndexError):
                        print(f"{RED}Invalid choice. Please try again.{RESET}")

                elif choice == '2':
                    print(f"{CYAN}Going back to the previous page.{RESET}")
                    url = input(f"{GREEN}Enter a URL to go back to (or 'exit' to quit): {RESET}").strip()
                    if url.lower() == 'exit':
                        print(f"{RED}Exiting the browser. Goodbye!{RESET}")
                        break

                elif choice == '4':
                    print(f"{RED}Exiting the browser. Goodbye!{RESET}")
                    break

                elif choice == '3':
                    search_query = input(f"{CYAN}Enter a search term: {RESET}").strip()
                    search_results = google_search(search_query)
                    print(f"\n{CYAN}Top search results for '{search_query}':{RESET}")
                    for idx, result in enumerate(search_results, 1):
                        print(f"{GREEN}{idx}. {result}{RESET}")

        elif choice == '2':
            search_query = input(f"{CYAN}Enter a search term: {RESET}").strip()
            search_results = google_search(search_query)
            if search_results:
                print(f"\n{CYAN}Top search results for '{search_query}':{RESET}")
                for idx, result in enumerate(search_results, 1):
                    print(f"{GREEN}{idx}. {result}{RESET}")

                while True:
                    # Only show options related to search results.
                    print(f"\n{CYAN}Enter the number of the link you want to visit, or enter 0 to go back to the options menu.")
                    choice = input(f"{GREEN}Enter your choice: {RESET}").strip()

                    if choice == '0':
                        break

                    elif choice.isdigit():
                        link_choice = int(choice) - 1
                        if 0 <= link_choice < len(search_results):
                            selected_link = search_results[link_choice]
                            print(f"{MAGENTA}Going to {selected_link}{RESET}")
                            # Now, visit the selected link and browse it
                            links = scrape_and_convert_images(selected_link)
                            print(f"\n{YELLOW}Options:{RESET}")
                            print(f"1. {GREEN}Go to link # {RESET}.")
                            print(f"2. {CYAN}Enter another URL{RESET}.")
                            print(f"3. {CYAN}Search for something{RESET}.")
                            print(f"4. {RED}Go back to options menu{RESET}.")
                        else:
                            print(f"{RED}Invalid choice.{RESET}")

                    else:
                        print(f"{RED}Invalid input.{RESET}")

        elif choice == '3':
            display_settings_menu()

        elif choice == '4':
            print(f"{RED}Exiting the browser. Goodbye!{RESET}")
            break
        else:
            print(f"{RED}Invalid choice.{RESET}")





if __name__ == "__main__":
    print(logo)
    interactive_browsing()
