"""Retry a simulated menu fetch using real Asha Tea House drink names.

Static selection from the 17 Kearny Street menu, checked November 5, 2026:
https://ashateahouse.square.site/?location=AJMSYRF8H2C90
This demo runs offline; it does not fetch live availability or prices.
"""

from retry import retry


ASHA_MENU = [
    "Matcha Latte",
    "Strawberry Matcha Latte",
    "Hojicha Latte",
    "Matcha Fresco",
    "Asian Pear Oolong Tea",
    "Sea Salt Crema Tea",
]

attempts = iter(range(1, 4))


def fetch_boba_menu():
    attempt = next(attempts)
    print(f"Attempt {attempt}: fetching Asha Tea House's menu...")
    if attempt < 3:
        print("Connection dropped. Still thinking about that matcha.")
        raise ConnectionError("Simulated connection failure while loading the menu")
    return list(ASHA_MENU)


menu = retry(fetch_boba_menu)
print("Menu loaded: " + ", ".join(menu))
