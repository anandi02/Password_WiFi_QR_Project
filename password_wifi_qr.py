
import secrets
import string
import getpass
import qrcode


def generate_password(length):
    """Generate a secure random password."""

    if length < 4:
        raise ValueError("Password length must be at least 4.")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+"

    all_characters = lowercase + uppercase + digits + symbols

    # Guarantee at least one character from each category.
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    # Fill the remaining positions.
    for _ in range(length - 4):
        password.append(secrets.choice(all_characters))

    # Randomize character positions.
    secrets.SystemRandom().shuffle(password)

    return "".join(password)


def escape_wifi_text(value):
    """Escape special characters in Wi-Fi QR data."""
    for char in ("\\", ";", ",", '"'):
        value = value.replace(char, "\\" + char)
    return value


def generate_wifi_qr():
    """Create and save a Wi-Fi connection QR code."""

    ssid = input("Enter Wi-Fi name (SSID): ").strip()

    if not ssid:
        print("Wi-Fi name cannot be empty.")
        return

    wifi_password = getpass.getpass(
        "Enter Wi-Fi password (input is hidden): "
    )

    if not wifi_password:
        print("Password cannot be empty for WPA/WPA2.")
        return

    safe_ssid = escape_wifi_text(ssid)
    safe_password = escape_wifi_text(wifi_password)

    # WPA format is used for typical WPA/WPA2 Wi-Fi networks.
    wifi_data = (
        f"WIFI:T:WPA;S:{safe_ssid};P:{safe_password};;"
    )

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )

    qr.add_data(wifi_data)
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    filename = "wifi_qr.png"
    image.save(filename)

    print(f"\nQR code saved as: {filename}")
    print("Scan it with a compatible phone to test Wi-Fi setup.")
    print("Keep this QR image private: it contains your Wi-Fi credentials.")


def main():
    while True:
        print("\n===== PASSWORD & WI-FI QR GENERATOR =====")
        print("1. Generate a random password")
        print("2. Generate a Wi-Fi QR code")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            try:
                length = int(
                    input("Enter password length (minimum 4): ")
                )

                if length > 256:
                    print("Please choose a length of 256 or less.")
                    continue

                password = generate_password(length)
                print("\nYour generated password:")
                print(password)

                print("\nStore your password securely.")
            except ValueError:
                print("Please enter a valid number of at least 4.")

        elif choice == "2":
            try:
                generate_wifi_qr()
            except (OSError, ValueError) as error:
                print(f"Could not create the QR code: {error}")

        elif choice == "3":
            print("Thank you for using the program!")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
