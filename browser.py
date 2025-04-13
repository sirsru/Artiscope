from random import choice

from Cython.Compiler.Visitor import PrintTree
from bs4 import BeautifulSoup
from PIL import Image
from googlesearch import search
import requests
import io
import os
import hashlib
import re

from pygments.styles.paraiso_dark import GREEN

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

themes = {
    "DARK": {
        "RESET": "\033[0m",
        "BOLD": "\033[1m",
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "YELLOW": "\033[33m",
        "BLUE": "\033[34m",
        "MAGENTA": "\033[35m",
        "CYAN": "\033[36m",
        "WHITE": "\033[37m",
        "BLACK": "\033[30m",
    },
    "LIGHT": {
        "RESET": "\033[0m",
        "BOLD": "\033[1m",
        "RED": "\033[91m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "BLUE": "\033[94m",
        "MAGENTA": "\033[95m",
        "CYAN": "\033[96m",
        "WHITE": "\033[97m",
        "BLACK": "\033[98m",
    },
    "RETRO": {
        "RESET": "\033[0m",
        "BOLD": "\033[1m",
        "RED": "\033[38;2;192;72;82m",    # Lightened Red from #D52429 (Faded red)
        "GREEN": "\033[38;2;232;142;119m",  # Lightened Orange from #F1602C (Faded orange)
        "YELLOW": "\033[38;2;227;180;101m", # Lightened Yellow-Orange from #EC8922 (Faded yellow-orange)
        "BLUE": "\033[38;2;161;105;46m",    # Lightened Brown from #915018 (Faded brown)
        "MAGENTA": "\033[38;2;145;90;43m",  # Lightened Dark Brown from #6C3F18 (Faded brownish)
        "CYAN": "\033[38;2;161;105;46m",    # Same as BLUE for consistency (Faded brown)
        "WHITE": "\033[38;2;235;235;235m",  # Off-white for washed-out effect
        "BLACK": "\033[38;2;75;75;75m",     # Muted Black (#4B4B4B) for washed-out black
    },
    "PASTEL": {
        "RESET": "\033[0m",
        "BOLD": "\033[1m",
        "RED": "\033[38;2;255;182;193m",    # Pastel light pink
        "GREEN": "\033[38;2;187;255;163m",  # Pastel light green
        "YELLOW": "\033[38;2;253;253;150m", # Pastel light yellow
        "BLUE": "\033[38;2;174;198;255m",   # Pastel light blue
        "MAGENTA": "\033[38;2;255;178;227m",# Pastel light magenta
        "CYAN": "\033[38;2;182;255;255m",   # Pastel light cyan
        "WHITE": "\033[38;2;255;255;255m",  # White for pastel style
        "BLACK": "\033[38;2;200;200;200m",  # Light gray for black in pastel
    },
    "VINTAGE": {
        "RESET": "\033[0m",
        "BOLD": "\033[1m",
        "RED": "\033[38;2;143;75;60m",    # Vintage brownish red
        "GREEN": "\033[38;2;85;93;66m",   # Muted green
        "YELLOW": "\033[38;2;178;156;67m",# Vintage yellow
        "BLUE": "\033[38;2;65;75;86m",    # Deep vintage blue
        "MAGENTA": "\033[38;2;123;75;113m",# Muted magenta
        "CYAN": "\033[38;2;60;90;110m",   # Soft cyan
        "WHITE": "\033[38;2;241;232;199m",# Soft white
        "BLACK": "\033[38;2;78;62;50m",   # Dark brownish black
    },
    "DESERT": {
        "RESET": "\033[0m",
        "BOLD": "\033[1m",
        "RED": "\033[38;2;255;140;105m",    # Desert red (lighter and more orange)
        "GREEN": "\033[38;2;107;142;35m",   # Desert green (duller)
        "YELLOW": "\033[38;2;210;180;140m", # Desert yellow (muted)
        "BLUE": "\033[38;2;70;130;180m",    # Desert blue
        "MAGENTA": "\033[38;2;128;0;128m",  # Desert magenta (darker)
        "CYAN": "\033[38;2;0;255;255m",     # Desert cyan
        "WHITE": "\033[38;2;255;255;255m",  # Desert white
        "BLACK": "\033[38;2;0;0;0m",        # Desert black
    },
    "NEON": {
        "RESET": "\033[0m",
        "BOLD": "\033[1m",
        "RED": "\033[38;2;255;0;0m",        # Neon red
        "GREEN": "\033[38;2;57;255;20m",    # Neon green
        "YELLOW": "\033[38;2;255;255;0m",   # Neon yellow
        "BLUE": "\033[38;2;0;102;255m",     # Neon blue
        "MAGENTA": "\033[38;2;255;0;255m",  # Neon magenta
        "CYAN": "\033[38;2;0;255;255m",     # Neon cyan
        "WHITE": "\033[38;2;255;255;255m",  # White neon
        "BLACK": "\033[38;2;0;0;0m",        # Black
    },
    "WINTER": {
        "RESET": "\033[0m",
        "BOLD": "\033[1m",
        "RED": "\033[38;2;255;87;34m",     # Winter red
        "GREEN": "\033[38;2;0;128;128m",   # Winter green (pine)
        "YELLOW": "\033[38;2;255;214;0m",  # Winter yellow (snowy)
        "BLUE": "\033[38;2;25;118;210m",   # Winter blue
        "MAGENTA": "\033[38;2;193;64;114m",# Winter magenta
        "CYAN": "\033[38;2;0;183;189m",    # Winter cyan
        "WHITE": "\033[38;2;255;255;255m", # Winter white
        "BLACK": "\033[38;2;33;33;33m",    # Winter black (darker tone)
    },
    "OCEAN": {
        "RESET": "\033[0m",
        "BOLD": "\033[1m",
        "RED": "\033[38;2;255;69;0m",      # Ocean red (darker)
        "GREEN": "\033[38;2;46;139;87m",   # Ocean green (deeper)
        "YELLOW": "\033[38;2;255;215;0m",  # Ocean yellow
        "BLUE": "\033[38;2;70;130;180m",   # Ocean blue (darker)
        "MAGENTA": "\033[38;2;255;105;180m",# Ocean magenta
        "CYAN": "\033[38;2;0;206;209m",    # Ocean cyan
        "WHITE": "\033[38;2;255;255;255m", # Ocean white
        "BLACK": "\033[38;2;0;0;0m",       # Ocean black
    }
}


settings = {
    "max_width": get_terminal_width(),
    "check_similarity": True,
    "allowed_formats": ["PNG", "JPEG", "GIF", "BMP", "TIFF", "WEBP"],
    "themes": list(themes.keys()),  # Dynamically get theme names from the 'themes' dictionary
    "current_theme": 0,  # Default theme is the first one in the list
    "verbose_output": True,
    "emoji": True
}

version = "Version 1.0.1"
# Define color codes for different themes

def apply_theme(theme_name):
    global RESET, BOLD, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, BLACK

    theme = themes.get(theme_name.upper(), themes["DARK"])  # Default to DARK theme if invalid
    RESET, BOLD, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, BLACK = theme.values()

def display_settings_menu():
    print(f"\n{BOLD}{CYAN}+------------------------------------------------------+{RESET}")
    print(f"{BOLD}{CYAN}|              ✎ Artiscope ── Settings Menu              {RESET}")
    print(f"{CYAN}+------------------------------------------------------+{RESET}")
    print(f"{CYAN}|{RESET} [1] Max ASCII Width        → {YELLOW}{settings['max_width']:<30}{RESET}{RESET}")
    print(f"{CYAN}|{RESET} [2] Similarity Check       → {YELLOW}{'Enabled' if settings['check_similarity'] else 'Disabled':<30}{RESET}{RESET}")
    print(f"{CYAN}|{RESET} [3] Allowed Formats        → {YELLOW}{', '.join(settings['allowed_formats']):<30}{RESET}{RESET}")
    print(f"{CYAN}|{RESET} [4] Current Theme          → {YELLOW}{settings['themes'][settings['current_theme']]:<30}{RESET}{RESET}")
    print(f"{CYAN}|{RESET} [5] verbose output         → {YELLOW}{settings['verbose_output']}{RESET}{RESET}")
    print(f"{CYAN}|{RESET} [6] Emoji support          → {YELLOW}{settings['emoji']}{RESET}{RESET}")
    print(f"{CYAN}|{RESET} [7] {RED}← Back to Main Menu{RESET:<38}{RESET}")
    print(f"{CYAN}+------------------------------------------------------+{RESET}")
    print(f"{CYAN}| Repo:{RESET} Visit https://github.com/sirsru/Artiscope     {CYAN}{RESET}")
    print(f"{CYAN}+------------------------------------------------------+{RESET}\n")

    choice = input(f"{BOLD}{YELLOW}→ Select an option [1-7]: {RESET}").strip()

    if choice == '1':
        new_width = input(f"{CYAN}→ Enter new max ASCII width: {RESET}")
        try:
            settings['max_width'] = int(new_width)
            print(f"{GREEN}✓ Max width set to {settings['max_width']}{RESET}")
        except ValueError:
            print(f"{RED}✗ Invalid input. Please enter a number.{RESET}")
    elif choice == '2':
        settings['check_similarity'] = not settings['check_similarity']
        print(f"{GREEN}✓ Similarity check {'enabled' if settings['check_similarity'] else 'disabled'}{RESET}")
    elif choice == '3':
        new_formats = input(f"{CYAN}→ Enter allowed formats (comma-separated): {RESET}")
        settings['allowed_formats'] = [fmt.strip().upper() for fmt in new_formats.split(',')]
        print(f"{GREEN}✓ Formats updated: {', '.join(settings['allowed_formats'])}{RESET}")
    elif choice == '4':
        settings['current_theme'] = (settings['current_theme'] + 1) % len(settings['themes'])
        apply_theme(settings['themes'][settings['current_theme']])
        print(f"{GREEN}✓ Switched to theme: {settings['themes'][settings['current_theme']]}{RESET}")
    elif choice == '5':
        settings["verbose_output"] = not settings["verbose_output"]
    elif choice == '6':
        settings["emoji"] = not settings["emoji"]
    elif choice == '7':
        return
    else:
        print(f"{RED}✗ Invalid choice. Try again.{RESET}")

    display_settings_menu()


# Initialize with the default theme
apply_theme(settings["themes"][settings["current_theme"]])

def check_network():
    try:
        response = requests.get('https://github.com/sirsru', timeout=15)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False


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


def scrape_and_output_text(url):
    if not url.lower().startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        response = requests.get(url, allow_redirects=True)
        final_url = response.url
    except requests.exceptions.RequestException as e:
        print(f"{RED}Error fetching page {url}: {e}{RESET}")
        return

    print(f"{CYAN}Page redirected to: {final_url}{RESET}")

    soup = BeautifulSoup(response.text, 'html.parser')

    text_content = soup.get_text(separator="\n", strip=True)

    print(f"\n{WHITE}{text_content}{RESET}")


def image_to_ascii(image_url, max_width=settings['max_width'], previous_image_hash=None):
    try:
        response = requests.get(image_url)
        img = Image.open(io.BytesIO(response.content))

        if img.format not in settings["allowed_formats"] and settings["verbose_output"]:
            print(f"{YELLOW}Skipping unsupported image format: {img.format} (URL: {image_url}){RESET}")
            return None, previous_image_hash

        current_image_hash = generate_image_hash(img)
        if settings["check_similarity"] and settings["verbose_output"] and previous_image_hash and current_image_hash == previous_image_hash:
            print(f"{MAGENTA}Skipping similar image.{RESET}")
            return None, previous_image_hash
    except Exception as e:
        print(f"{RED}→ Error fetching or opening image {image_url}: {e}{RESET}")
        return None, previous_image_hash

    terminal_width = 100
    width = min(max_width, terminal_width - 2)
    aspect_ratio = img.height / img.width
    height = int(aspect_ratio * width)
    img = img.resize((width, height))
    img = img.convert('RGB')

    ascii_chars = "██▓▒░/=:_. "
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

    scrape_and_output_text(url)

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

def google_search(query, num_results=10):
    results = []
    try:
        for url in search(query, num_results=num_results):
            results.append(url)

        if results:
            return results
        else:
            print(f"{RED}✗ No results found for '{query}'. Please try again.{RESET}")
            return []

    except Exception as e:
        print(f"{RED} ✗ Error fetching Google search results: {e}{RESET}")
        return []

# ------------------info and update definitions --------------------

def find_browser_py(start_path='.'):
    for root, _, files in os.walk(start_path):
        if 'browser.py' in files:
            return os.path.join(root, 'browser.py')
    return None

def download_latest_browser_py(repo_url, local_path):
    raw_url = 'https://raw.githubusercontent.com/sirsru/Artiscope/refs/heads/main/browser.py'
    response = requests.get(raw_url)
    if response.status_code == 200:
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f'[✓] Replaced: {local_path}')
    else:
        print(f"{RED}[✗] Failed to download browser.py (HTTP {response.status_code}){RESET}")

def get_latest_version_from_readme():
    global version
    url = "https://raw.githubusercontent.com/sirsru/Artiscope/main/README.md"
    response = requests.get(url)

    if response.status_code == 200:
        readme_lines = response.text.strip().splitlines()
        if len(readme_lines) >= 2:
            version_line = readme_lines[1].strip()
            print(f"[✓] Found version: {version_line}")
            if version_line != version:
                print(f"{RED}★ You should probably update!{RESET}")
            else:
                print(f"{GREEN}✓ You are up to date!{RESET}")
            return version_line
        else:
            print("[✗] README.md is too short to contain a version line.")
    else:
        print(f"[✗] Failed to fetch README.md (HTTP {response.status_code})")

    return None


def info():
    if settings["emoji"]:
        print(f"\n{BLUE}+-------------------- ⚙️ Version info and updater --------------------+{RESET}")
        print(f"{BLUE}|{RESET}📦 Release → {version}{RESET}")
        print(f"{BLUE}|{RESET}1. 📥 Update by cloning github repo{RESET}")
        print(f"{BLUE}|{RESET}2. 📡 Check for update ★ (recommended before update){RESET}")
        print(f"{BLUE}|{RESET}3. ⬅️ {RED}Exit{RESET}")
    else:
        print(f"\n{BLUE}+-------------------- ⚙️ Version info and updater --------------------+{RESET}")
        print(f"{BLUE}|{RESET}{version}{RESET}")
        print(f"{BLUE}|{RESET}1. ↻ Update by cloning github repo (will replace current browser.py){RESET}")
        print(f"{BLUE}|{RESET}2. ⏱ Check for update ★ (recommended before update){RESET}")
        print(f"{BLUE}|{RESET}3. ⬅ {RED}Exit{RESET}")
    print(f"{BLUE}+---------------------------------------------------------------------+{RESET}")
    choice = input("choose option [1-3]")

    if choice == '1':
        download_latest_browser_py('https://github.com/sirsru/Artiscope', find_browser_py())
    elif choice == '2':
        get_latest_version_from_readme()

def interactive_browsing():
    print(f"{CYAN}Welcome to Artiscope the interactive Ascii internet browser!{RESET}")

    if check_network():
        print(f"{GREEN}✓ You are connected to the internet!{RESET}")
    else:
        print(f"{RED}✗ You are not connected to the internet!{RESET}")

    while True:
        print(f"\n{BLUE}+-------------------- Main Menu --------------------+{RESET}")
        print(f"{BLUE}|{RESET}1. enter direct URL")
        print(f"{BLUE}|{RESET}2. {CYAN}Search the internet{RESET}")
        print(f"{BLUE}|{RESET}3. {CYAN}Settings{RESET}")
        print(f"{BLUE}|{RESET}4. {YELLOW}Info and updates{RESET}")
        print(f"{BLUE}|{RESET}5. {RED}Exit{RESET}")
        print(f"{BLUE}+---------------------------------------------------+{RESET}")
        choice = input(f"{GREEN}Enter your choice: {RESET}").strip()

        if choice == '1':
            url = input(f"{GREEN}Enter a URL to start browsing: {RESET}").strip()
            browsing_url(url)

        elif choice == '2':
            search_query = input(f"{CYAN}Enter a search term: {RESET}").strip()
            search_results = google_search(search_query)
            if search_results:
                print(f"\n{CYAN}Top search results for '{search_query}':{RESET}")
                for idx, result in enumerate(search_results, 1):
                    print(f"{GREEN}{idx}. {result}{RESET}")
                show_options_menu(search_results)

        elif choice == '3':
            display_settings_menu()

        elif choice == '4':
            info()

        elif choice == '5':
            print(f"{RED}Exiting the browser. Goodbye!{RESET}")
            break
        else:
            print(f"{RED}✗ Invalid choice.{RESET}")


def browsing_url(url):
    while True:
        links = scrape_and_convert_images(url)
        print(f"\n{BLUE}Now browsing: {url}{RESET}")
        print(f"\n{BLUE}+-------------------- Browse Menu --------------------+{RESET}")
        print(f"{BLUE}|{RESET}1. {GREEN}Go to link # {RESET}.")
        print(f"{BLUE}|{RESET}2. {CYAN}Enter another URL{RESET}.")
        print(f"{BLUE}|{RESET}3. {CYAN}Search for something{RESET}.")
        print(f"{BLUE}|{RESET}4. {RED}Go back to Main Menu{RESET}")
        print(f"{BLUE}+-----------------------------------------------------+{RESET}")
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

        elif choice == '3':
            search_query = input(f"{CYAN}Enter a search term: {RESET}").strip()
            search_results = google_search(search_query)
            print(f"\n{CYAN}Top search results for '{search_query}':{RESET}")
            for idx, result in enumerate(search_results, 1):
                print(f"{GREEN}{idx}. {result}{RESET}")
            show_options_menu(search_results)

        elif choice == '4':
            print(f"{RED}Going back to Main Menu...{RESET}")
            break


def show_options_menu(results=None):
    print(f"\n{BLUE}+-------------------- Options menu --------------------+{RESET}")
    print(f"{BLUE}|{RESET}1. {GREEN}Go to link # {RESET}.")
    print(f"{BLUE}|{RESET}2. {CYAN}Enter another URL{RESET}.")
    print(f"{BLUE}|{RESET}3. {CYAN}Search for something{RESET}.")
    print(f"{BLUE}|{RESET}4. {RED}Go back to Main Menu{RESET}")
    print(f"{BLUE}+------------------------------------------------------+{RESET}")

    choice = input(f"{GREEN}Enter your choice: {RESET}").strip()

    if choice == '1' and results:
        try:
            link_choice = int(input(f"{CYAN}Enter the link number to visit: {RESET}")) - 1
            selected_link = results[link_choice]
            print(f"{MAGENTA}Going to {selected_link}{RESET}")
            links = scrape_and_convert_images(selected_link)
            show_options_menu(links)

        except (ValueError, IndexError):
            print(f"{RED}Invalid choice. Please try again.{RESET}")

    elif choice == '2':
        print(f"{CYAN}Going back to the previous page.{RESET}")
        url = input(f"{GREEN}Enter a URL to go back to (or 'exit' to quit): {RESET}").strip()
        if url.lower() == 'exit':
            print(f"{RED}Exiting the browser. Goodbye!{RESET}")
            exit()

    elif choice == '3':
        search_query = input(f"{CYAN}Enter a search term: {RESET}").strip()
        search_results = google_search(search_query)
        print(f"\n{CYAN}Top search results for '{search_query}':{RESET}")
        for idx, result in enumerate(search_results, 1):
            print(f"{GREEN}{idx}. {result}{RESET}")
        show_options_menu(search_results)

    elif choice == '4':
        print(f"{MAGENTA}Going back to Main Menu...{RESET}")
        return



if __name__ == "__main__":
    print(logo)
    interactive_browsing()
